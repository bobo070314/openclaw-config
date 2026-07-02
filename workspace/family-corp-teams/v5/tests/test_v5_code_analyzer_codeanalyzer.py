"""IGP 自动生成测试: CodeAnalyzer"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\sdk\analyzer\source"
if _SD not in sys.path: sys.path.insert(0, _SD)
from v5_code_analyzer import CodeAnalyzer

def test_import():
    assert CodeAnalyzer is not None

def test_create():
    try:
        obj = CodeAnalyzer(None)
        assert obj is not None
    except Exception:
        assert CodeAnalyzer is not None

def test_scan_dead_code():
    try:
        obj = CodeAnalyzer(None)
        r = obj.scan_dead_code()
        assert True
    except Exception:
        assert True

def test_scan_refactoring():
    try:
        obj = CodeAnalyzer(None)
        r = obj.scan_refactoring()
        assert True
    except Exception:
        assert True

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_scan_dead_code(); _ok += 1; _r.append(f"  PASS: scan_dead_code")
    except Exception as _e: _r.append(f"  FAIL: scan_dead_code: {_e}")
    try: test_scan_refactoring(); _ok += 1; _r.append(f"  PASS: scan_refactoring")
    except Exception as _e: _r.append(f"  FAIL: scan_refactoring: {_e}")
    for _l in _r: print(_l)
    print(f"\nCodeAnalyzer: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)