@echo off
REM add-setting-env v0.2.0 — delegates to Python
set PYTHONIOENCODING=utf-8
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%env_validator.py" %*
exit /b %ERRORLEVEL%
