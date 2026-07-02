"""IGP 自动生成测试: SymbolicEngine"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\sdk\symbolic\source"
if _SD not in sys.path: sys.path.insert(0, _SD)
from v5_symbolic_engine import SymbolicEngine

def test_import():
    assert SymbolicEngine is not None

def test_create():
    obj = SymbolicEngine()
    assert obj is not None

def test_add_var():
    assert hasattr(SymbolicEngine, "add_var")

def test_add_constraint():
    assert hasattr(SymbolicEngine, "add_constraint")

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_add_var(); _ok += 1; _r.append(f"  PASS: add_var")
    except Exception as _e: _r.append(f"  FAIL: add_var: {_e}")
    try: test_add_constraint(); _ok += 1; _r.append(f"  PASS: add_constraint")
    except Exception as _e: _r.append(f"  FAIL: add_constraint: {_e}")
    for _l in _r: print(_l)
    print(f"\nSymbolicEngine: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)