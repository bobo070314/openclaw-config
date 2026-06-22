@echo off
REM code-navigator v0.2.0 — delegates to Python
set PYTHONIOENCODING=utf-8
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%code_navigator.py" %*
exit /b %ERRORLEVEL%
