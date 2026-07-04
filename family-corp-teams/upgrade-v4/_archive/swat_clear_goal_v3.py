#!/usr/bin/env python3
"""SWAT突击队 v3 — 直接读Gateway日志，找正确的token + 命令格式"""
import http.client, json, os, subprocess

# 仔细读一下openclaw.json的完整结构看看auth怎么配置的
config_path = os.path.expanduser("~/.openclaw/openclaw.json")
cfg = json.load(open(config_path, encoding="utf-8"))
print("=== Config keys ===")
print(json.dumps({k: type(v).__name__ for k, v in cfg.items()}, indent=2))

gw = cfg.get("gateway", {})
print("\n=== Gateway section ===")
print(json.dumps(gw, indent=2, ensure_ascii=False)[:1000])

# 试试用.env里面的OPENCLAW_GATEWAY_TOKEN
env_file = os.path.expanduser("~/.openclaw/.env")
if os.path.exists(env_file):
    print(f"\n=== .env file ({env_file}) ===")
    with open(env_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "TOKEN" in line.upper() and not line.startswith("#"):
                print(line[:60])

# 试试clawdbot (旧版)
old_config = os.path.expanduser("~/.clawdbot/openclaw.json")
if os.path.exists(old_config):
    print(f"\n=== Old config at {old_config} ===")
    old_cfg = json.load(open(old_config, encoding="utf-8"))
    print(json.dumps(old_cfg.get("gateway", {}), indent=2)[:500])

# 真正关键：用正确的token访问
# openclaw status显示它连gateway成功，说明token对
# 可能是header格式问题
# 试试直接按openclaw源码来
token = os.environ.get("OPENCLAW_GATEWAY_TOKEN", gw.get("auth", {}).get("token", ""))

print(f"\n=== Using token: {token[:30]}... ===")

def try_token_style(style_name, headers, body):
    """试不同header格式"""
    conn = http.client.HTTPConnection("127.0.0.1", 18900, timeout=10)
    try:
        conn.request("POST", "/v1/chat/completions", body=body, headers=headers)
        resp = conn.getresponse()
        data = resp.read().decode()[:200]
        print(f"[{style_name}] => {resp.status}")
        if resp.status == 200:
            print(f"SUCCESS! Data: {data[:200]}")
            return True
        elif resp.status == 401:
            pass  # expected
        else:
            print(f"  {data[:100]}")
    except Exception as e:
        print(f"[{style_name}] Error: {e}")
    finally:
        conn.close()
    return False

payload = json.dumps({"model": "openclaw", "messages": [{"role": "user", "content": "/goal clear"}]})

try_token_style("Bearer + token", {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}, payload)
try_token_style("Token + token", {"Content-Type": "application/json", "Authorization": f"Token {token}"}, payload)
try_token_style("Basic base64", {"Content-Type": "application/json", "Authorization": f"Basic {token}"}, payload)

# 检查x-auth-token
try_token_style("X-Auth-Token", {"Content-Type": "application/json", "X-Auth-Token": token}, payload)

# 看看dashboard有没有goal控制
conn = http.client.HTTPConnection("127.0.0.1", 18900, timeout=10)
conn.request("GET", "/")
resp = conn.getresponse()
data = resp.read().decode()[:2000]
print(f"\n[Dashboard /] => {resp.status}")
# 看有没有跳转
if resp.status in (301, 302):
    print(f"Redirect: {resp.getheader('Location')}")
conn.close()
