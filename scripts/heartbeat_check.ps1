param(
    [string]$TimeLabel = ""
)

# ✅ 硬编码日志路径（绝对不会错）
$logDir = "D:\bobo\openclaw-foreign\logs"
$logPath = "$logDir\heartbeat_$(Get-Date -Format 'yyyyMMdd').log"
$timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

# 标签
$label = if ($TimeLabel) { "[$TimeLabel]" } else { "" }

# 1. 检查 Gateway (18789) —— 端口 + 3 次重试避假阳性
$gwStatus = ""
$gwHealthy = $false
for ($attempt = 0; $attempt -lt 3; $attempt++) {
    $portCheck = netstat -ano | findstr ":18789" | findstr "LISTENING"
    if ($portCheck) {
        $gwHealthy = $true
        break
    }
    Start-Sleep -Seconds 5
}
if ($gwHealthy) {
    $gwStatus = "✅ Gateway OK (Port 18789 Listening)"
} else {
    $gwStatus = "❌ Gateway FAIL (3次重试后端口仍无响应)"
    # L4 故障自愈：确认为真故障才拉重启
    powershell.exe -ExecutionPolicy Bypass -File "D:\bobo\openclaw-foreign\scripts\restart-gateway.ps1" | Out-Null
}

# 2. 检查 IGP API (8080) —— 3 次重试防假阳性
$igpStatus = ""
$igpHealthy = $false
for ($attempt = 0; $attempt -lt 3; $attempt++) {
    try {
        $r = Invoke-RestMethod -Uri "http://127.0.0.1:8080/api/v1/health" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
        $igpHealthy = $true
        break
    } catch {
        Start-Sleep -Seconds 3
    }
}
if ($igpHealthy) {
    $igpStatus = "✅ IGP API OK (Status: ok)"
} else {
    $igpStatus = "❌ IGP API FAIL (3次重试后仍无响应)"
    # L4 故障自愈
    powershell.exe -ExecutionPolicy Bypass -File "D:\bobo\openclaw-foreign\scripts\restart-igp.ps1" | Out-Null
}

# 3. 检查 Lossless DB
$lcmStatus = ""
$lcmDb = "D:\bobo\openclaw-foreign\memory\lossless\lcm.db"
$lcmStatus = if (Test-Path $lcmDb) { 
    $size = (Get-Item $lcmDb).Length
    $sizeStr = if ($size -gt 1MB) { "{0:N1} MB" -f ($size / 1MB) } else { "{0:N1} KB" -f ($size / 1KB) }
    "✅ Lossless DB ($sizeStr)"
} else { 
    "⚠️ Lossless DB not found" 
}

# 4. 写日志（确保目录存在）
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
$line = "[$timestamp] $label Gateway=$gwStatus | IGP=$igpStatus | Memory=$lcmStatus"
Add-Content -Path $logPath -Value $line -Encoding Default

# 晨检分隔线
if ($TimeLabel -eq "晨检") { Add-Content -Path $logPath -Value "----------------------------------------" -Encoding Default }

# L5+L9: 自动备份 Lossless DB + 配置
powershell -ExecutionPolicy Bypass -File "D:\bobo\openclaw-foreign\scripts\backup-lossless-db.ps1" -ErrorAction SilentlyContinue | Out-Null

# L7: 日志轮转
powershell -ExecutionPolicy Bypass -File "D:\bobo\openclaw-foreign\scripts\rotate-logs.ps1" -ErrorAction SilentlyContinue | Out-Null

# L10: 告警通知（有组件 FAIL 时弹 Windows 消息框）
if ($gwStatus -like '*FAIL*' -or $igpStatus -like '*FAIL*' -or $lcmStatus -like '*FAIL*' -or $lcmStatus -like '*not found*') {
    $msgBody = "ALERT: " + $gwStatus + " | " + $igpStatus + " | " + $lcmStatus
    msg * "$msgBody" 2>$null
}

# 控制台输出（GBK编码不显示乱码）
Write-Host "✅ 心跳检测完成，日志已写入：$logPath"
Write-Host $line