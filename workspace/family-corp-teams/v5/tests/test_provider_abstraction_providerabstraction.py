"""IGP 单元测试: ProviderAbstraction"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome4", "infra"))
from provider_abstraction import ProviderAbstraction
def test_create():
    obj = ProviderAbstraction("test"); assert obj is not None
def test_add_model():
    obj = ProviderAbstraction("test"); obj.add_model("m1", lambda: "ok")
    r = obj.list_models(); assert len(r) > 0
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("add_model",test_add_model)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nProviderAbstraction: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
