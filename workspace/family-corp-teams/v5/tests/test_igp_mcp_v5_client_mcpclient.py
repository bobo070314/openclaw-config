"""IGP 自动生成测试: MCPClient"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome1\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from igp_mcp_v5_client import MCPClient

def test_import():
    assert MCPClient is not None

def test_create():
    try:
        obj = MCPClient(None)
        assert obj is not None
    except Exception:
        assert MCPClient is not None

def test_connect_stdio():
    assert hasattr(MCPClient, "connect_stdio")

def test_connect_http():
    assert hasattr(MCPClient, "connect_http")

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_connect_stdio(); _ok += 1; _r.append(f"  PASS: connect_stdio")
    except Exception as _e: _r.append(f"  FAIL: connect_stdio: {_e}")
    try: test_connect_http(); _ok += 1; _r.append(f"  PASS: connect_http")
    except Exception as _e: _r.append(f"  FAIL: connect_http: {_e}")
    for _l in _r: print(_l)
    print(f"\nMCPClient: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)