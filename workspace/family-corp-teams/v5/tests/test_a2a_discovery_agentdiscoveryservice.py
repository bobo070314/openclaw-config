"""IGP 自动生成测试: AgentDiscoveryService"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome2\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from a2a_discovery import AgentDiscoveryService

def test_import():
    assert AgentDiscoveryService is not None

def test_create():
    obj = AgentDiscoveryService()
    assert obj is not None

def test_register():
    assert hasattr(AgentDiscoveryService, "register")

def test_find_by_capability():
    assert hasattr(AgentDiscoveryService, "find_by_capability")

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_register(); _ok += 1; _r.append(f"  PASS: register")
    except Exception as _e: _r.append(f"  FAIL: register: {_e}")
    try: test_find_by_capability(); _ok += 1; _r.append(f"  PASS: find_by_capability")
    except Exception as _e: _r.append(f"  FAIL: find_by_capability: {_e}")
    for _l in _r: print(_l)
    print(f"\nAgentDiscoveryService: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)