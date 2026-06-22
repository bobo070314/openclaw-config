@echo off
REM db-migrations v0.2.0 — delegates to Python
set PYTHONIOENCODING=utf-8
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%db_migrate.py" %*
exit /b %ERRORLEVEL%
