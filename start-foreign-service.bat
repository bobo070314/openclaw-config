@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
pushd "D:\bobo\openclaw-foreign"

echo ==========
echo   OpenClaw Foreign (Port 18900) - COMPLETELY ISOLATED
echo ==========
echo.

REM ==========  STEP 1: Clear ALL QClaw environment variables ==========
set "QCLAW_LLM_BASE_URL="
set "QCLAW_LLM_API_KEY="
set "QCLAW_BUNDLED_CONFIG_DIR="
set "QCLAW_PLUGIN_CONFIG_PATH="
set "QCLAW_DEVICE_ID="
set "QCLAW_USER_ID="
set "QCLAW_USER_DATA_DIR="
set "QCLAW_WECHAT_WS_URL="

REM ==========  STEP 2: Force OpenClaw Foreign config ==========
set "OPENCLAW_CONFIG_PATH=D:\bobo\openclaw-foreign\openclaw.json"
set "OPENCLAW_STATE_DIR=D:\bobo\openclaw-foreign\state"

REM ==========  STEP 3: Kill old processes ==========
powershell -NoProfile -Command "Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object { $_.Path -like '*openclaw*' } | Stop-Process -Force"
powershell -NoProfile -Command "Start-Sleep -Seconds 2"

if exist "state\gateway.lock" del /f "state\gateway.lock" >nul 2>&1

echo.
echo STEP 1: Environment cleaned
echo STEP 2: Config set to Foreign config
echo STEP 3: Old processes killed
echo.
echo Starting Gateway...

REM ==========  STEP 4: Start gateway (foreground, blocks until exit) ==========
if not exist "openclaw\openclaw.mjs" (
    echo ERROR: openclaw\openclaw.mjs not found
    popd
    exit /b 1
)

REM Run node directly (not in new window), this will block until gateway exits
node.exe openclaw\openclaw.mjs gateway --port 18900

REM If we get here, gateway has exited
popd
echo Gateway exited with code %errorlevel%
exit /b %errorlevel%
