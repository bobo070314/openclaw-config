@echo off
setlocal enabledelayedexpansion

:: ============================================
:: 国际版 OpenClaw 启动脚本（修复自杀循环版）
:: 逻辑：先杀旧进程 → 等端口空闲 → 启动新 Gateway → 等就绪 → 开浏览器
:: ============================================

:: 1. 杀掉所有占用 18791 端口的旧进程
echo Killing old Gateway processes on port 18791...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :18791') do (
    echo   Killing PID %%a...
    taskkill /PID %%a /F >nul 2>&1
)

:: 2. 等待端口完全空闲（最多等 10 秒）
echo Waiting for port 18791 to be free...
for /l %%i in (1,1,20) do (
    netstat -ano | findstr :18791 >nul
    if errorlevel 1 (
        echo   Port 18791 is free after %%i seconds
        goto PORT_FREE
    )
    timeout /t 1 /nobreak >nul
)
echo ERROR: Port 18791 still in use after 20 seconds
pause
exit /b 1

:PORT_FREE
:: 3. 启动 Gateway（后台运行）
echo Starting International OpenClaw Gateway...
start "" /min cmd /c D:\bobo\openclaw-foreign\run-gateway.cmd

:: 4. 等待 Gateway 就绪（轮询 HTTP，最多等 30 秒）
echo Waiting for Gateway to be ready...
for /l %%i in (1,1,30) do (
    powershell -Command "try { Invoke-WebRequest -Uri http://127.0.0.1:18791 -UseBasicParsing -TimeoutSec 1 } catch { exit 1 }" >nul 2>&1
    if not errorlevel 1 (
        echo   Gateway ready after %%i seconds!
        goto GATEWAY_READY
    )
    <nul set /p ".=."
    timeout /t 1 /nobreak >nul
)
echo ERROR: Gateway failed to start within 30 seconds
pause
exit /b 1

:GATEWAY_READY
:: 5. 打开浏览器
echo Opening browser...
start http://127.0.0.1:18791

echo.
echo ============================================
echo International OpenClaw is ready!
echo   Dashboard: http://127.0.0.1:18791
echo   Config: D:\bobo\openclaw-foreign\openclaw.json
echo ============================================
exit /b 0
