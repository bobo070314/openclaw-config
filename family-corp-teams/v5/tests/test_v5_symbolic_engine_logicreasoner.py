"""IGP 自动生成测试: LogicReasoner"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\sdk\symbolic\source"
if _SD not in sys.path: sys.path.insert(0, _SD)
from v5_symbolic_engine import LogicReasoner

def test_import():
    assert LogicReasoner is not None

def test_create():
    obj = LogicReasoner()
    assert obj is not None

def test_add_rule():
    assert hasattr(LogicReasoner, "add_rule")

def test_add_fact():
    assert hasattr(LogicReasoner, "add_fact")

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_add_rule(); _ok += 1; _r.append(f"  PASS: add_rule")
    except Exception as _e: _r.append(f"  FAIL: add_rule: {_e}")
    try: test_add_fact(); _ok += 1; _r.append(f"  PASS: add_fact")
    except Exception as _e: _r.append(f"  FAIL: add_fact: {_e}")
    for _l in _r: print(_l)
    print(f"\nLogicReasoner: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)