@echo off
chcp 437 >nul
echo ===========================================
echo   Disable qclaw-llm-provider plugin
echo ===========================================
echo.
echo Target: C:\Program Files\QClaw\v0.2.29.592\resources\openclaw\config\extensions\qclaw-llm-provider
echo Action: Rename to qclaw-llm-provider.DISABLED
echo.
echo If UAC window appears, click YES

cd /d "C:\Program Files\QClaw\v0.2.29.592\resources\openclaw\config\extensions"

if not exist "qclaw-llm-provider" (
    echo [OK] qclaw-llm-provider already gone
    pause
    exit /b 0
)

if exist "qclaw-llm-provider.DISABLED" (
    echo [OK] qclaw-llm-provider.DISABLED already exists - no action needed
    pause
    exit /b 0
)

ren "qclaw-llm-provider" "qclaw-llm-provider.DISABLED"
if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUCCESS] qclaw-llm-provider has been DISABLED!
    echo Now you can double-click start-foreign.bat to launch.
) else (
    echo.
    echo [FAILED] Permission denied. Right-click this file - Run as Administrator.
)

pause
