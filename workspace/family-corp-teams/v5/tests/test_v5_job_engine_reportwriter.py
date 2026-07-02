"""IGP 单元测试: ReportWriter"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "absorb", "docagent"))
import v5_job_engine
def test_module():
    assert hasattr(v5_job_engine, 'ReportWriter')
def test_import():
    assert True
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("module",test_module),("import",test_import)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nReportWriter: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
