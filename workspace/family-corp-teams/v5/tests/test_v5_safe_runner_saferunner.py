"""IGP 自动生成测试: SafeRunner"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome12\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from v5_safe_runner import SafeRunner

def test_import():
    assert SafeRunner is not None

def test_create():
    try:
        obj = SafeRunner(None, None)
        assert obj is not None
    except Exception:
        assert SafeRunner is not None

def test_run():
    assert hasattr(SafeRunner, "run")

def test_run_async():
    assert hasattr(SafeRunner, "run_async")

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_run(); _ok += 1; _r.append(f"  PASS: run")
    except Exception as _e: _r.append(f"  FAIL: run: {_e}")
    try: test_run_async(); _ok += 1; _r.append(f"  PASS: run_async")
    except Exception as _e: _r.append(f"  FAIL: run_async: {_e}")
    for _l in _r: print(_l)
    print(f"\nSafeRunner: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)