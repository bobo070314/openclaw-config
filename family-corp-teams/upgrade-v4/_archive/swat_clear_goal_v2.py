#!/usr/bin/env python3
"""SWAT突击队 v2：排查Gateway auth + 强制清Goal"""
import http.client, json, os

config_path = os.path.expanduser("~/.openclaw/openclaw.json")
cfg = json.load(open(config_path, encoding="utf-8"))
gw = cfg.get("gateway", {})
auth = gw.get("auth", {})
token = auth.get("token", "")
mode = auth.get("mode", "")

print(f"Auth mode: {mode}")
print(f"Token type: {type(token).__name__}")
print(f"Token len: {len(token)}")
print(f"Token preview: {token[:40]}...")

# 尝试直接用 /v1/goal 或其它端点
# 先查dashboard
port = 18900

def try_request(method, path, body=None, extra_headers=None):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    headers = {"Content-Type": "application/json", "Origin": "http://127.0.0.1:18900"}
    if extra_headers:
        headers.update(extra_headers)
    # 尝试各种auth格式
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        conn.request(method, path, body=body, headers=headers)
        resp = conn.getresponse()
        data = resp.read().decode()[:500]
        print(f"[{method} {path}] => {resp.status} {data[:200]}")
        conn.close()
        return resp.status, data
    except Exception as e:
        print(f"[{method} {path}] Error: {e}")
        conn.close()
        return None, str(e)

# 1. 直接POST到消息API (新格式)
payload = json.dumps({"channel": "webchat", "message": "/goal clear", "sessionKey": "agent:main:main"})
try_request("POST", "/api/messages", body=payload)

# 2. 试试SEND端点
try_request("POST", "/v1/sessions/send", body=json.dumps({"sessionKey": "agent:main:main", "message": "/goal clear"}))

# 3. 没有token也能访问的control UI
try_request("GET", "/openclaw/")

# 4. 试试用env token走remote
env_token = os.environ.get("OPENCLAW_GATEWAY_TOKEN", "")
print(f"\nENV token: {env_token[:20]}..." if env_token else "No env token")

if env_token:
    try_request("POST", "/v1/chat/completions", 
                body=json.dumps({"model": "openclaw", "messages": [{"role": "user", "content": "/goal clear"}]}),
                extra_headers={"Authorization": f"Bearer {env_token}"})

print("\n=== 尝试用WebSocket发送 - 通过openclaw CLI ===")
