<#
.SYNOPSIS 日志轮转（L7），保留最近 7 天日志
#>

$logDir   = "D:\bobo\openclaw-foreign\logs"
$retention = 7
$rotateLog = "$logDir\rotate_$(Get-Date -Format 'yyyyMMdd').log"
$ts = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

function Log($m) { "$ts $m" | Out-File -Append -FilePath $rotateLog -Encoding Default }

try {
    $cut = (Get-Date).AddDays(-$retention)
    $cleaned = 0
    $errors = 0

    Get-ChildItem $logDir -Filter "*.log" | ForEach-Object {
        if ($_.LastWriteTime -lt $cut) {
            try {
                Remove-Item -Path $_.FullName -Force
                Log "Remove $($_.Name)"
                $cleaned++
            } catch {
                Log "ERROR $($_.Name): $($_.Exception.Message)"
                $errors++
            }
        }
    }

    Log "Done: cleaned=$cleaned errors=$errors"
    exit 0
} catch {
    Log "Exception: $($_.Exception.Message)"
    exit 1
}
