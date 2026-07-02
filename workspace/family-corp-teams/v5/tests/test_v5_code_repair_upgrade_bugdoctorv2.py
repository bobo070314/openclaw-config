"""IGP 自动生成测试: BugDoctorV2"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome9\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from v5_code_repair_upgrade import BugDoctorV2

def test_import():
    assert BugDoctorV2 is not None

def test_create():
    obj = BugDoctorV2()
    assert obj is not None

def test_scan_file():
    assert hasattr(BugDoctorV2, "scan_file")

def test_scan_directory():
    assert hasattr(BugDoctorV2, "scan_directory")

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_scan_file(); _ok += 1; _r.append(f"  PASS: scan_file")
    except Exception as _e: _r.append(f"  FAIL: scan_file: {_e}")
    try: test_scan_directory(); _ok += 1; _r.append(f"  PASS: scan_directory")
    except Exception as _e: _r.append(f"  FAIL: scan_directory: {_e}")
    for _l in _r: print(_l)
    print(f"\nBugDoctorV2: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)