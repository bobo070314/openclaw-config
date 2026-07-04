"""IGP 单元测试: LoggerContext"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome12", "infra"))
from v5_logger_context import LoggerContext
def test_create():
    lc = LoggerContext("test"); assert lc is not None
def test_info():
    lc = LoggerContext("test"); lc.info("test"); assert True
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("info",test_info)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nLoggerContext: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
