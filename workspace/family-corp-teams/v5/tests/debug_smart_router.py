"""Debug SmartRouter.route"""
import sys, os
V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
sys.path.insert(0, os.path.join(V5, 'chromosomes', 'chromosome4', 'infra'))
from v5_smart_router import SmartRouter
sr = SmartRouter("test")
sr.register("p1", {"name":"p1", "capabilities":"general"})
sr.register("p2", {"name":"p2", "capabilities":"special"})

try:
    r = sr.route({"type":"test"}, "weighted")
    print(f"route weighted: {type(r).__name__} = {r}")
except Exception as e:
    print(f"route weighted ERROR: {e}")

try:
    r = sr.route({"type":"test"}, "lru")
    print(f"route lru: {type(r).__name__} = {r}")
except Exception as e:
    print(f"route lru ERROR: {e}")

try:
    r = sr.select({"type":"test"})
    print(f"select: {type(r).__name__} = {r}")
except Exception as e:
    print(f"select ERROR: {e}")
