@echo off
REM frontend-code-review v0.2.0 — delegates to Python
set PYTHONIOENCODING=utf-8
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%code_review.py" %*
exit /b %ERRORLEVEL%
