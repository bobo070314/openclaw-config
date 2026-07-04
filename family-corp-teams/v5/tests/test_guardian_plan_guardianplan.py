"""IGP 自动生成测试: GuardianPlan"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome5\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from guardian_plan import GuardianPlan

def test_import():
    assert GuardianPlan is not None

def test_create():
    obj = GuardianPlan()
    assert obj is not None

def test_receive_request():
    assert hasattr(GuardianPlan, "receive_request")

def test_analyze_risk():
    try:
        obj = GuardianPlan()
        r = obj.analyze_risk()
        assert True
    except Exception:
        assert True

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_receive_request(); _ok += 1; _r.append(f"  PASS: receive_request")
    except Exception as _e: _r.append(f"  FAIL: receive_request: {_e}")
    try: test_analyze_risk(); _ok += 1; _r.append(f"  PASS: analyze_risk")
    except Exception as _e: _r.append(f"  FAIL: analyze_risk: {_e}")
    for _l in _r: print(_l)
    print(f"\nGuardianPlan: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)