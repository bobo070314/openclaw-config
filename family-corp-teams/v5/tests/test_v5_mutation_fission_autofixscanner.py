"""IGP 单元测试: AutoFixScanner"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome0", "infra"))
from v5_mutation_fission import AutoFixScanner
def test_create():
    obj = AutoFixScanner(); assert obj is not None
def test_scan():
    obj = AutoFixScanner(); r = obj.scan_and_fix(V5); assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("scan",test_scan)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nAutoFixScanner: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
