"""IGP 单元测试: Result"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome12", "infra"))
from v5_result_monad import Result
def test_ok():
    r = Result.Ok(42); assert r.is_ok
def test_err():
    r = Result.Err("err"); assert r.is_err
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("ok",test_ok),("err",test_err)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nResult: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
