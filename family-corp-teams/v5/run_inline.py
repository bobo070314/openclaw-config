"""IGP Inline Runner — 内联脚本转发器
用法: python run_inline.py <命令名> [args...]
支持的快捷命令:
  pipeline          CI/CD pipeline
  deploy            一键部署
  test              跑全部单元测试
  health            API健康检查
  hr                生成HR报告
  dashboard         显示IGP状态面板
  scan_registry     扫描产品注册表
"""
from __future__ import annotations
import sys
import os
import json
import urllib.request

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'

def cmd_pipeline():
    os.system(f'{sys.executable} -W ignore "{V5}/v6/ci/pipeline.py"')

def cmd_deploy():
    os.system(f'{sys.executable} -W ignore "{V5}/v6/ci/deploy.py"')

def cmd_test():
    os.system(f'{sys.executable} -W ignore "{V5}/tests/run_tests.py"')

def cmd_health():
    try:
        r = urllib.request.urlopen('http://localhost:8080/api/v1/health', timeout=3)
        d = json.loads(r.read())
        print(f"API: {d['status']}")
    except Exception as e:
        print(f"API health check failed: {e}")

def cmd_hr():
    os.system(f'{sys.executable} -W ignore "{V5}/v6/hr/generate_report.py"')

def cmd_dashboard():
    os.system(f'{sys.executable} -W ignore "{V5}/v5_dashboard.py"')

def cmd_scan_registry():
    os.system(f'{sys.executable} -W ignore "{V5}/v6/scan_registry.py"')

CMDS = {
    'pipeline': cmd_pipeline,
    'deploy': cmd_deploy,
    'test': cmd_test,
    'health': cmd_health,
    'hr': cmd_hr,
    'dashboard': cmd_dashboard,
    'scan_registry': cmd_scan_registry,
}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: python run_inline.py <command>")
        print(f"Commands: {', '.join(sorted(CMDS))}")
        sys.exit(1)
    
    name = sys.argv[1].lower()
    if name not in CMDS:
        print(f"Unknown command: {name}")
        print(f"Available: {', '.join(sorted(CMDS))}")
        sys.exit(1)
    
    CMDS[name]()
