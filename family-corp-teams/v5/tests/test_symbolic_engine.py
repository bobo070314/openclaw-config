"""IGP 单元测试: SymbolicEngine"""
from __future__ import annotations
import sys, os
V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
sys.path.insert(0, os.path.join(V5, 'chromosomes', 'chromosome10', 'infra'))
from v5_symbolic_engine import SymbolicEngine

results = []

def test(name, fn):
    try:
        fn()
        results.append((name, True, ''))
    except Exception as e:
        results.append((name, False, str(e)[:80]))

test('create_engine', lambda: isinstance(SymbolicEngine(), SymbolicEngine))
test('add_constraint', lambda: (
    (lambda se: se.add_constraint('x > 5') or se.solve() is not None)(SymbolicEngine())
))

for name, ok, err in results:
    print(f"  {'✅' if ok else '❌'} {name:30} {err}")
total = len(results); passed = sum(1 for _,ok,_ in results if ok)
print(f"\nSymbolicEngine: {passed}/{total}")
sys.exit(0 if passed == total else 1)
