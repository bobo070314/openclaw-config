@echo off
chcp 65001 >nul 2>&1
pushd "D:\bobo\openclaw-foreign"

echo ==========
echo   OpenClaw Foreign (Port 18900) - COMPLETELY ISOLATED
echo ==========
echo.

REM Clear all QClaw environment variables
set "QCLAW_LLM_BASE_URL="
set "QCLAW_LLM_API_KEY="
set "QCLAW_BUNDLED_CONFIG_DIR="
set "QCLAW_PLUGIN_CONFIG_PATH="
set "QCLAW_DEVICE_ID="
set "QCLAW_USER_ID="
set "QCLAW_USER_DATA_DIR="
set "QCLAW_WECHAT_WS_URL="

REM Force OpenClaw Foreign config (use minimal config to avoid plugin issues)
set "OPENCLAW_CONFIG_PATH=D:\bobo\openclaw-foreign\openclaw-minimal.json"
set "OPENCLAW_STATE_DIR=D:\bobo\openclaw-foreign\state"

REM Kill old processes
powershell -NoProfile -Command "Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object { $_.Path -like '*openclaw*' } | Stop-Process -Force"
powershell -NoProfile -Command "Start-Sleep -Seconds 2"

if exist "state\gateway.lock" del /f "state\gateway.lock" >nul 2>&1

echo Done.

REM Check port
netstat -ano | findstr ":18900 " >nul 2>&1
if %errorlevel% equ 0 (
    echo ERROR: Port 18900 is already in use.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Start gateway in new window (stays running after this bat exits)
start "OpenClaw-Foreign" /min cmd /k "cd /d D:\bobo\openclaw-foreign && set OPENCLAW_CONFIG_PATH=D:\bobo\openclaw-foreign\openclaw-minimal.json && set OPENCLAW_STATE_DIR=D:\bobo\openclaw-foreign\state && node.exe openclaw\openclaw.mjs gateway --port 18900"

REM Wait a moment then check if started
echo Waiting for gateway to start...
powershell -NoProfile -Command "Start-Sleep -Seconds 5"

netstat -ano | findstr ":18900 " >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo Gateway is running on port 18900.
    echo This window will close.
    timeout /t 3 >nul
    exit /b 0
) else (
    echo.
    echo ERROR: Gateway failed to start.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)
