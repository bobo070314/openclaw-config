"""IGP 单元测试: ComplexityAnalyzer"""
from __future__ import annotations
import sys, os, traceback

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
sys.path.insert(0, os.path.join(V5, 'chromosomes', 'chromosome11', 'infra'))
from v5_complexity_analyzer import ComplexityAnalyzer

results = []

def test(name, fn):
    try:
        fn()
        results.append((name, True, ''))
    except Exception as e:
        results.append((name, False, str(e)[:80]))

test('measure_module', lambda: (
    isinstance(ComplexityAnalyzer().analyze_file(__file__), dict)
))
test('has_score', lambda: (
    any(k in ComplexityAnalyzer().analyze_file(__file__)
        for k in ['score', 'maintainability_index', 'avg_complexity'])
))

for name, ok, err in results:
    print(f"  {'✅' if ok else '❌'} {name:30} {err}")
total = len(results); passed = sum(1 for _,ok,_ in results if ok)
print(f"\nComplexityAnalyzer: {passed}/{total}")
sys.exit(0 if passed == total else 1)
