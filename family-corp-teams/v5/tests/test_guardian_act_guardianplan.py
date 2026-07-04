"""IGP 单元测试: GuardianPlan"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome5", "infra"))
from guardian_act import GuardianPlan
def test_create():
    obj = GuardianPlan("test"); assert obj is not None
def test_add_step():
    obj = GuardianPlan("test"); obj.add_step("test"); r = obj.execute()
    assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("add_step",test_add_step)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nGuardianPlan: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
