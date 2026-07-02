"""IGP 单元测试: PRDQueue"""
from __future__ import annotations
import sys, os
V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
V6 = os.path.join(V5, 'v6')
sys.path.insert(0, V6)
sys.path.insert(0, os.path.join(V6, 'prd'))
from prd_queue import PRDQueue

results = []

def test(name, fn):
    try:
        fn()
        results.append((name, True, ''))
    except Exception as e:
        results.append((name, False, str(e)[:80]))

q = PRDQueue(V6)
test('submit_prd', lambda: 'id' in q.submit(department='test', product='test', title='test'))
test('list_returns_dict', lambda: isinstance(q.list_all(), dict))
test('summary', lambda: isinstance(q.summary(), dict) and 'total' in q.summary())

for name, ok, err in results:
    print(f"  {'✅' if ok else '❌'} {name:30} {err}")
total = len(results); passed = sum(1 for _,ok,_ in results if ok)
print(f"\nPRDQueue: {passed}/{total}")
sys.exit(0 if passed == total else 1)
