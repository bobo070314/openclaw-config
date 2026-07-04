"""IGP 单元测试: GuardianAct"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome5", "infra"))
import guardian_act
def test_module():
    assert hasattr(guardian_act, 'GuardianAct')
def test_contains():
    assert 'GuardianAct' in dir(guardian_act)
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("module",test_module),("contains",test_contains)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nGuardianAct: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
