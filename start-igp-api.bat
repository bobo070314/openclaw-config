@echo off
REM 延迟 30 秒启动，避免刚开机抢资源
timeout /t 30 /nobreak >nul

pushd "D:\bobo\openclaw-foreign"

set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

REM 确保 logs 目录存在
if not exist "logs" mkdir "logs"

REM 启动 IGP API 服务，日志按日期存储
REM L8: Auto retry up to 3 times
set retry_count=0
:RETRY_IGP
set /a retry_count+=1
if %retry_count% gtr 3 (
    echo [%date% %time%] IGP API failed after 3 retries >> "logs\igp_startup.log"
    exit /b 1
)

python -W ignore -u "family-corp-teams\v5\v6\api\igp_api.py" --port 8080 >> "logs\igp_api_%date:~0,4%%date:~5,2%%date:~8,2%.log" 2>&1

REM Check if it stayed alive
powershell -NoProfile -Command "Start-Sleep -Seconds 5"
netsh http show servicestate 2>nul | findstr ":8080 " >nul 2>&1
if errorlevel 1 (
    echo [%date% %time%] Retry %retry_count%/3: IGP API failed to start >> "logs\igp_startup.log"
    timeout /t 10 /nobreak >nul
    goto RETRY_IGP
)
