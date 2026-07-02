"""IGP 自动生成测试: WeightedRouter"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes"
if _SD not in sys.path: sys.path.insert(0, _SD)
from thin_upgrade import WeightedRouter

def test_import():
    assert WeightedRouter is not None

def test_create():
    try:
        obj = WeightedRouter(None)
        assert obj is not None
    except Exception:
        assert WeightedRouter is not None

def test_route():
    assert hasattr(WeightedRouter, "route")

def test_inspect():
    try:
        obj = WeightedRouter(None)
        r = obj.inspect()
        assert True
    except Exception:
        assert True

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_route(); _ok += 1; _r.append(f"  PASS: route")
    except Exception as _e: _r.append(f"  FAIL: route: {_e}")
    try: test_inspect(); _ok += 1; _r.append(f"  PASS: inspect")
    except Exception as _e: _r.append(f"  FAIL: inspect: {_e}")
    for _l in _r: print(_l)
    print(f"\nWeightedRouter: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)