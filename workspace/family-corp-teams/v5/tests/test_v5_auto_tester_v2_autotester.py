"""IGP 单元测试: AutoTester"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome12", "infra"))
from v5_auto_tester_v2 import AutoTester
def test_create():
    obj = AutoTester(); assert obj is not None
def test_module():
    assert AutoTester is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("module",test_module)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nAutoTester: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
