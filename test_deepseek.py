#!/usr/bin/env python3
import os
import requests
import json

key = os.environ.get('DEEPSEEK_API_KEY', '')
if not key:
    print("❌ DEEPSEEK_API_KEY 环境变量未设置")
    exit(1)

url = "https://api.deepseek.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}
body = {
    "model": "deepseek-v4-flash",
    "messages": [{"role": "user", "content": "你好"}]
}

print(f"🔑 Key 长度: {len(key)} 位")
print(f"🔑 Key 末尾: ...{key[-4:]}")
print(f"📡 调用 DeepSeek API: {url}")

try:
    resp = requests.post(url, headers=headers, json=body, timeout=30)
    print(f"\n✅ 状态码: {resp.status_code}")
    data = resp.json()
    print(f"✅ 回复: {data['choices'][0]['message']['content'][:100]}...")
    print("\n✅ DeepSeek API 正常，Key 和模型 ID 完全正确！问题在 OpenClaw 的 tool 调用。")
except Exception as e:
    print(f"\n❌ 错误: {e}")
    print("请检查 Key 是否完整（末尾有没有多 n）")
