import os
key = os.environ.get("OPENAI_API_KEY", "")
print(f"Length: {len(key)}")
print(f"Prefix: {key[:15]}")
print(f"sk-or in key: {('sk-or' in key)}")
print(f"sk-ws in key: {('sk-ws' in key)}")
# Check all relevant env vars
for k, v in sorted(os.environ.items()):
    if any(x in k.upper() for x in ["OPEN", "API", "DEEP", "MODEL", "ROUTER"]):
        print(f"  {k} = {v[:20]}...{v[-4:] if len(v)>20 else v}")
