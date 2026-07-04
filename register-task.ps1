# ============================================
# 注册 OpenClaw 开机自启 Scheduled Task
# 作用：开机自动清理 + 启动网关，解放双手
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  注册 OpenClaw 开机自动启动任务" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$taskName = "OpenClaw Auto Clean Start"
$scriptPath = "D:\bobo\openclaw-foreign\openclaw-clean-start.ps1"

# 删除旧任务（如果有）
Write-Host "🗑️ 删除旧任务（如有）..." -ForegroundColor Yellow
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
Write-Host "  ✅ 旧任务已删除" -ForegroundColor Green

# 创建新任务
Write-Host "🔧 创建新任务..." -ForegroundColor Yellow
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Force

Write-Host "  ✅ 任务已注册: $taskName" -ForegroundColor Green
Write-Host ""
Write-Host "📋 任务详情:" -ForegroundColor Cyan
Get-ScheduledTask -TaskName $taskName | Format-List TaskName, State, TaskPath

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ 注册完成！重启后自动清理+启动网关" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
