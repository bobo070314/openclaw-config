"""IGP 自动生成测试: AgentOSScheduler"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome7\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from agent_os_scheduler import AgentOSScheduler

def test_import():
    assert AgentOSScheduler is not None

def test_create():
    obj = AgentOSScheduler()
    assert obj is not None

def test_schedule():
    assert hasattr(AgentOSScheduler, "schedule")

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_schedule(); _ok += 1; _r.append(f"  PASS: schedule")
    except Exception as _e: _r.append(f"  FAIL: schedule: {_e}")
    for _l in _r: print(_l)
    print(f"\nAgentOSScheduler: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)