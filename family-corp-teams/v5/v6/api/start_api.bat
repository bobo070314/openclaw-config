@echo off
REM IGP API 常驻 — 启动
REM 这个脚本可以放在桌面、启动文件夹或任何地方
echo Starting IGP API Server...
start /b cmd /c "python -W ignore -u D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\api\igp_api.py --port 8080"
timeout /t 3 /nobreak >nul
echo Checking health...
python -c "import json,urllib.request; r=urllib.request.urlopen('http://localhost:8080/api/v1/health',timeout=3); print(json.loads(r.read())['status'])"
echo.
echo IGP API is running at http://localhost:8080
echo Stop with: stop_api.bat
