@echo off
chcp 65001 >nul
title OpenClaw-Foreign

REM === OpenClaw International (port 18900) ===
set OPENCLAW_STATE_DIR=D:\bobo\openclaw-foreign
set OPENCLAW_CONFIG_PATH=D:\bobo\openclaw-foreign\openclaw.json

REM Kill any existing process on 18900 (locale-safe)
powershell -NoProfile -Command ^
    "$proc = netstat -ano | Select-String ':18900.*LISTENING';" ^
    "if ($proc) { Stop-Process -Id (($proc -split '\s+')[4]) -Force -ErrorAction SilentlyContinue; Start-Sleep 2 }"

REM Clear stale lock
del /f "D:\bobo\openclaw-foreign\state\gateway.lock" 2>nul

REM Launch OpenClaw Gateway
echo [%DATE% %TIME%] Starting OpenClaw Foreign Edition on port 18900...
"node" "C:\Users\asus\AppData\Roaming\npm\node_modules\openclaw\openclaw.mjs" gateway --port 18900

echo [%DATE% %TIME%] Gateway exited with code %ERRORLEVEL%
pause
