#!/usr/bin/env python3
"""SWAT突击队：强行清旧Goal + 创建新Goal — 不走tool，走Gateway API"""
import http.client, json, os, sys

config_path = os.path.expanduser("~/.openclaw/openclaw.json")
token = ""

if os.path.exists(config_path):
    try:
        cfg = json.load(open(config_path, encoding="utf-8"))
        gw = cfg.get("gateway", {})
        auth = gw.get("auth", {})
        token = auth.get("token", "")
        print(f"Gateway auth mode: {auth.get('mode', '?')}")
        print(f"Token: {token[:20]}..." if token else "No token found")
    except Exception as e:
        print(f"Config error: {e}")

port = 18900
headers = {"Content-Type": "application/json"}

def api_chat(msg):
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=15)
    payload = json.dumps({"model": "openclaw", "messages": [{"role": "user", "content": msg}]})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        conn.request("POST", "/v1/chat/completions", body=payload, headers=headers)
        resp = conn.getresponse()
        data = resp.read().decode()
        print(f"\n[SEND] {msg}")
        print(f"[STATUS] {resp.status}")
        print(f"[RESP] {data[:300]}")
        conn.close()
        return data
    except Exception as e:
        print(f"[ERROR] {e}")
        conn.close()
        return None

# 第一步：/goal clear
print("=== Step 1: /goal clear ===")
api_chat("/goal clear")

# 第二步：/goal start 
print("\n=== Step 2: /goal start ===")
api_chat("/goal start IGP v4 ultimate upgrade - 42Team collective research breakthrough, engine 8.5/10")

print("\n=== Done ===")
