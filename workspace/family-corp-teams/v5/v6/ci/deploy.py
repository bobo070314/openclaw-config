"""IGP — 一键部署: 升级→测试→重启→验证"""
from __future__ import annotations
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
V6 = os.path.join(V5, 'v6')

print('=' * 55)
print('IGP Deploy')
print('=' * 55)

errors = []

# 1. 注册表检查
print('\n[1] 产品注册表...')
reg = os.path.join(V6, 'product_registry.json')
with open(reg, 'r', encoding='utf-8') as f:
    data = json.load(f)
count = data['total_products']
print(f'   {count} products, {len(data["products"])} entries')

# 2. 重启API
print('\n[2] 重启API...')
subprocess.run(['taskkill', '/F', '/IM', 'python.exe', '/FI',
                'WINDOWTITLE eq igp_api*'], capture_output=True, timeout=3)
subprocess.run(
    f'start /b cmd /c ""{sys.executable}" -W ignore -u "{os.path.join(V6, "api", "igp_api.py")}" --port 8080"',
    shell=True, capture_output=True, timeout=3)

for i in range(5):
    time.sleep(1)
    try:
        r = urllib.request.urlopen('http://localhost:8080/api/v1/health', timeout=2)
        d = json.loads(r.read().decode('utf-8'))
        if d.get('status') == 'ok':
            print(f'   API ready')
            break
    except:
        pass
else:
    errors.append('API startup timeout')

# 3. 运行  CI pipeline
print('\n[3] CI Pipeline...')
r = subprocess.run([sys.executable, '-W', 'ignore', '-u',
                    os.path.join(V6, 'ci', 'pipeline.py')],
                   capture_output=True, timeout=60, text=True, encoding='utf-8')
out = r.stdout.decode('utf-8', errors='replace')
print(out[-500:] if len(out) > 500 else out)
if r.returncode != 0:
    errors.append('CI pipeline failed')

# 4. 验证API路由
print('\n[4] 验证路由...')
routes = ['/api/v1/health', '/api/v1/lifecycle', '/api/v1/version/v5_bug_doctor']
for path in routes:
    try:
        r = urllib.request.urlopen(f'http://localhost:8080{path}', timeout=3)
        print(f'   ✅ {path}')
    except Exception as e:
        errors.append(f'{path}: {e}')
        print(f'   ❌ {path}')

# 输出
print(f'\n{"="*55}')
if errors:
    print(f'⚠️  {len(errors)} warnings:')
    for e in errors:
        print(f'  - {e}')
else:
    print('✅ Deploy SUCCESS')
print(f'   Products: {count}')
print(f'   API: http://localhost:8080')
