@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

echo ========================================
echo   OpenClaw Task Installer
echo ========================================
echo.

set SCRIPTS=D:\bobo\openclaw-foreign\scripts

echo [1/6] Gateway AutoStart...
schtasks /create /tn "OpenClaw\Gateway AutoStart" /xml "%SCRIPTS%\task-gateway-autostart.xml" /f
if %errorlevel% equ 0 ( echo   [OK] ) else ( echo   [FAIL] )

echo [2/6] IGP API AutoStart...
schtasks /create /tn "OpenClaw\IGP API AutoStart" /xml "%SCRIPTS%\task-igp-api-autostart.xml" /f
if %errorlevel% equ 0 ( echo   [OK] ) else ( echo   [FAIL] )

echo [3/6] Heartbeat Morning (09:00)...
schtasks /create /tn "OpenClaw\Heartbeat Morning" /xml "%SCRIPTS%\task-heartbeat-morning.xml" /f
if %errorlevel% equ 0 ( echo   [OK] ) else ( echo   [FAIL] )

echo [4/6] Heartbeat Afternoon (13:00)...
schtasks /create /tn "OpenClaw\Heartbeat Afternoon" /xml "%SCRIPTS%\task-heartbeat-afternoon.xml" /f
if %errorlevel% equ 0 ( echo   [OK] ) else ( echo   [FAIL] )

echo [5/6] Heartbeat Evening (19:00)...
schtasks /create /tn "OpenClaw\Heartbeat Evening" /xml "%SCRIPTS%\task-heartbeat-evening.xml" /f
if %errorlevel% equ 0 ( echo   [OK] ) else ( echo   [FAIL] )

echo [6/6] Heartbeat Night (23:00)...
schtasks /create /tn "OpenClaw\Heartbeat Night" /xml "%SCRIPTS%\task-heartbeat-night.xml" /f
if %errorlevel% equ 0 ( echo   [OK] ) else ( echo   [FAIL] )

echo.
echo ========================================
echo   Done! Check Task Scheduler for results.
echo ========================================
pause
