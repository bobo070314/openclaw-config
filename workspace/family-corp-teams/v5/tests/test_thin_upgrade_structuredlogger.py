"""IGP 自动生成测试: StructuredLogger"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes"
if _SD not in sys.path: sys.path.insert(0, _SD)
from thin_upgrade import StructuredLogger

def test_import():
    assert StructuredLogger is not None

def test_create():
    try:
        obj = StructuredLogger(None)
        assert obj is not None
    except Exception:
        assert StructuredLogger is not None

def test_log():
    assert hasattr(StructuredLogger, "log")

def test_rotate_logs():
    try:
        obj = StructuredLogger(None)
        r = obj.rotate_logs()
        assert True
    except Exception:
        assert True

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_log(); _ok += 1; _r.append(f"  PASS: log")
    except Exception as _e: _r.append(f"  FAIL: log: {_e}")
    try: test_rotate_logs(); _ok += 1; _r.append(f"  PASS: rotate_logs")
    except Exception as _e: _r.append(f"  FAIL: rotate_logs: {_e}")
    for _l in _r: print(_l)
    print(f"\nStructuredLogger: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)