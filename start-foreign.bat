@echo off
setlocal enabledelayedexpansion
echo ========================================
echo   OpenClaw Foreign Edition (Port 18791)
echo ========================================
echo.

REM Kill old process on 18791
for /f "tokens=5" %%a in ('netstat -ano ^| findstr "18791.*LISTENING"') do (
    echo Killing old process %%a...
    taskkill /PID %%a /F >nul 2>&1
)
timeout /t 2 /nobreak >nul

echo Starting Gateway on port 18791...
start "OpenClaw-Foreign" /min "D:\bobo\openclaw-foreign\run-gateway.cmd"

echo Waiting for Gateway to be ready...
set READY=0
for /l %%i in (1,1,30) do (
    timeout /t 1 /nobreak >nul
    powershell -Command "try{Invoke-WebRequest -Uri 'http://127.0.0.1:18791' -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop|Out-Null;exit 0}catch{exit 1}" 2>nul
    if !errorlevel! equ 0 (
        set READY=1
        goto :ready
    )
    echo    attempt %%i...
)

:ready
if !READY! equ 1 (
    echo Gateway ready^^! Opening browser...
) else (
    echo Gateway not ready after 30s. Opening browser anyway...
)
start http://127.0.0.1:18791

echo.
echo Done! Gateway running on port 18791.
echo To stop: close the "OpenClaw-Foreign" window.
echo.
pause
