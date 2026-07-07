<#
.SYNOPSIS
  IGP API 8080 自动重启脚本 — 检测端口挂了就自动拉起
#>

$apiPort = 8080
$apiScript = "D:\bobo\openclaw-foreign\family-corp-teams\v5\v6\api\igp_api.py"
$logDir = "D:\bobo\openclaw-foreign\logs"
$logFile = "$logDir\igp_restart_$(Get-Date -Format 'yyyyMMdd').log"

# 确保日志目录存在
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }

$timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

# 1. 先尝试 HTTP 健康检查
$healthy = $false
try {
    $r = Invoke-RestMethod -Uri "http://localhost:$apiPort/api/v1/health" -TimeoutSec 3 -ErrorAction Stop
    if ($r.status -eq "ok") { $healthy = $true }
} catch {}

if (-not $healthy) {
    # 2. 再查端口
    $portCheck = netstat -ano | Select-String ":$apiPort\s"
    if (-not $portCheck) {
        "[$timestamp] ⚠️ IGP API $apiPort 未响应 + 端口未监听，触发自动重启..." | Out-File -Append -FilePath $logFile

        # 杀掉残留 Python 进程（仅 igp_api 相关）
        Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*igp_api*' } | Stop-Process -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2

        # 启动 IGP API
        $env:PYTHONIOENCODING = 'utf-8'
        $env:PYTHONUTF8 = '1'
        $psi = New-Object System.Diagnostics.ProcessStartInfo
        $psi.FileName = "python"
        $psi.Arguments = "-W ignore -u `"$apiScript`" --port $apiPort"
        $psi.WorkingDirectory = "D:\bobo\openclaw-foreign"
        $psi.RedirectStandardOutput = $true
        $psi.RedirectStandardError = $true
        $psi.UseShellExecute = $false
        $psi.CreateNoWindow = $true
        $psi.EnvironmentVariables["PYTHONIOENCODING"] = "utf-8"
        $psi.EnvironmentVariables["PYTHONUTF8"] = "1"
        $p = [System.Diagnostics.Process]::Start($psi)

        "[$timestamp] ✅ IGP API 重启命令已执行 (PID: $($p.Id))" | Out-File -Append -FilePath $logFile

        # 等待 10 秒后检查
        Start-Sleep -Seconds 10
        try {
            $r2 = Invoke-RestMethod -Uri "http://localhost:$apiPort/api/v1/health" -TimeoutSec 3 -ErrorAction Stop
            if ($r2.status -eq "ok") {
                "[$timestamp] ✅ IGP API 已恢复健康 (PID: $($p.Id))" | Out-File -Append -FilePath $logFile
            } else {
                "[$timestamp] ❌ IGP API 已启动但状态异常: $($r2 | ConvertTo-Json -Compress)" | Out-File -Append -FilePath $logFile
            }
        } catch {
            "[$timestamp] ❌ IGP API 重启失败，需人工介入" | Out-File -Append -FilePath $logFile
        }
    } else {
        "[$timestamp] ⚠️ IGP API 端口 $apiPort 在监听但健康检查失败，服务可能卡死，跳过自动重启" | Out-File -Append -FilePath $logFile
    }
}
# IGP 正常，静默退出
