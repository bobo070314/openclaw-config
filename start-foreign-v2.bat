@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo ========================================
echo   OpenClaw Foreign Edition (Port 18900)
echo ========================================
echo.

set "OPENCLAW_CONFIG_PATH=D:\bobo\openclaw-foreign\openclaw.json"
set "OPENCLAW_STATE_DIR=D:\bobo\openclaw-foreign\state"
set "QCLAW_LLM_BASE_URL="
set "QCLAW_LLM_API_KEY="

powershell -NoProfile -Command "Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like '*openclaw-foreign*'} | Stop-Process -Force"
timeout /t 2 /nobreak >nul

if exist "D:\bobo\openclaw-foreign\state\gateway.lock" del /f "D:\bobo\openclaw-foreign\state\gateway.lock" >nul 2>&1

echo.
echo Starting Gateway on port 18900...

start "OpenClaw-Foreign-Gateway" /min cmd /c "cd /d D:\bobo\openclaw-foreign && set OPENCLAW_CONFIG_PATH=D:\bobo\openclaw-foreign\openclaw.json && set OPENCLAW_STATE_DIR=D:\bobo\openclaw-foreign\state && ""D:\Program Files\nodejs\node.exe"" ""D:\bobo\openclaw-foreign\openclaw\openclaw.mjs"" gateway --port 18900"

echo Waiting for Gateway...
set READY=0
for /l %%i in (1,1,30) do (
    timeout /t 1 /nobreak >nul
    powershell -NoProfile -Command "try { Invoke-WebRequest -Uri 'http://127.0.0.1:18900' -TimeoutSec 2 -UseBasicParsing | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
    if !errorlevel! equ 0 (
        set READY=1
        echo    Ready on attempt %%i!
        goto :ready
    )
)

:ready
if !READY! equ 1 (
    echo Gateway ready! Opening WebChat...
    start http://127.0.0.1:18900/webchat?token=foreign18900
) else (
    echo Gateway failed to start!
    echo.
    echo Please check the "OpenClaw-Foreign-Gateway" window for errors.
    pause
    exit /b 1
)

echo.
echo Done! Gateway running on port 18900.
echo.
pause
