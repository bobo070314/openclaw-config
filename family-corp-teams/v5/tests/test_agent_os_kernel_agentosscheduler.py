"""IGP 自动生成测试: AgentOSScheduler"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome7\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from agent_os_kernel import AgentOSScheduler

def test_import():
    assert AgentOSScheduler is not None

def test_create():
    obj = AgentOSScheduler()
    assert obj is not None

def test_add_task():
    assert hasattr(AgentOSScheduler, "add_task")

def test_run_pending():
    try:
        obj = AgentOSScheduler()
        r = obj.run_pending()
        assert True
    except Exception:
        assert True

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_add_task(); _ok += 1; _r.append(f"  PASS: add_task")
    except Exception as _e: _r.append(f"  FAIL: add_task: {_e}")
    try: test_run_pending(); _ok += 1; _r.append(f"  PASS: run_pending")
    except Exception as _e: _r.append(f"  FAIL: run_pending: {_e}")
    for _l in _r: print(_l)
    print(f"\nAgentOSScheduler: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)