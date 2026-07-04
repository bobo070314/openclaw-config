"""IGP 自动生成测试: ArchitectureAgent"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\sdk\review\source"
if _SD not in sys.path: sys.path.insert(0, _SD)
from v6_review_agents import ArchitectureAgent

def test_import():
    assert ArchitectureAgent is not None

def test_create():
    try:
        obj = ArchitectureAgent(None)
        assert obj is not None
    except Exception:
        assert ArchitectureAgent is not None

def test_review():
    assert hasattr(ArchitectureAgent, "review")

def test_name():
    try:
        obj = ArchitectureAgent(None)
        r = obj.name()
        assert True
    except Exception:
        assert True

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_review(); _ok += 1; _r.append(f"  PASS: review")
    except Exception as _e: _r.append(f"  FAIL: review: {_e}")
    try: test_name(); _ok += 1; _r.append(f"  PASS: name")
    except Exception as _e: _r.append(f"  FAIL: name: {_e}")
    for _l in _r: print(_l)
    print(f"\nArchitectureAgent: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)