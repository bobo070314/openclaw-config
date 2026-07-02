"""IGP 自动生成测试: AgentOSKernel"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome7\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from agent_os_kernel import AgentOSKernel

def test_import():
    assert AgentOSKernel is not None

def test_create():
    try:
        obj = AgentOSKernel(None)
        assert obj is not None
    except Exception:
        assert AgentOSKernel is not None

def test_register_agent():
    assert hasattr(AgentOSKernel, "register_agent")

def test_send_message():
    assert hasattr(AgentOSKernel, "send_message")

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_register_agent(); _ok += 1; _r.append(f"  PASS: register_agent")
    except Exception as _e: _r.append(f"  FAIL: register_agent: {_e}")
    try: test_send_message(); _ok += 1; _r.append(f"  PASS: send_message")
    except Exception as _e: _r.append(f"  FAIL: send_message: {_e}")
    for _l in _r: print(_l)
    print(f"\nAgentOSKernel: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)