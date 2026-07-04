param()

$config = 'D:\bobo\openclaw-foreign\openclaw-minimal.json'
$env:OPENCLAW_CONFIG_PATH = $config
$log = "D:\bobo\openclaw-foreign\scout-log.txt"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
    $result = echo "爬GitHub CVE最新列表+Spring Boot公告，评优先级≥8分推CEO" | openclaw agent --agent scout --message "-" --session-key "auto:scout:$(Get-Date -Format 'yyyyMMddHHmm')" 2>&1
    "$timestamp | OK | $result" | Out-File -FilePath $log -Append -Encoding utf8
} catch {
    "$timestamp | FAIL | $($_.Exception.Message)" | Out-File -FilePath $log -Append -Encoding utf8
}
