"""IGP 单元测试: TestResult"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes\\chromosome12\\infra"))
from v5_auto_tester_v2 import TestResult

def test_create():
    obj = TestResult("test", True, {}, 0); assert obj is not None

def test_to_dict():
    obj = TestResult("test", True, {}, 0); r = obj.to_dict()
    assert r is not None

if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("to_dict",test_to_dict)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nTestResult: {_ok}/2"); sys.exit(0 if _ok==2 else 1)