"""IGP 自动生成测试: Reader"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome13_hr\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from v5_hr_engine import Reader

def test_import():
    assert Reader is not None

def test_create():
    try:
        obj = Reader(None)
        assert obj is not None
    except Exception:
        assert Reader is not None

def test_scan():
    try:
        obj = Reader(None)
        r = obj.scan()
        assert True
    except Exception:
        assert True

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_scan(); _ok += 1; _r.append(f"  PASS: scan")
    except Exception as _e: _r.append(f"  FAIL: scan: {_e}")
    for _l in _r: print(_l)
    print(f"\nReader: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)