import requests, json

BASE = "http://127.0.0.1:18900"
HEADERS = {"Authorization": "Bearer foreign18900"}

routes = [
    "/v1/models",
    "/v1/agents",
    "/v1/channels",
    "/api/v1/models",
    "/api/v1/agents",
    "/api/v1/channels",
    "/openai/v1/models",
]

for route in routes:
    try:
        r = requests.get(BASE + route, headers=HEADERS, timeout=5)
        ct = r.headers.get("content-type", "")
        print(f"{route:30s} => {r.status_code:3d} | {ct}")
        if r.status_code == 200 and "json" in ct:
            data = r.json()
            if isinstance(data, dict):
                keys = list(data.keys()) if isinstance(data, dict) else []
                print(f"                               Keys: {keys[:10]}")
    except Exception as e:
        print(f"{route:30s} => ERROR: {e}")
