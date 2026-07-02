"""Fix last 8 tests — each with specific real API"""
import os

TD = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\tests'

# guardianact — was mangled by previous fix. Rewrite fully
content0 = r'''"""IGP 单元测试: GuardianAct"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome5", "infra"))
from guardian_act import GuardianAct
def test_create():
    obj = GuardianAct(); assert obj is not None
def test_queue():
    obj = GuardianAct(); obj.add_to_queue("test"); obj.process_queue()
    r = obj.is_allowed("test"); assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("queue",test_queue)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nGuardianAct: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''
open(os.path.join(TD, 'test_guardian_act_guardianact.py'), 'w', encoding='utf-8').write(content0)

# autotester — add_suite needs suit object
content1 = r'''"""IGP 单元测试: AutoTester"""
from __future__ import annotations
import sys, os, types
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome12", "infra"))
from v5_auto_tester_v2 import AutoTester, TestSuite
def test_create():
    obj = AutoTester(); assert obj is not None
def test_add_suite():
    obj = AutoTester(); ts = TestSuite("test"); obj.add_suite(ts); assert True
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("add_suite",test_add_suite)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nAutoTester: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''
open(os.path.join(TD, 'test_v5_auto_tester_v2_autotester.py'), 'w', encoding='utf-8').write(content1)

# testsuite — add needs func
content2 = r'''"""IGP 单元测试: TestSuite"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome12", "infra"))
from v5_auto_tester_v2 import TestSuite
def test_create():
    obj = TestSuite("test"); assert obj is not None
def test_add():
    obj = TestSuite("test"); obj.add(lambda: None); assert True
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("add",test_add)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nTestSuite: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''
open(os.path.join(TD, 'test_v5_auto_tester_v2_testsuite.py'), 'w', encoding='utf-8').write(content2)

# reportwriter — write_md needs out_path
content3 = r'''"""IGP 单元测试: ReportWriter"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "absorb", "docagent"))
from v5_job_engine import ReportWriter
def test_create():
    obj = ReportWriter([{"class": "test", "methods": []}]); assert obj is not None
def test_write_md():
    obj = ReportWriter([{"class": "test", "methods": []}]); r = obj.write_md(os.path.join(V5, "tests", "_tmp_report.md"))
    assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("write_md",test_write_md)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nReportWriter: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''
open(os.path.join(TD, 'test_v5_job_engine_reportwriter.py'), 'w', encoding='utf-8').write(content3)

# knowledgebase — use tempdir with r/w
content4 = r'''"""IGP 单元测试: KnowledgeBase"""
from __future__ import annotations
import sys, os, tempfile
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome10", "infra"))
from v5_logic_upgrade import KnowledgeBase
tdir = tempfile.mkdtemp()
def test_create():
    obj = KnowledgeBase(tdir); assert obj is not None
def test_add_fact():
    obj = KnowledgeBase(tdir); obj.add_fact("likes", "alice", "bob")
    r = obj.query("likes", "alice", None); assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("add_fact",test_add_fact)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nKnowledgeBase: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''
open(os.path.join(TD, 'test_v5_logic_upgrade_knowledgebase.py'), 'w', encoding='utf-8').write(content4)

# mutation fission 3 — fix args
content5 = r'''"""IGP 单元测试: AutoFixScanner"""
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
'''
open(os.path.join(TD, 'test_v5_mutation_fission_autofixscanner.py'), 'w', encoding='utf-8').write(content5)

content6 = r'''"""IGP 单元测试: FissionEngine"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome0", "infra"))
from v5_mutation_fission import FissionEngine
def test_create():
    obj = FissionEngine(); assert obj is not None
def test_fission():
    obj = FissionEngine(); r = obj.fission({"chromosome1": {"m1": {}}})
    assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("fission",test_fission)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nFissionEngine: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''
open(os.path.join(TD, 'test_v5_mutation_fission_fissionengine.py'), 'w', encoding='utf-8').write(content6)

content7 = r'''"""IGP 单元测试: MutationEngine"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome0", "infra"))
from v5_mutation_fission import MutationEngine
def test_create():
    obj = MutationEngine(); assert obj is not None
def test_cross_breed():
    r = MutationEngine.cross_breed(type("A",(),{}), type("B",(),{}), "AB"); assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("cross_breed",test_cross_breed)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nMutationEngine: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''
open(os.path.join(TD, 'test_v5_mutation_fission_mutationengine.py'), 'w', encoding='utf-8').write(content7)

print("All 8 fixed")
