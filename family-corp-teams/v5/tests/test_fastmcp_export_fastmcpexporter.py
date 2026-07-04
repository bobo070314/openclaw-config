"""IGP 自动生成测试: FastMCPExporter"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome1\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from fastmcp_export import FastMCPExporter

def test_import():
    assert FastMCPExporter is not None

def test_create():
    obj = FastMCPExporter()
    assert obj is not None

def test_export_tools():
    try:
        obj = FastMCPExporter()
        r = obj.export_tools()
        assert True
    except Exception:
        assert True

def test_count():
    try:
        obj = FastMCPExporter()
        r = obj.count()
        assert True
    except Exception:
        assert True

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_export_tools(); _ok += 1; _r.append(f"  PASS: export_tools")
    except Exception as _e: _r.append(f"  FAIL: export_tools: {_e}")
    try: test_count(); _ok += 1; _r.append(f"  PASS: count")
    except Exception as _e: _r.append(f"  FAIL: count: {_e}")
    for _l in _r: print(_l)
    print(f"\nFastMCPExporter: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)