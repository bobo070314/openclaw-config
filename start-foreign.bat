@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo ========================================
echo   OpenClaw Foreign Edition (Port 18900)
echo ========================================
echo.

REM ── Verify environment variables ──
if "%OPENCLAW_DASHSCOPE_KEY%"=="" (
    echo [WARN] OPENCLAW_DASHSCOPE_KEY is not set
)
if "%OPENCLAW_SILICONFLOW_KEY%"=="" (
    echo [WARN] OPENCLAW_SILICONFLOW_KEY is not set
)

echo.

REM ── Kill any existing process on 18900 (locale-safe) ──
echo Checking port 18900...
powershell -Command ^
    "$proc = netstat -ano | Select-String ':18900.*LISTENING';" ^
    "if ($proc) { $pid = ($proc -split '\s+')[4];" ^
    "  Write-Host ('Killing old PID: ' + $pid);" ^
    "  Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue;" ^
    "  Start-Sleep -Seconds 2;" ^
    "  Write-Host 'Done.' } else { Write-Host 'Port 18900 is free.' }"

REM ── Clear stale lock files ──
del /f "D:\bobo\openclaw-foreign\state\gateway.lock" 2>nul

echo.
echo Starting Gateway on port 18900...
start "OpenClaw-Foreign" /min "D:\bobo\openclaw-foreign\run-gateway.cmd"

REM ── Wait for Gateway readiness ──
echo Waiting for Gateway to be ready...
set READY=0
for /l %%i in (1,1,30) do (
    timeout /t 1 /nobreak >nul
    powershell -NoProfile -Command ^
        "try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:18900/api/health' -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop; if ($r.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" 2>nul
    if !errorlevel! equ 0 (
        set READY=1
        echo    Gateway ready on attempt %%i!
        goto :ready
    )
    echo    attempt %%i...
)

REM Fallback: try root endpoint
if !READY! equ 0 (
    powershell -NoProfile -Command ^
        "try { Invoke-WebRequest -Uri 'http://127.0.0.1:18900' -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop; exit 0 } catch { exit 1 }" 2>nul
    if !errorlevel! equ 0 set READY=1
)

:ready
if !READY! equ 1 (
    echo Gateway ready^^! Opening browser...
) else (
    echo Gateway not ready after all attempts. Opening browser anyway...
)
start http://127.0.0.1:18900

echo.
echo Done! Gateway running on port 18900.
echo To stop: close the "OpenClaw-Foreign" window.
echo.

REM ── Print gbrain status ──
if exist "D:\bobo\openclaw-foreign\skills\gbrain\mcp-server.js" (
    echo [gbrain] MCP server registered ^(skills/gbrain/mcp-server.js^)
) else (
    echo [gbrain] MCP server not found
)

pause
