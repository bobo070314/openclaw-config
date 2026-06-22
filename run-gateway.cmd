@echo off
REM === OpenClaw International (port 18791) ===
REM Direct Node launch ? bypasses QClaw wrappers
set OPENCLAW_STATE_DIR=D:\bobo\openclaw-foreign
set OPENCLAW_CONFIG_PATH=D:\bobo\openclaw-foreign\openclaw.json

REM Kill any existing process on 18791
for /f "tokens=5" %%a in ('netstat -ano ^| findstr "18791.*LISTENING"') do taskkill /PID %%a /F >nul 2>&1
timeout /t 2 /nobreak >nul

REM Clear stale lock
del /f "D:\bobo\openclaw-foreign\state\gateway.lock" 2>nul

node "C:\Users\asus\AppData\Roaming\npm\node_modules\openclaw\openclaw.mjs" gateway --port 18791
