<#
.SYNOPSIS
  Gateway 18789 自动重启脚本 — 检测端口挂了就自动拉起
#>

$gwPort = 18789
$batPath = "D:\bobo\openclaw-foreign\start-foreign.bat"
$logDir = "D:\bobo\openclaw-foreign\logs"
$logFile = "$logDir\gateway_restart_$(Get-Date -Format 'yyyyMMdd').log"

# 确保日志目录存在
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }

$timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

# 检查 Gateway 端口
$portCheck = netstat -ano | Select-String ":$gwPort\s"
if (-not $portCheck) {
    "[$timestamp] ⚠️ Gateway $gwPort 未运行，触发自动重启..." | Out-File -Append -FilePath $logFile

    # 杀掉残留 node 进程
    Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object { $_.Path -like '*openclaw*' } | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2

    # 启动网关
    Start-Process -FilePath $batPath -WindowStyle Hidden
    "[$timestamp] ✅ Gateway 重启命令已执行 (start-foreign.bat)" | Out-File -Append -FilePath $logFile

    # 等待 10 秒后检查是否成功
    Start-Sleep -Seconds 10
    $retry = netstat -ano | Select-String ":$gwPort\s"
    if ($retry) {
        "[$timestamp] ✅ Gateway $gwPort 已恢复 LISTENING" | Out-File -Append -FilePath $logFile
    } else {
        "[$timestamp] ❌ Gateway $gwPort 重启失败，需人工介入" | Out-File -Append -FilePath $logFile
    }
} else {
    # Gateway 正常运行，静默退出
}
