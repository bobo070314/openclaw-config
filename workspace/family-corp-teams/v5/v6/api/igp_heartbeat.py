"""
IGP API Heartbeat — 保活脚本
只输出 status: ok（正常）或 status: ALERT（真故障）
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
import time
import urllib.request

V6 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6'
API_SCRIPT = os.path.join(V6, 'api', 'igp_api.py')
PORT = 8080

def check():
    try:
        r = urllib.request.urlopen(f'http://localhost:{PORT}/api/v1/health', timeout=3)
        d = json.loads(r.read().decode('utf-8'))
        if d.get('status') == 'ok':
            return {"status": "ok", "pid": "running"}
    except Exception:
        pass
    return {"status": "down"}

def start():
    cmd = f'start /b cmd /c ""{sys.executable}" -W ignore -u "{API_SCRIPT}" --port {PORT}"'
    subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
    for i in range(5):
        time.sleep(0.5)
        s = check()
        if s.get('status') == 'ok':
            return s
    return {"status": "failed"}

if __name__ == '__main__':
    s = check()
    if s.get('status') == 'ok':
        # ✅ 正常：只输出一行 ok
        print("status: ok")
        sys.exit(0)
    else:
        # ⚠️ 异常：先重启再报
        r = start()
        if r.get('status') == 'ok':
            print("status: ok")
            sys.exit(0)
        else:
            print("status: ALERT (IGP API 重启失败)")
            sys.exit(1)
