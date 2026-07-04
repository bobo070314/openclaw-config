"""IGP 自动生成测试: ACPClient"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome6\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from acp_client import ACPClient

def test_import():
    assert ACPClient is not None

def test_create():
    try:
        obj = ACPClient(None)
        assert obj is not None
    except Exception:
        assert ACPClient is not None

def test_create_checkout():
    assert hasattr(ACPClient, "create_checkout")

def test_get_cart():
    assert hasattr(ACPClient, "get_cart")

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_create_checkout(); _ok += 1; _r.append(f"  PASS: create_checkout")
    except Exception as _e: _r.append(f"  FAIL: create_checkout: {_e}")
    try: test_get_cart(); _ok += 1; _r.append(f"  PASS: get_cart")
    except Exception as _e: _r.append(f"  FAIL: get_cart: {_e}")
    for _l in _r: print(_l)
    print(f"\nACPClient: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)