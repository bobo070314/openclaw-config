#!/usr/bin/env python3
"""SWAT突击队 v4 — Gateway端口是18789不是18900"""
import http.client, json, os

config_path = os.path.expanduser("~/.openclaw/openclaw.json")
cfg = json.load(open(config_path, encoding="utf-8"))
gw = cfg.get("gateway", {})
port = gw.get("port", 18789)
token = gw.get("auth", {}).get("token", "")
auth_mode = gw.get("auth", {}).get("mode", "")

print(f"Gateway port: {port}")
print(f"Auth mode: {auth_mode}")
print(f"Token: {token[:30]}...")

def send_goal_cmd(cmd):
    """直接发/goal命令到Gateway API"""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=15)
    payload = json.dumps({
        "model": "openclaw",
        "messages": [{"role": "user", "content": cmd}]
    })
    headers = {"Content-Type": "application/json"}
    if auth_mode == "token" and token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        conn.request("POST", "/v1/chat/completions", body=payload, headers=headers)
        resp = conn.getresponse()
        data = resp.read().decode()[:500]
        print(f"[{cmd}] => {resp.status}")
        if resp.status == 200:
            print(f"  SUCCESS!")
        else:
            print(f"  {data[:200]}")
        conn.close()
        return resp.status == 200
    except Exception as e:
        print(f"[{cmd}] Error: {e}")
        conn.close()
        return False

# 1. 先看能不能ping通
print("\n=== Check Gateway ===")
conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
try:
    conn.request("GET", "/v1/models")
    resp = conn.getresponse()
    print(f"Gateway reachable: {resp.status}")
    conn.close()
except Exception as e:
    print(f"Gateway NOT reachable: {e}")
    print("Trying dashboard port 18900 instead...")
    # 也可能是control UI代理
    conn = http.client.HTTPConnection("127.0.0.1", 18900, timeout=5)
    conn.request("POST", "/v1/chat/completions", 
                 body=json.dumps({"model": "openclaw", "messages": [{"role": "user", "content": "/goal clear"}]}),
                 headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    data = resp.read().decode()[:300]
    print(f"Dashboard proxy: {resp.status} {data[:200]}")
    conn.close()

# 2. 发送/goal clear
print("\n=== Step 1: /goal clear ===")
send_goal_cmd("/goal clear")

# 3. 发送/goal start
print("\n=== Step 2: /goal start ===")
send_goal_cmd("/goal start IGP v4 ultimate upgrade - 42Team collective research breakthrough, engine 8.5/10")

# 4. 验证
print("\n=== Done ===")
