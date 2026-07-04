@echo off
cd /d D:\bobo\openclaw-foreign\workspace\infrastructure
set HTTP_PROXY=
set HTTPS_PROXY=
npm install -g openclaw --registry=https://registry.npmmirror.com
echo.
echo 安装完成，验证路径：
where openclaw
pause
