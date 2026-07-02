"""IGP 单元测试: MCPClient"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome1", "infra"))
from igp_mcp_v5_client import MCPClient
def test_create():
    mc = MCPClient("http://localhost:8000"); assert mc is not None
def test_connected():
    mc = MCPClient("http://localhost:8000"); r = mc.is_connected()
    assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("connected",test_connected)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nMCPClient: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
