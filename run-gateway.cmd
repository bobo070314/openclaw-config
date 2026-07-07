@echo off
chcp 65001 >nul
title OpenClaw-Foreign-Independent

REM === 彻底独立：自己加载 .env，清除 QClaw PATH ===
set PATH=D:\Program Files\nodejs;%SystemRoot%\system32;%SystemRoot%
set NODE_OPTIONS=

REM === 加载 .env（OpenClaw 也会自动加载，但确保 cmd 也有） ===
for /f "tokens=1,2 delims==" %%a in (D:\bobo\openclaw-foreign\.env) do (
    if not "%%a"=="" if not "%%a"=="#%" set "%%a=%%b"
)

powershell -NoProfile -ExecutionPolicy Bypass -File "D:\bobo\openclaw-foreign\scripts\kill-port.ps1" 18900

if exist "D:\bobo\openclaw-foreign\state\gateway.lock" del /f "D:\bobo\openclaw-foreign\state\gateway.lock" >nul 2>&1

echo [%DATE% %TIME%] Starting OpenClaw Foreign Edition INDEPENDENT
echo Node: 
"D:\Program Files\nodejs\node.exe" --version

"D:\Program Files\nodejs\node.exe" "D:\bobo\openclaw-foreign\openclaw\openclaw.mjs" gateway --port 18900

echo [%DATE% %TIME%] Gateway exited with code %ERRORLEVEL%
pause