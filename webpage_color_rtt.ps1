# check-cope.ps1
# hits a url endpoint and color codes if/what/how fast it gets back.
# been meaning to do this as a companion to my colorpings.ps1 script
# icmp may be unreliable, whereas this is essentially "cURL"
$url = "http://example.com" #change to your endpoint
$expectedBytes = "yes`n"    #change to your endpoint's SHORT reply. my endpoint returns 'yes\n'
$expectedLength = 4         #set this to the number of literal bytes you expect each time
$failureCount = 0   
$slowThresholdMs = 200      #200ms+ is bad for games, but you can set this to whatever
$lastWasProblem = $false    # Tracks if previous line was DarkYellow/Red (failure or slow)

Write-Host "Monitoring $url every second. Press Ctrl+C to stop." -ForegroundColor Cyan
Write-Host ""
Write-Host "Legend: Green = fast PASS | DarkYellow = slow PASS, 1st FAIL, or recovery | Red = consecutive FAILS" -ForegroundColor DarkGray
Write-Host ""

while ($true) {
    $startTime = Get-Date
    
    try {
        $response = Invoke-WebRequest -Uri $url -Method Get -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
        $endTime = Get-Date
        $elapsedMs = [math]::Round(($endTime - $startTime).TotalMilliseconds)
        
        $bodyText = $response.Content
        $bytesReceived = [System.Text.Encoding]::UTF8.GetBytes($bodyText)
        $byteCount = $bytesReceived.Length
        
        # Verify content is exactly "yes\n" (4 bytes)
        if ($bodyText -eq $expectedBytes -and $byteCount -eq $expectedLength) {
            # SUCCESS case
            
            if ($lastWasProblem) {
                # Recovery: first success after any problem (failure OR slow) -> DarkYellow
                $color = "DarkYellow"
                $lastWasProblem = $false
                $failureCount = 0
            } else {
                # No recent problem, color by response time
                if ($elapsedMs -gt $slowThresholdMs) {
                    $color = "DarkYellow"  # Slow but successful, becomes a problem state
                    $lastWasProblem = $true
                } else {
                    $color = "Green"   # Fast and successful
                    $lastWasProblem = $false
                }
            }
            
            Write-Host ("PASS | {0,4}ms | {1,2} Bytes" -f $elapsedMs, $byteCount) -ForegroundColor $color
        } else {
            # Wrong content (treat as failure)
            $failureCount++
            $color = if ($failureCount -eq 1) { "DarkYellow" } else { "Red" }
            Write-Host ("FAIL |                   | {0,2} time{1}" -f $failureCount, $(if ($failureCount -eq 1) { "" } else { "s" })) -ForegroundColor $color
            $lastWasProblem = $true
        }
    }
    catch {
        # Network error or timeout
        $failureCount++
        $color = if ($failureCount -eq 1) { "DarkYellow" } else { "Red" }
        Write-Host ("FAIL |                   | {0,2} time{1}" -f $failureCount, $(if ($failureCount -eq 1) { "" } else { "s" })) -ForegroundColor $color
        $lastWasProblem = $true
    }
    
    Start-Sleep -Seconds 1
}
