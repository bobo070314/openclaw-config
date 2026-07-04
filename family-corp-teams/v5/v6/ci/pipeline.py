"""IGP CI/CD 流水线 — 自动测试→构建→部署"""
from __future__ import annotations
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
V6 = os.path.join(V5, 'v6')

sys.path.insert(0, V6)
sys.path.insert(0, os.path.join(V6, 'review'))
sys.path.insert(0, os.path.join(V6, 'prd'))
sys.path.insert(0, os.path.join(V5, 'chromosomes', 'chromosome9', 'infra'))
sys.path.insert(0, os.path.join(V5, 'chromosomes', 'chromosome0', 'infra'))
sys.path.insert(0, os.path.join(V5, 'chromosomes', 'chromosome11', 'infra'))

steps = []

def step(name, fn):
    steps.append((name, fn))

sys.path.insert(0, os.path.join(V5, 'tests'))

# Phase 1: Tests
step("BugDoctor单元测试", lambda: os.system(f'{sys.executable} -W ignore -u "{os.path.join(V5, "tests", "test_bug_doctor.py")}"') == 0)
step("代码分析", lambda: (
    __import__('v5_code_analyzer').CodeAnalyzer(V5).scan_bad_patterns(),
    True
))
step("复杂度计算", lambda: (
    __import__('v5_complexity_analyzer').ComplexityAnalyzer().analyze_file(__file__),
    True
))

# Phase 2: Build
step("生命周期验证", lambda:
    __import__('v6_lifecycle').LifecycleManager(
        os.path.join(V6, 'product_registry.json')
    ).summary()['total'] > 50
)
step("三Agent评审存活", lambda:
    __import__('v6_review_agents').review_file(
        os.path.join(V6, 'v6_lifecycle.py')
    )['passed'] == True
)
step("PRD队列存活", lambda:
    __import__('prd_queue').PRDQueue(V6).summary()['total'] >= 0
)

# Phase 3: API
def api_get(path):
    try:
        r = urllib.request.urlopen(f'http://localhost:8080{path}', timeout=3)
        return json.loads(r.read().decode('utf-8'))
    except Exception:
        return {"error": "unreachable"}

step("API health", lambda: api_get('/api/v1/health').get('status') == 'ok')
step("API lifecycle", lambda: api_get('/api/v1/lifecycle').get('total', 0) > 50)
step("API version", lambda: 'version' in api_get('/api/v1/version/v5_bug_doctor'))

print('=' * 55)
print('IGP CI/CD Pipeline')
print('=' * 55)

passed = 0
for name, fn in steps:
    try:
        ok = fn()
        print(f"  {'✅' if ok else '❌'} {name:35}")
        if ok:
            passed += 1
        else:
            print(f"       (返回False)")
    except Exception as e:
        print(f"  {'❌'} {name:35} {str(e)[:60]}")

print(f'= {"="*53}')
print(f"  Passed: {passed}/{len(steps)}")
print(f"  {'✅ Deployable' if passed == len(steps) else '⚠️ ' + str(len(steps)-passed) + ' failed'}")

report = {
    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
    "passed": passed,
    "total": len(steps),
    "deployable": passed == len(steps)
}
with open(os.path.join(V6, 'ci', 'last_build.json'), 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False)
print(f"\nBuild report: {os.path.join(V6, 'ci', 'last_build.json')}")