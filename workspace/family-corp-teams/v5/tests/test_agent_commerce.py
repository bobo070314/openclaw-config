"""IGP 单元测试: AgentCommerceEngine"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome6", "infra"))
from agent_commerce_v2 import AgentCommerceEngine
def test_create():
    ac = AgentCommerceEngine(); assert ac is not None
def test_charge():
    ac = AgentCommerceEngine(); r = ac.charge_task("test", "test_task", 0)
    assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("charge",test_charge)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nAgentCommerceEngine: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
