"""IGP 单元测试: AgentOSKernel"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome7", "infra"))
from agent_os_kernel import AgentOSKernel
def test_create():
    k = AgentOSKernel(); assert k is not None
def test_register():
    k = AgentOSKernel(); k.register_agent("test", {"name":"test"})
    s = k.status(); assert s.get("agents",0) >= 1
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("register",test_register)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nAgentOSKernel: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
