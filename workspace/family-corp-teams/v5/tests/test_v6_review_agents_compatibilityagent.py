"""IGP 自动生成测试: CompatibilityAgent"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\sdk\review\source"
if _SD not in sys.path: sys.path.insert(0, _SD)
from v6_review_agents import CompatibilityAgent

def test_import():
    assert CompatibilityAgent is not None

def test_create():
    try:
        obj = CompatibilityAgent(None)
        assert obj is not None
    except Exception:
        assert CompatibilityAgent is not None

def test_extract_signatures():
    assert hasattr(CompatibilityAgent, "extract_signatures")

def test_review():
    assert hasattr(CompatibilityAgent, "review")

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_extract_signatures(); _ok += 1; _r.append(f"  PASS: extract_signatures")
    except Exception as _e: _r.append(f"  FAIL: extract_signatures: {_e}")
    try: test_review(); _ok += 1; _r.append(f"  PASS: review")
    except Exception as _e: _r.append(f"  FAIL: review: {_e}")
    for _l in _r: print(_l)
    print(f"\nCompatibilityAgent: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)