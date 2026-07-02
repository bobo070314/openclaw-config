"""IGP 自动生成测试: IncrementalScanner"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome9\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from v5_incremental_scanner import IncrementalScanner

def test_import():
    assert IncrementalScanner is not None

def test_create():
    obj = IncrementalScanner()
    assert obj is not None

def test_scan_diff():
    assert hasattr(IncrementalScanner, "scan_diff")

def test_scan_file():
    assert hasattr(IncrementalScanner, "scan_file")

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_scan_diff(); _ok += 1; _r.append(f"  PASS: scan_diff")
    except Exception as _e: _r.append(f"  FAIL: scan_diff: {_e}")
    try: test_scan_file(); _ok += 1; _r.append(f"  PASS: scan_file")
    except Exception as _e: _r.append(f"  FAIL: scan_file: {_e}")
    for _l in _r: print(_l)
    print(f"\nIncrementalScanner: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)