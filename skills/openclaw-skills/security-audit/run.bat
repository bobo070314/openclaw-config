@echo off
REM security-audit v0.2.0 — delegates to Python
set PYTHONIOENCODING=utf-8
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%security_audit.py" %*
exit /b %ERRORLEVEL%
