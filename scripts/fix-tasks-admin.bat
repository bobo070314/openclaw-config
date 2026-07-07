@echo off
chcp 65001 2>&1 | Out-Null
title OpenClaw 定时任务修复 — 管理员执行

echo ============================================
echo  OpenClaw Task Scheduler Fix
echo  需要管理员权限才能更新 Task Scheduler
echo ============================================
echo.
echo 请右键以"管理员身份运行"此脚本
echo.
pause

set SCRIPTS=%~dp0

echo [1/2] 删除旧任务...
schtasks /delete /tn "OpenClaw\Gateway AutoStart" /f
schtasks /delete /tn "OpenClaw\IGP API AutoStart" /f
schtasks /delete /tn "OpenClaw\Heartbeat Morning" /f
schtasks /delete /tn "OpenClaw\Heartbeat Afternoon" /f
schtasks /delete /tn "OpenClaw\Heartbeat Evening" /f
schtasks /delete /tn "OpenClaw\Heartbeat Night" /f
echo 旧任务已删除

echo.
echo [2/2] 注册新任务（LogonType 已修复）...
schtasks /create /tn "OpenClaw\Gateway AutoStart" /xml "%SCRIPTS%\task-gateway-autostart.xml" /f
schtasks /create /tn "OpenClaw\IGP API AutoStart" /xml "%SCRIPTS%\task-igp-api-autostart.xml" /f
schtasks /create /tn "OpenClaw\Heartbeat Morning" /xml "%SCRIPTS%\task-heartbeat-morning.xml" /f
schtasks /create /tn "OpenClaw\Heartbeat Afternoon" /xml "%SCRIPTS%\task-heartbeat-afternoon.xml" /f
schtasks /create /tn "OpenClaw\Heartbeat Evening" /xml "%SCRIPTS%\task-heartbeat-evening.xml" /f
schtasks /create /tn "OpenClaw\Heartbeat Night" /xml "%SCRIPTS%\task-heartbeat-night.xml" /f

echo.
echo ====== 验证 ======
schtasks /query /fo LIST | findstr "OpenClaw"
echo.
echo 完成！6 个任务全部修复
pause
