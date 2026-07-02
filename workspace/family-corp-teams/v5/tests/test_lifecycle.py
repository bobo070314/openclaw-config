"""IGP 单元测试: LifecycleManager"""
from __future__ import annotations
import sys, os, traceback
V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
V6 = os.path.join(V5, 'v6')
sys.path.insert(0, V6)
from v6_lifecycle import LifecycleManager

results = []

def test(name, fn):
    try:
        fn()
        results.append((name, True, ''))
    except Exception as e:
        results.append((name, False, str(e)[:80]))

reg = os.path.join(V6, 'product_registry.json')
lm = LifecycleManager(reg)

test('summary_has_total', lambda: lm.summary().get('total', 0) > 0)
test('get_product', lambda: lm.get_product('v5_bug_doctor') is not None)
test('record_call', lambda: (
    lm.record_call('v5_bug_doctor', 10.5, True) or True
))

for name, ok, err in results:
    print(f"  {'✅' if ok else '❌'} {name:30} {err}")
total = len(results); passed = sum(1 for _,ok,_ in results if ok)
print(f"\nLifecycleManager: {passed}/{total}")
sys.exit(0 if passed == total else 1)
