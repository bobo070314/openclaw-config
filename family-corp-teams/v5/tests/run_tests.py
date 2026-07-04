"""IGP 测试运行器 v5 — 每个测试文件用subprocess隔离跑"""
from __future__ import annotations
import os
import subprocess
import sys
import time

test_dir = os.path.dirname(os.path.abspath(__file__))
test_files = sorted(f for f in os.listdir(test_dir)
                    if f.startswith('test_') and f.endswith('.py')
                    and f != 'debug_loader.py')

print(f"Found {len(test_files)} test files:\n")
print(f"{'Test':35} {'Result':8} {'Passed':8} {'Time':8}")
print('-' * 59)

results = []
for tf in test_files:
    path = os.path.join(test_dir, tf)
    start = time.time()
    
    r = subprocess.run(
        [sys.executable, '-W', 'ignore', '-u', path],
        capture_output=True, timeout=30, text=True, encoding='utf-8'
    )
    
    elapsed = time.time() - start
    
    out = r.stdout or ''
    err = (r.stderr or '')[:100].strip()
    
    ok = r.returncode == 0
    
    # 从输出提取passed/total
    last_line = out.strip().split('\n')[-1] if out.strip() else ''
    status = last_line.split(':')[-1].strip() if ':' in last_line else ('ok' if ok else 'fail')
    
    print(f"{tf:35} {'✅' if ok else '❌':8} {status:8} {elapsed*1000:5.0f}ms")
    if err:
        print(f"  stderr: {err}")
    
    results.append((tf, ok, out[:200]))

total = len(results)
passed = sum(1 for r in results if r[1])
print(f'\n{"="*60}')
print(f'Total: {total} | Passed: {passed} | Failed: {total-passed}')
print(f'{"="*60}')
sys.exit(0 if passed == total else 1)
