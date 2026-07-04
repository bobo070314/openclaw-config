@echo off
REM IGP v3 全部门压测
cd /d D:\bobo\openclaw-foreign\workspace\family-corp-teams\upgrade-v3
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
python igp_engine_v3_bridge.py --stress
