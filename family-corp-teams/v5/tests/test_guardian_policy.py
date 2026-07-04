"""IGP 单元测试: GuardianPolicy"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome5", "infra"))
from guardian_policy import GuardianPolicy
def test_create():
    gp = GuardianPolicy(); assert gp is not None
def test_check_file():
    gp = GuardianPolicy(); r = gp.check_file_op("/tmp/test.txt")
    assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("check_file",test_check_file)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nGuardianPolicy: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
