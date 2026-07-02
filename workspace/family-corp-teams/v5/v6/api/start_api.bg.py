"""IGP API — 后台启动（绕过了subprocess编码问题）"""
from __future__ import annotations
import os
import subprocess
import sys
import time

V6 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6'
API_SCRIPT = os.path.join(V6, 'api', 'igp_api.py')
PORT = 8080

# 1. 清理旧进程
subprocess.run('netstat -ano | findstr :8080 > %TEMP%\\port_pids.txt', shell=True, capture_output=True)
if os.path.exists(os.environ['TEMP'] + '\\port_pids.txt'):
    with open(os.environ['TEMP'] + '\\port_pids.txt', 'r') as f:
        for line in f:
            if 'LISTENING' in line:
                parts = line.strip().split()
                if parts and parts[-1].isdigit():
                    subprocess.run(['taskkill', '/F', '/PID', parts[-1]], capture_output=True)
                    print(f"  Killed PID={parts[-1]}")

# 2. 用cmd /c start /b 启动（彻底分离进程树）
cmd = f'start /b cmd /c ""{sys.executable}" -W ignore -u "{API_SCRIPT}" --port {PORT}"'
subprocess.run(cmd, shell=True, capture_output=True)

# 3. 等待
import json
import urllib.request

for i in range(10):
    time.sleep(0.5)
    try:
        r = urllib.request.urlopen(f'http://localhost:{PORT}/api/v1/health', timeout=2)
        data = json.loads(r.read().decode('utf-8'))
        if data.get('status') == 'ok':
            print(f"  ✅ API就绪 (第{i+1}次尝试)")
            break
    except:
        pass
else:
    print("  ⚠️ 服务可能未完全就绪")

# 4. 验证路由
def api_get(path):
    try:
        return urllib.request.urlopen(f'http://localhost:{PORT}{path}', timeout=5).read().decode()
    except:
        return "error"

print(f"\n路由验证:")
print(f"  GET /api/v1/health                    -> {api_get('/api/v1/health')[:60]}")
print(f"  GET /api/v1/lifecycle                 -> {api_get('/api/v1/lifecycle')[:60]}")
print(f"  GET /api/v1/version/v5_bug_doctor      -> {api_get('/api/v1/version/v5_bug_doctor')[:60]}")
print(f"  GET /api/v1/lifecycle/product/v5_bug_doctor -> {api_get('/api/v1/lifecycle/product/v5_bug_doctor')[:60]}")

print(f"\n✅ 常驻服务: http://localhost:{PORT}")
print(f"  使用: curl http://localhost:{PORT}/api/v1/health")
print(f"  停止: taskkill /F /PID $(netstat -ano | findstr :{PORT} | findstr LISTENING)")
