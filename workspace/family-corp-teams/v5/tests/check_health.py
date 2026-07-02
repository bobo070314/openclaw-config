"""IGP health check"""
import json, urllib.request
r = urllib.request.urlopen('http://localhost:8080/api/v1/health', timeout=3)
d = json.loads(r.read())
print(f"API: {d['status']}")
print(f"Full: {d}")
