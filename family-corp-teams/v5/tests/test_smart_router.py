"""IGP 单元测试: SmartRouter"""
from __future__ import annotations
import sys, os
V5 = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome4", "infra"))
from v5_smart_router import SmartRouter
def test_create():
    sr = SmartRouter("test"); assert sr is not None
def test_route():
    sr = SmartRouter("test"); sr.register("p1", {"capabilities":"general"})
    r = sr.route({"type":"test"}, "weighted")
    assert isinstance(r, dict)
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("route",test_route)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\\nSmartRouter: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
