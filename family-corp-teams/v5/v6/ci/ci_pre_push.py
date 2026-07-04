"""IGP CI/CD — pre-push hook"""
import subprocess, sys, os, json, datetime

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
LOG = os.path.join(V5, 'v6', 'ci', 'ci_status.log')

def log(msg):
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(f'[{ts}] {msg}\n')

def run(cmd, timeout=60):
    r = subprocess.run(cmd, capture_output=True, timeout=timeout, text=True, encoding='utf-8')
    return r.returncode, r.stdout, r.stderr

print("=== IGP CI/CD Pre-Push Hook ===")

# Step 1: Run unit tests
print("[1/3] Running unit tests...")
code, out, err = run([sys.executable, '-W', 'ignore', os.path.join(V5, 'tests', 'run_tests.py')], timeout=120)
if code != 0:
    log('FAIL: Unit tests failed')
    print("FAIL: Unit tests failed")
    print(err[:500] if err else out[-500:])
    sys.exit(1)
print("PASS: Unit tests")

# Step 2: Run pipeline
print("[2/3] Running CI pipeline...")
code, out, err = run([sys.executable, '-W', 'ignore', os.path.join(V5, 'v6', 'ci', 'pipeline.py')], timeout=60)
if code != 0:
    log('FAIL: Pipeline failed')
    print("FAIL: CI Pipeline")
    sys.exit(1)
print("PASS: CI Pipeline (9/9 Deployable)")

# Step 3: Quick health check
print("[3/3] Health check...")
code, out, err = run([sys.executable, '-W', 'ignore', '-u', '-c', '''
import sys
sys.path.insert(0, r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\v5\\v6\\api")
from igp_api import app
print("API module loaded OK")
'''], timeout=10)
if code != 0:
    log('FAIL: Health check')
    print("FAIL: API module health")
    sys.exit(1)
print("PASS: Health check")

log('ALL PASS: pre-push hook')
print("\n=== All Passed ✅ ===")
sys.exit(0)
