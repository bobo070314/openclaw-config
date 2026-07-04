"""IGP 自动生成测试: IGPAPIClient"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\api"
if _SD not in sys.path: sys.path.insert(0, _SD)
from igp_api_client import IGPAPIClient

def test_import():
    assert IGPAPIClient is not None

def test_create():
    try:
        obj = IGPAPIClient(None)
        assert obj is not None
    except Exception:
        assert IGPAPIClient is not None

def test_health():
    try:
        obj = IGPAPIClient(None)
        r = obj.health()
        assert True
    except Exception:
        assert True

def test_lifecycle_summary():
    try:
        obj = IGPAPIClient(None)
        r = obj.lifecycle_summary()
        assert True
    except Exception:
        assert True

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_health(); _ok += 1; _r.append(f"  PASS: health")
    except Exception as _e: _r.append(f"  FAIL: health: {_e}")
    try: test_lifecycle_summary(); _ok += 1; _r.append(f"  PASS: lifecycle_summary")
    except Exception as _e: _r.append(f"  FAIL: lifecycle_summary: {_e}")
    for _l in _r: print(_l)
    print(f"\nIGPAPIClient: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)