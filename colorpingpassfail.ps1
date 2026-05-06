# use it like `.\script.ps1 1.1.1.1`
# or `.\script.ps1 -HostIP example.com`
# i had this without color, running for a year
# but i want to be able to see "how bad"
# the network is at a glance from far away.

param(
    [string]$HostIP = "8.8.8.8"
)

$lastTTL = $null
$failureCount = 0
$lastColor = $null

function Write-ColoredOutput {
    param($Text, $Color)
    Write-Host $Text -ForegroundColor $Color
}

Write-Output "Testing: $HostIP"
Write-Output "type 'continue' after hitting ctrl-break"

cmd /c "ping $HostIP -t" | ForEach-Object {
    if ($_ -match "time=(\d+ms).*TTL=(\d+)") {
        $lastTTL = $matches[2]
        $output = "PASS | $($matches[1]) `t| TTL=$lastTTL"
        
        # Determine color for PASS line
        if ($lastColor -in @('Red', 'DarkYellow') -or $lastColor -eq $null) {
            $color = 'DarkYellow'  # Orange
            $lastColor = 'Green'
        } else {
            $color = 'Green'
        }
        
        Write-ColoredOutput $output $color
        if ($lastColor -ne 'Green') {
            $lastColor = $color
        }
        $failureCount = 0
    }
    elseif ($_ -match "Request timed out.") {
        $failureCount++
        if ($lastTTL) {
            $output = "FAIL |`t`t| TTL=$lastTTL"
        } else {
            $output = "FAIL |`t`t| TTL=unknown"
        }
        
        # Determine color based on failure count
        if ($failureCount -ge 3) {
            $color = 'Red'
        } elseif ($failureCount -ge 2) {
            $color = 'DarkYellow'  # Orange
        } else {
            $color = 'DarkYellow'  # Orange for first failure as well
        }
        
        Write-ColoredOutput $output $color
        $lastColor = $color
    }
    else {
        Write-Host $_  # Default color for other output
    }
}
