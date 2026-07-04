#!/usr/bin/env python3
"""测试OPENCLAW_DASHSCOPE_KEY —— 新格式ws-key"""
import os, json, urllib.request

key = os.environ.get("OPENCLAW_DASHSCOPE_KEY", "")
print(f"Key type: {key[:5]}... len={len(key)}")

if not key or len(key) < 20:
    print("Key too short or missing")
else:
    payload = json.dumps({
        "model": "qwen-plus",
        "messages": [{"role": "user", "content": "Reply with exactly: hello"}],
        "max_tokens": 10,
    }).encode()
    req = urllib.request.Request(
        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
        print(f"DASHSCOPE: SUCCESS ✅ -> {resp['choices'][0]['message']['content']}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if "Incorrect API key" in body:
            # 可能是OpenAI兼容key格式，试试用OpenAI的endpoint
            print("DashScope rejected key, trying as OpenAI-compatible key...")
            payload2 = json.dumps({
                "model": "qwen-plus",
                "messages": [{"role": "user", "content": "hi"}],
                "max_tokens": 10,
            }).encode()
            req2 = urllib.request.Request(
                "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                data=payload2,
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            try:
                resp2 = json.loads(urllib.request.urlopen(req2, timeout=30).read())
                print(f"DASHSCOPE(2): SUCCESS ✅ -> {resp2['choices'][0]['message']['content']}")
            except Exception as e2:
                print(f"Both failed: {e2}")
        else:
            print(f"HTTP {e.code}: {body[:200]}")
    except Exception as e:
        print(f"Error: {e}")
