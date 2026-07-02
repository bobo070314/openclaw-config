"""IGP 单元测试: IncrementalScanner"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome9", "infra"))
from v5_incremental_scanner import IncrementalScanner
def test_create():
    s = IncrementalScanner(); assert s is not None
def test_report():
    s = IncrementalScanner(); r = s.report("json")
    assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("report",test_report)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nIncrementalScanner: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
