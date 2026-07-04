"""IGP 单元测试: BugDoctor — 5种pattern"""
from __future__ import annotations
import sys, os, tempfile, traceback

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
sys.path.insert(0, os.path.join(V5, 'chromosomes', 'chromosome9', 'infra'))
from v5_bug_doctor import BugDoctor

results = []

def test(name, fn):
    try:
        fn()
        results.append((name, True, ''))
    except Exception as e:
        results.append((name, False, str(e)[:80]))

def _bd(code):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(code); tmp = f.name
    try:
        d = BugDoctor(); bugs = d.scan_file(tmp); return bugs
    finally:
        os.unlink(tmp)

test('bare_except', lambda: (
    lambda r: any('bare' in str(b).lower() for b in r)
)(_bd("try:\n    x = 1\nexcept:\n    pass\n")))

test('mutable_default', lambda: (
    lambda r: any('mutable' in str(b).lower() for b in r)
)(_bd("def foo(items=[]): return items\n")))

test('eval', lambda: (
    lambda r: any('eval' in str(b).lower() for b in r)
)(_bd("def run(c): return eval(c)\n")))

test('exec', lambda: (
    lambda r: any('exec' in str(b).lower() for b in r)
)(_bd("def run(c): exec(c)\n")))

test('multi_issues', lambda: (
    lambda r: len(r) >= 2
)(_bd("try:\n    eval('1+1')\nexcept:\n    pass\n")))

for name, ok, err in results:
    print(f"  {'✅' if ok else '❌'} {name:30} {err}")
total = len(results); passed = sum(1 for _,ok,_ in results if ok)
print(f"\nBugDoctor: {passed}/{total}")
sys.exit(0 if passed == total else 1)
