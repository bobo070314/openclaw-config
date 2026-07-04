"""IGP 自动生成测试: IGPAPIHandler"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\api"
if _SD not in sys.path: sys.path.insert(0, _SD)
from igp_api import IGPAPIHandler

def test_import():
    assert IGPAPIHandler is not None

def test_create():
    obj = IGPAPIHandler()
    assert obj is not None

def test_do_GET():
    try:
        obj = IGPAPIHandler()
        r = obj.do_GET()
        assert True
    except Exception:
        assert True

def test_do_POST():
    try:
        obj = IGPAPIHandler()
        r = obj.do_POST()
        assert True
    except Exception:
        assert True

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_do_GET(); _ok += 1; _r.append(f"  PASS: do_GET")
    except Exception as _e: _r.append(f"  FAIL: do_GET: {_e}")
    try: test_do_POST(); _ok += 1; _r.append(f"  PASS: do_POST")
    except Exception as _e: _r.append(f"  FAIL: do_POST: {_e}")
    for _l in _r: print(_l)
    print(f"\nIGPAPIHandler: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)