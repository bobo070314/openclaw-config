#!/usr/bin/env python3
"""直接测试DashScope API调用，诊断错误原因"""
import os, urllib.request, json, sys

key_vars = [
    ("QWEN_API_KEY", ""),
    ("DASHSCOPE_API_KEY", ""),
    ("OPENCLAW_DASHSCOPE_KEY", ""),
]

for var, _ in key_vars:
    val = os.environ.get(var, "")
    if val and len(val) > 10:
        print(f"[{var}] len={len(val)} prefix={val[:12]}...")

# 尝试用OPENCLAW_DASHSCOPE_KEY调一次
key = os.environ.get("QWEN_API_KEY", "") or os.environ.get("DASHSCOPE_API_KEY", "") or os.environ.get("OPENCLAW_DASHSCOPE_KEY", "")
print(f"\nUsing key (first 12): {key[:12] if key else 'EMPTY'}...")
if not key:
    print("NO KEY FOUND")
    sys.exit(1)

# 直接调用一次
payload = {
    "model": "qwen-plus",
    "messages": [{"role": "user", "content": "Say hello in one word."}],
    "max_tokens": 10,
}
data = json.dumps(payload).encode()
req = urllib.request.Request(
    "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    data=data,
    headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    },
    method="POST",
)
try:
    resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
    print(f"SUCCESS: {resp['choices'][0]['message']['content']}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"HTTP {e.code}: {body[:300]}")
except Exception as e:
    print(f"Error: {e}")
