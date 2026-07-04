import requests
r = requests.get('http://127.0.0.1:12008/mcp', timeout=5)
print(f'MCP 12008/mcp => {r.status_code} | {r.headers.get("content-type", "")}')
print(r.text[:300])
