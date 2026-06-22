@echo off
REM create-skill v0.2.0 — Skill Factory with Context Snapshot
REM Delegates to Python for cross-platform + rg-like workspace scanning
set PYTHONIOENCODING=utf-8

REM Get this file's directory to locate create_skill.py
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%create_skill.py" %*
exit /b %ERRORLEVEL%
