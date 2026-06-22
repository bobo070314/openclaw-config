@echo off
REM agent-testing v0.2.0 — delegates to Python
set PYTHONIOENCODING=utf-8
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%agent_test.py" %*
exit /b %ERRORLEVEL%
