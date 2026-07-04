@echo off
chcp 65001 >nul
echo ========================================
echo  IGP 研发部 — 一键全链路检测
echo ========================================
echo.

echo [1/5] API 健康检查...
python -W ignore D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\tests\check_health.py
echo.

echo [2/5] 单元测试...
python -W ignore D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\tests\run_tests.py
echo.

echo [3/5] CI/CD Pipeline...
python -W ignore D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\ci\pipeline.py
echo.

echo [4/5] HR 报告生成...
python -W ignore D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\hr\generate_report.py
echo.

echo [5/5] IGP 状态面板...
python -W ignore D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v5_dashboard.py
echo.

echo ========================================
echo  全部检测完成
echo ========================================
pause
