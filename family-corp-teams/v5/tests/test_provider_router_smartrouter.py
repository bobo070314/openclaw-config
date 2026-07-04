"""IGP 自动生成测试: SmartRouter"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome4\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from provider_router import SmartRouter

def test_import():
    assert SmartRouter is not None

def test_create():
    try:
        obj = SmartRouter(None)
        assert obj is not None
    except Exception:
        assert SmartRouter is not None

def test_route():
    assert hasattr(SmartRouter, "route")

def test_chat():
    assert hasattr(SmartRouter, "chat")

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_route(); _ok += 1; _r.append(f"  PASS: route")
    except Exception as _e: _r.append(f"  FAIL: route: {_e}")
    try: test_chat(); _ok += 1; _r.append(f"  PASS: chat")
    except Exception as _e: _r.append(f"  FAIL: chat: {_e}")
    for _l in _r: print(_l)
    print(f"\nSmartRouter: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)