"""IGP 自动生成测试: A2ATaskProtocol"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome2\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from a2a_v2_upgrade import A2ATaskProtocol

def test_import():
    assert A2ATaskProtocol is not None

def test_create():
    obj = A2ATaskProtocol()
    assert obj is not None

def test_create_task():
    assert hasattr(A2ATaskProtocol, "create_task")

def test_create_streaming():
    assert hasattr(A2ATaskProtocol, "create_streaming")

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_create_task(); _ok += 1; _r.append(f"  PASS: create_task")
    except Exception as _e: _r.append(f"  FAIL: create_task: {_e}")
    try: test_create_streaming(); _ok += 1; _r.append(f"  PASS: create_streaming")
    except Exception as _e: _r.append(f"  FAIL: create_streaming: {_e}")
    for _l in _r: print(_l)
    print(f"\nA2ATaskProtocol: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)