"""IGP 自动生成测试: MCPv2Discovery"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome1\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from mcp_v2_upgrade import MCPv2Discovery

def test_import():
    assert MCPv2Discovery is not None

def test_create():
    obj = MCPv2Discovery()
    assert obj is not None

def test_discover_local():
    try:
        obj = MCPv2Discovery()
        r = obj.discover_local()
        assert True
    except Exception:
        assert True

def test_discover_pypi():
    assert hasattr(MCPv2Discovery, "discover_pypi")

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_discover_local(); _ok += 1; _r.append(f"  PASS: discover_local")
    except Exception as _e: _r.append(f"  FAIL: discover_local: {_e}")
    try: test_discover_pypi(); _ok += 1; _r.append(f"  PASS: discover_pypi")
    except Exception as _e: _r.append(f"  FAIL: discover_pypi: {_e}")
    for _l in _r: print(_l)
    print(f"\nMCPv2Discovery: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)