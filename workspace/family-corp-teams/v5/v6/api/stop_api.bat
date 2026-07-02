@echo off
REM IGP API 常驻 — 停止
echo Stopping IGP API Server...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8080 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
    echo Killed PID %%a
)
echo IGP API stopped.
