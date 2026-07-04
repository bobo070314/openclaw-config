import requests, json, os

base = 'http://127.0.0.1:18900'

print('=== L2 健康检查 ===')
try:
    r = requests.get(f'{base}/health', timeout=5)
    print(f'状态码: {r.status_code}')
    print(json.dumps(r.json(), indent=2, ensure_ascii=False)[:500])
except Exception as e:
    print(f'❌ 失败: {e}')

print('\n=== L4 模型列表 ===')
try:
    r = requests.get(f'{base}/v1/models', timeout=5)
    data = r.json()
    for p in data.get('data', []):
        print(f"  {p['id']}: {p.get('owned_by','?')}/{p['id']}")
except Exception as e:
    print(f'❌ 失败: {e}')

print('\n=== L3 Agent 列表 ===')
try:
    r = requests.get(f'{base}/v1/agents', timeout=5)
    for a in r.json().get('data', []):
        print(f"  {a['id']}: {a.get('defaults',{}).get('model','?')}")
except Exception as e:
    print(f'❌ 失败: {e}')

print('\n=== L1 Channels ===')
try:
    r = requests.get(f'{base}/v1/channels', timeout=5)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False)[:300])
except Exception as e:
    print(f'❌ 失败: {e}')

print('\n=== L5 State 目录 ===')
for d in os.listdir('D:\\bobo\\openclaw-foreign\\state'):
    print(f'  {d}/')
