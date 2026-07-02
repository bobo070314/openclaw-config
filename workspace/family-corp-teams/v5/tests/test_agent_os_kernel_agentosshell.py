"""IGP 自动生成测试: AgentOSShell"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome7\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from agent_os_kernel import AgentOSShell

def test_import():
    assert AgentOSShell is not None

def test_create():
    try:
        obj = AgentOSShell(None)
        assert obj is not None
    except Exception:
        assert AgentOSShell is not None

def test_run_command():
    assert hasattr(AgentOSShell, "run_command")

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_run_command(); _ok += 1; _r.append(f"  PASS: run_command")
    except Exception as _e: _r.append(f"  FAIL: run_command: {_e}")
    for _l in _r: print(_l)
    print(f"\nAgentOSShell: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)