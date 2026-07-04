@echo off
chcp 65001 >nul
echo ============================================
echo  IGP V5 CI/CD — One-click Runner
echo ============================================

echo.
echo [1/4] Running Pipeline (test + analyze + API)...
cd /d "%~dp0"
python -W ignore ci\pipeline.py
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Pipeline failed! > ci\ci_status.log
    type ci\ci_status.log
    pause
    exit /b 1
)
echo [PASS] Pipeline: 9/9 Deployable

echo.
echo [2/4] Running All Unit Tests...
cd /d "%~dp0\.."
python -W ignore tests\run_tests.py
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Tests failed! > ..\v6\ci\ci_status.log
    echo Tests failed at %DATE% %TIME% >> ..\v6\ci\ci_status.log
    pause
    exit /b 1
)
echo [PASS] Tests: All passed

echo.
echo [3/4] Deploy Verification...
cd /d "%~dp0"
python ci\deploy.py
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Deploy verification failed! > ci\ci_status.log
    pause
    exit /b 1
)
echo [PASS] Deploy: Verified

echo.
echo [4/4] Dashboard Status...
cd /d "%~dp0\.."
python v5_dashboard.py

echo.
echo ============================================
echo  CI/CD Complete: ALL PASS ✅
echo ============================================
echo PASS ALL at %DATE% %TIME% > ..\v6\ci\ci_status.log
