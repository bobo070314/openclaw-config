import requests, json, os

BASE = "http://127.0.0.1:18900"

def check(url, label):
    try:
        r = requests.get(f"{BASE}{url}", timeout=10)
        print(f"\n{'='*50}")
        print(f"📋 {label}: {url}")
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            ct = r.headers.get("content-type", "")
            if "json" in ct:
                data = r.json()
                print(json.dumps(data, indent=2, ensure_ascii=False)[:800])
            else:
                print(r.text[:500])
        else:
            print(r.text[:300])
    except Exception as e:
        print(f"❌ {label} ERROR: {e}")

check("/health", "L2 Gateway 健康")
check("/v1/models", "L4 Models")
check("/v1/agents", "L3 Agents")
check("/v1/channels", "L1 Channels")

state_dir = r"D:\bobo\openclaw-foreign\state"
print(f"\n{'='*50}")
print(f"📋 L5 State 目录: {state_dir}")
if os.path.exists(state_dir):
    files = os.listdir(state_dir)
    print(f"文件数: {len(files)}")
    for f in files[:10]:
        print(f"  - {f}")
else:
    print("目录不存在")
