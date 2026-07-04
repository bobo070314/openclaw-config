@echo off
cd /d D:\bobo\openclaw-foreign
set HTTP_PROXY=
set HTTPS_PROXY=
npm install -g openclaw --registry=https://registry.npmmirror.com
where openclaw > openclaw-path.txt
echo 安装完成，路径已保存到 openclaw-path.txt
pause
