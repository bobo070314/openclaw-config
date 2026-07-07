@echo off
setlocal
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
set "_params="
set "_args=%*"
if not defined _args exit /b 1
python "%~1" %2 %3 %4 %5 %6 %7 %8 %9
endlocal
