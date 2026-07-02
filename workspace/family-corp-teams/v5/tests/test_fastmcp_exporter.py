"""IGP 单元测试: FastMCPExporter"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome1", "infra"))
from fastmcp_export import FastMCPExporter
def test_create():
    f = FastMCPExporter(); assert f is not None
def test_export_tools():
    f = FastMCPExporter(); r = f.export_tools()
    assert isinstance(r, (list, dict))
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("export_tools",test_export_tools)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nFastMCPExporter: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
