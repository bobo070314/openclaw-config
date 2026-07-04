#!/usr/bin/env python3
"""IGP V5 一键全景启动 —— 每日循环 + 竞技场 + 扫描 + 检查"""
import os, sys, subprocess, json
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("🏭 六步循环引擎",      "v5_engine_loop.py",       "循环引擎"),
    ("🏟️ 每日淘汰赛场",     "v5_pk_arena.py",           "竞技场"),
    ("🔭 GitHub Scanner",   "v5_github_scanner.py",     "扫描仪"),
    ("🔌 外接API检查",      "deploy/api_live_check.py", "API检查"),
    ("📦 Skills注册表",     "v5_skills_registry.py",    "注册表"),
    ("🦴 GHOST自愈巡逻",    "v5_ghost_patrol.py",       "巡逻队"),
]

def run_checkpoint(name, script, label):
    fp = os.path.join(BASE, script)
    if not os.path.exists(fp):
        return {'name': name, 'status': '❌', 'detail': '文件缺失'}
    try:
        r = subprocess.run([sys.executable, fp], capture_output=True, text=True, timeout=120, encoding='utf-8',
                          cwd=os.path.dirname(fp))
        last_lines = [l for l in r.stdout.split('\n') if '✅' in l or '❌' in l or '失败' in l or '健康' in l]
        detail = last_lines[-1][:80] if last_lines else f'rc={r.returncode}'
        return {
            'name': name,
            'status': '✅' if r.returncode == 0 else '❌',
            'detail': detail,
            'rc': r.returncode,
        }
    except subprocess.TimeoutExpired:
        return {'name': name, 'status': '⏳', 'detail': '超时(>120s)'}
    except Exception as e:
        return {'name': name, 'status': '❌', 'detail': str(e)[:60]}

print('🔥' * 35)
print(f'  IGP V5 一键全景启动 — {datetime.now(timezone.utc).isoformat()}')
print('🔥' * 35)

results = []
for name, script, label in STEPS:
    print(f'  ▶ {name}...', end=' ', flush=True)
    r = run_checkpoint(name, script, label)
    results.append(r)
    print(f'{r["status"]}  {r["detail"]}')

print(f'\n{"="*50}')
print('  📊 全景摘要')
print(f'{"="*50}')
ok = sum(1 for r in results if r['status'] == '✅')
total = len(results)
for r in results:
    print(f'  {r["status"]} {r["name"]:20s} {r["detail"]}')
print(f'  {"—"*40}')
print(f'  {ok}/{total} 通过')

if ok == total:
    print(f'\n  🎉 V5全链路就绪！')
    print(f'  8染色体 | 38模块 | 六步循环 | 淘汰赛 | GitHub扫描 | Skills注册\n')
print('🔥' * 35)
