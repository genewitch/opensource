# NetworkDashboard.ps1 — Real-time terminal network monitoring dashboard
# Requires: PowerShell 5.1+ (Windows PowerShell) or PowerShell 7+ (pwsh)

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION — Edit these to add/remove targets
# ═══════════════════════════════════════════════════════════════════════════════

$PingTargets = @("8.8.8.8", "1.1.1.1", "192.168.1.1")

$UrlTargets = @(
    @{ Url = "https://httpbin.org/get";  Label = "httpbin" }
    @{ Url = "https://google.com";       Label = "google"  }
)


$PingCountPerCycle = 10        # pings sent per measurement cycle
$PingIntervalMs   = 500        # milliseconds between pings within a cycle
$PingTimeoutMs    = 2000       # per-ping timeout in ms
$HistorySize      = 60         # samples kept in rolling buffer (for graphs)
$HttpTimeoutSec   = 10         # URL fetch timeout

# ═══════════════════════════════════════════════════════════════════════════════
# INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

try { $Host.UI.RawUI.CursorVisible = $false } catch {}
[Console]::TreatControlCAsInput = $false

$Ping = New-Object System.Net.NetworkInformation.Ping
$Sha256 = [System.Security.Cryptography.SHA256]::Create()

function New-TargetState {
    param([string]$Name, [string]$Type, [string]$Label = "")
    [PSCustomObject]@{
        Name      = $Name
        Type      = $Type
      Label     = $Label
        RttHistory = [double[]]::new($HistorySize)
        WriteIdx   = 0
        Count      = 0
        Sent       = 0
        Received   = 0
        Lost       = 0
        LastRtt    = [double]::NaN
        LastJitter = [double]::NaN
        LastHash   = ""
        ConsecFail = 0
    }
}

function Add-RttSample {
    param([PSCustomObject]$State, [double]$Rtt)
    $State.RttHistory[$State.WriteIdx % $HistorySize] = $Rtt
    $State.WriteIdx++
    if ($State.Count -lt $HistorySize) { $State.Count++ }
    $State.LastRtt = $Rtt
    $State.LastJitter = Get-Jitter -Values $State.RttHistory -Count $State.Count
}

function Get-Jitter {
    param([double[]]$Values, [int]$Count)
    # Exclude lost packets (negative values) from jitter calculation
    $sum = 0.0; $sumSq = 0.0; $valid = 0
    for ($i = 0; $i -lt $Count; $i++) {
        if ($Values[$i] -ge 0) {
            $sum  += $Values[$i]
            $sumSq += $Values[$i] * $Values[$i]
            $valid++
        }
    }
    if ($valid -lt 2) { return [double]::NaN }
    $mean = $sum / $valid
    [Math]::Sqrt(($sumSq / $valid) - ($mean * $mean))
}

function Get-LossPercent {
    param([PSCustomObject]$State)
    if ($State.Sent -eq 0) { return 0.0 }
    [Math]::Round(($State.Lost / $State.Sent) * 100, 3)
}

function Get-AvgRtt {
    param([PSCustomObject]$State)
    # Exclude lost packets (negative values) from average calculation
    $sum = 0.0; $valid = 0
    for ($i = 0; $i -lt $State.Count; $i++) {
        if ($State.RttHistory[$i] -ge 0) {
            $sum += $State.RttHistory[$i]
            $valid++
        }
    }
    if ($valid -eq 0) { return [double]::NaN }
    $sum / $valid
}

# ═══════════════════════════════════════════════════════════════════════════════
# COLOR HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

function Write-Colored {
    param([string]$Text, [ConsoleColor]$Fg = "White", [ConsoleColor]$Bg = "Black", [switch]$NoNewline)
    $oldFg = [Console]::ForegroundColor
    $oldBg = [Console]::BackgroundColor
    [Console]::ForegroundColor = $Fg
    [Console]::BackgroundColor = $Bg
    if ($NoNewline) { [Console]::Write($Text) } else { [Console]::WriteLine($Text) }
    [Console]::ForegroundColor = $oldFg
    [Console]::BackgroundColor = $oldBg
}

function Get-RttFgColor {
    param([double]$Rtt, [double]$Avg)
    if ([Double]::IsNaN($Avg) -or $Avg -eq 0) { return "Green" }
    $ratio = $Rtt / $Avg
    if     ($ratio -lt 1.5) { return "Green" }
    elseif ($ratio -lt 3.0) { return "Yellow" }
    else                    { return "Red" }
}

function Get-BarChar {
    param([double]$Rtt, [double]$Avg, [double]$StdDev, [bool]$IsLoss)
    if ($IsLoss) { return @{ Char = [char]0x00B7; Fg = "DarkRed" } }  # · middle dot
    if ([Double]::IsNaN($Avg) -or $Avg -eq 0) { return @{ Char = [char]0x2592; Fg = "Green" } }  # ▒
    if ([Double]::IsNaN($StdDev) -or $StdDev -lt 0.5) { $StdDev = [Math]::Max(1, $Avg * 0.1) }
    $diff = $Rtt - $Avg
    if     ($diff -lt 0)                        { return @{ Char = [char]0x2591; Fg = "Green" } }  # ░
    elseif ($diff -lt $StdDev)                  { return @{ Char = [char]0x2592; Fg = "Green" } }  # ▒
    elseif ($diff -lt ($StdDev * 2))            { return @{ Char = [char]0x2593; Fg = "Yellow" } } # ▓
    else                                        { return @{ Char = [char]0x2588; Fg = "Red" } }    # █
}

# ═══════════════════════════════════════════════════════════════════════════════
# DRAWING
# ═══════════════════════════════════════════════════════════════════════════════

function Draw-Header {
    param([int]$Width)
    $line = [string][char]0x2550 * [Math]::Max(0, $Width - 1)
    $time = Get-Date -Format "HH:mm:ss"
    $title = " NETWORK DASHBOARD"
    $padding = $Width - $title.Length - $time.Length - 1
    if ($padding -lt 1) { $padding = 1 }
    Write-Colored $line -Fg "DarkCyan"
    Write-Colored "$title$(' ' * $padding)$time" -Fg "Cyan"
    Write-Colored $line -Fg "DarkCyan"
}

function Draw-TableHeader {
    param([int]$BarWidth, [string]$Label, [switch]$ForUrl)
    $hdr = " $Label"
    Write-Colored $hdr -Fg "White" -NoNewline
    if (-not $ForUrl) {
        $cols = "  RTT    	   Jitter	Loss	"
        $bar  = " " + ([string][char]0x2500 * $BarWidth)
        Write-Colored $cols -Fg "DarkGray" -NoNewline
        Write-Colored "History" -Fg "DarkGray"
    } else {
        $cols = "		  RTT      SHA256        "
        $bar  = " " + ([string][char]0x2500 * $BarWidth)
        Write-Colored $cols -Fg "DarkGray" -NoNewline
        Write-Colored "History" -Fg "DarkGray"
    }
}

function Draw-PingRow {
    param([PSCustomObject]$State, [int]$BarWidth)
    $avgRtt = Get-AvgRtt -State $State
    $lossPct = Get-LossPercent -State $State

    # Name column (14 chars)
    $nameStr = $State.Name.PadRight(14)
    $nameColor = if ($State.ConsecFail -ge 3) { "Red" }
                 elseif ($State.ConsecFail -ge 1) { "Yellow" }
                 else { "White" }
    Write-Colored " $nameStr" -Fg $nameColor -NoNewline

    # RTT column
    if ([Double]::IsNaN($State.LastRtt)) {
        Write-Colored "  ---     " -Fg "DarkGray" -NoNewline
    } else {
        $rttStr = "{0,7:F1}ms" -f $State.LastRtt
        $rttColor = Get-RttFgColor -Rtt $State.LastRtt -Avg $avgRtt
        Write-Colored " $rttStr " -Fg $rttColor -NoNewline
    }

    # Jitter column
    if ([Double]::IsNaN($State.LastJitter)) {
        Write-Colored "  ---     " -Fg "DarkGray" -NoNewline
    } else {
        $jitStr = "{0,7:F1}ms" -f $State.LastJitter
        $jitColor = if ($State.LastJitter -lt 5) { "Green" }
                    elseif ($State.LastJitter -lt 20) { "Yellow" }
                    else { "Red" }
        Write-Colored " $jitStr " -Fg $jitColor -NoNewline
    }

    # Loss column
    $lossStr = "{0,6:F3}%" -f $lossPct
    $lossColor = if ($lossPct -eq 0) { "Green" }
                 elseif ($lossPct -le 5) { "Yellow" }
                 else { "Red" }
    Write-Colored " $lossStr " -Fg $lossColor -NoNewline

    # Bar graph
    Write-Colored " " -Fg "White" -NoNewline
    $barLen = [Math]::Min($State.Count, $BarWidth)
    for ($i = 0; $i -lt $barLen; $i++) {
        $sampleIdx = ($State.WriteIdx - $State.Count + $i + $HistorySize * 2) % $HistorySize
        $val = $State.RttHistory[$sampleIdx]
        $isLoss = ($val -lt 0)
        $absVal = [Math]::Abs($val)
        $bc = Get-BarChar -Rtt $absVal -Avg $avgRtt -StdDev $State.LastJitter -IsLoss $isLoss
        Write-Colored $bc.Char -Fg $bc.Fg -NoNewline
    }
    # Pad remaining space
    if ($barLen -lt $BarWidth) {
        Write-Colored (" " * ($BarWidth - $barLen)) -NoNewline
    }

    # Totals
    $totStr = "  {0}/{1}/{2}" -f $State.Sent, $State.Received, $State.Lost
    Write-Colored $totStr -Fg "DarkGray"
}

function Draw-UrlRow {
    param([PSCustomObject]$State, [int]$BarWidth)
    $avgRtt = Get-AvgRtt -State $State

    # Label column (14 chars)
    $displayText = if ($State.Label) { $State.Label } else { $State.Name }
    $label = if ($displayText.Length -gt 14) { $displayText.Substring(0, 14) } else { $displayText.PadRight(14) }
    $labelColor = if ($State.ConsecFail -ge 3) { "Red" }
                  elseif ($State.ConsecFail -ge 1) { "Yellow" }
                  else { "White" }
    Write-Colored " $label" -Fg $labelColor -NoNewline

    # RTT column
    if ([Double]::IsNaN($State.LastRtt)) {
        Write-Colored "  ---     " -Fg "DarkGray" -NoNewline
    } else {
        $rttStr = "{0,7:F1}ms" -f $State.LastRtt
        $rttColor = Get-RttFgColor -Rtt $State.LastRtt -Avg $avgRtt
        Write-Colored " $rttStr " -Fg $rttColor -NoNewline
    }

    # SHA256 column (first 10 chars)
    $hashStr = if ($State.LastHash.Length -gt 10) { $State.LastHash.Substring(0, 10) + ".." } else { $State.LastHash.PadRight(12) }
    Write-Colored " $hashStr " -Fg "DarkCyan" -NoNewline

    # Bar graph
    Write-Colored " " -Fg "White" -NoNewline
    $barLen = [Math]::Min($State.Count, $BarWidth)
    for ($i = 0; $i -lt $barLen; $i++) {
        $sampleIdx = ($State.WriteIdx - $State.Count + $i + $HistorySize * 2) % $HistorySize
        $val = $State.RttHistory[$sampleIdx]
        $isLoss = ($val -lt 0)
        $absVal = [Math]::Abs($val)
        $bc = Get-BarChar -Rtt $absVal -Avg $avgRtt -StdDev $State.LastJitter -IsLoss $isLoss
        Write-Colored $bc.Char -Fg $bc.Fg -NoNewline
    }
    if ($barLen -lt $BarWidth) {
        Write-Colored (" " * ($BarWidth - $barLen)) -NoNewline
    }

    # Status
    $statusStr = "  {0}/{1}" -f $State.Received, $State.Sent
    $statusColor = if ($State.ConsecFail -ge 3) { "Red" }
                   elseif ($State.ConsecFail -ge 1) { "Yellow" }
                   else { "Green" }
    Write-Colored $statusStr -Fg $statusColor
}

function Draw-Legend {
    param([int]$Width)
    Write-Colored "" 
    $legend = " $([char]0x2591)=below avg  $([char]0x2592)=normal  $([char]0x2593)=elevated  $([char]0x2588)=spike  $([char]0x00B7)=lost    Ctrl+C to exit"
    Write-Colored $legend -Fg "DarkGray"
}

function Draw-Display {
    param([PSCustomObject[]]$AllStates, [int]$BarWidth)
    # Move cursor to top-left instead of clearing (avoids flicker)
    [Console]::SetCursorPosition(0, 0)

    $winWidth = $host.UI.RawUI.WindowSize.Width
    Draw-Header -Width $winWidth

    Write-Colored ""

    $pingStates = $AllStates | Where-Object { $_.Type -eq "ping" }
    $urlStates  = $AllStates | Where-Object { $_.Type -eq "url" }

    if ($pingStates.Count -gt 0) {
        Write-Colored " PING TARGETS" -Fg "White"
        Draw-TableHeader -BarWidth $BarWidth -Label ""
        foreach ($s in $pingStates) {
            Draw-PingRow -State $s -BarWidth $BarWidth
        }
        Write-Colored ""
    }

    if ($urlStates.Count -gt 0) {
        Write-Colored " URL TARGETS" -Fg "White"
        Draw-TableHeader -BarWidth $BarWidth -Label "" -ForUrl
        foreach ($s in $urlStates) {
            Draw-UrlRow -State $s -BarWidth $BarWidth
        }
    }

    Draw-Legend -Width $winWidth

    # Clear remaining lines (in case previous frame was taller)
    $curY = [Console]::CursorTop
    $winH = $host.UI.RawUI.WindowSize.Height
    for ($y = $curY; $y -lt [Math]::Min($curY + 5, $winH); $y++) {
        [Console]::SetCursorPosition(0, $y)
        [Console]::Write((" " * $winWidth))
    }
    [Console]::SetCursorPosition(0, $curY)
}

function Get-BarWidth {
    $winWidth = $host.UI.RawUI.WindowSize.Width
    # Fixed columns before bar: " 14chars + rtt + jit/loss + space " ≈ 42 chars
    $fixedCols = 42
    [Math]::Max(20, $winWidth - $fixedCols)
}

# ═══════════════════════════════════════════════════════════════════════════════
# MEASUREMENT LOOPS
# ═══════════════════════════════════════════════════════════════════════════════

function Measure-PingCycle {
    param([PSCustomObject[]]$States)
    foreach ($state in $States) {
        $state.Sent++
        try {
            $reply = $Ping.Send($state.Name, $PingTimeoutMs)
            if ($reply.Status -eq [System.Net.NetworkInformation.IPStatus]::Success) {
                Add-RttSample -State $state -Rtt ([double]$reply.RoundtripTime)
                $state.Received++
                $state.ConsecFail = 0
            } else {
                # Record as -1 (lost) in history
                Add-RttSample -State $state -Rtt -1.0
                $state.Lost++
                $state.ConsecFail++
            }
        } catch {
            Add-RttSample -State $state -Rtt -1.0
            $state.Lost++
            $state.ConsecFail++
        }
        if ($PingIntervalMs -gt 0) {
            Start-Sleep -Milliseconds $PingIntervalMs
        }
    }
}

function Measure-UrlCycle {
    param([PSCustomObject[]]$States)
    foreach ($state in $States) {
        $state.Sent++
        $sw = [Diagnostics.Stopwatch]::StartNew()
        try {
            $response = Invoke-WebRequest -Uri $state.Name -UseBasicParsing -TimeoutSec $HttpTimeoutSec -ErrorAction Stop
            $sw.Stop()
            Add-RttSample -State $state -Rtt ([double]$sw.Elapsed.TotalMilliseconds)
            $state.Received++

            # Compute SHA256
            $bytes = [System.Text.Encoding]::UTF8.GetBytes($response.Content)
            $hash = $Sha256.ComputeHash($bytes)
            $hashHex = -join ($hash | ForEach-Object { $_.ToString("x2") })
            $state.LastHash = $hashHex
            $state.ConsecFail = 0
        } catch {
            $sw.Stop()
            Add-RttSample -State $state -Rtt -1.0
            $state.Lost++
            $state.ConsecFail++
        }
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════════════════════════

try {
    [Console]::Clear()

    # Create state objects
    $pingStates = foreach ($target in $PingTargets) {
        New-TargetState -Name $target -Type "ping"
    }
    $urlStates = foreach ($target in $UrlTargets) {
        New-TargetState -Name $target.Url -Type "url" -Label $target.Label
    }
    $allStates = $pingStates + $urlStates

    # Initial display
    $barWidth = Get-BarWidth
    Draw-Display -AllStates $allStates -BarWidth $barWidth

    # Continuous loop
    while ($true) {
        # Ping cycle
        Measure-PingCycle -States $pingStates

        # URL cycle
        if ($urlStates.Count -gt 0) {
            Measure-UrlCycle -States $urlStates
        }

        # Redraw
        $barWidth = Get-BarWidth
        Draw-Display -AllStates $allStates -BarWidth $barWidth
    }
} finally {
    try { $Host.UI.RawUI.CursorVisible = $true } catch {}
    [Console]::ForegroundColor = "White"
    [Console]::BackgroundColor = "Black"
    [Console]::Clear()
    Write-Host "Dashboard stopped." -ForegroundColor Cyan
}
