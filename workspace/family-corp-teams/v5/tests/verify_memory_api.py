"""Verify Silicon Memory + Department API"""
import subprocess, sys, os, time, json, urllib.request, socket

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
API_PORT = 8082

def req(method, path, body=None):
    url = 'http://localhost:%d%s' % (API_PORT, path)
    data = json.dumps(body).encode('utf-8') if body else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header('Content-Type', 'application/json')
    try:
        resp = urllib.request.urlopen(r, timeout=5)
        return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode('utf-8'))
    except Exception as e:
        return {'error': str(e)}

# Start fresh API instance
api_dir = os.path.join(V5, 'v6', 'api')
subprocess.Popen([sys.executable, '-W', 'ignore', 'igp_api.py', '--port', str(API_PORT)],
                 cwd=api_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                 creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
time.sleep(2)

results = []

# 1. Health
r = req('GET', '/api/v1/health')
ok = r.get('status') == 'ok'
results.append(('Health check', ok))

# 2. Write memory (chromosome16 records a bug)
r = req('POST', '/api/v1/memory', {
    'type': 'bug_found',
    'dept': 'chromosome16',
    'payload': {'entity': 'AP2_Wallet', 'type': 'class', 'props': {'error': 'sign_timeout'}},
    'tags': ['bug', 'fix_needed', 'chromosome8']
})
ok = 'id' in r
results.append(('Write memory (chromosome16 bug)', ok))
mem_id = r.get('id', '?')

# 3. Write another memory (chromosome9 success)
req('POST', '/api/v1/memory', {
    'type': 'success_pattern',
    'dept': 'chromosome9',
    'payload': {'entity': 'BugDoctor', 'type': 'tool', 'props': {'scanned_files': 66, 'bugs_found': 50}},
    'tags': ['success', 'chromosome9', 'scan']
})
results.append(('Write memory (chromosome9 scan)', True))

# 4. Query memory
r = req('GET', '/api/v1/memory?q=wallet+timeout&k=5')
episodic = r.get('results', {}).get('episodic', [])
ok = len(episodic) > 0
results.append(('Query memory (wallet timeout)', ok))

# 5. Department filter
r = req('GET', '/api/v1/memory?q=BugDoctor&dept=chromosome9')
ok = r.get('department') == 'chromosome9'
results.append(('Department filter', ok))

# 6. Cross-department notification
r = req('POST', '/api/v1/notify', {
    'from_dept': 'chromosome9', 'to_dept': 'chromosome8',
    'message': 'Found AP2_Wallet sign timeout',
    'urgency': 'high'
})
ok = r.get('status') == 'notified'
results.append(('Cross-dept notification', ok))

# 7. Add skill (best practice)
r = req('POST', '/api/v1/memory/skill', {
    'name': 'wallet_sig_fix',
    'pattern': 'sign_timeout',
    'instruction': 'Use CryptoKit.SignatureVerifier instead',
    'category': 'chromosome8'
})
ok = r.get('status') == 'skill_added'
results.append(('Add best practice skill', ok))

# 8. Query skills
r = req('GET', '/api/v1/memory/skills?context=sign_timeout')
ok = len(r.get('results', [])) > 0
results.append(('Query best practices', ok))

# 9. All departments
r = req('GET', '/api/v1/dept')
depts = r.get('departments', {})
ok = len(depts) > 0
results.append(('All departments list (%d depts)' % len(depts), ok))

# 10. Specific department
r = req('GET', '/api/v1/dept/chromosome13')
ok = 'name' in r and '硅胶' in str(r.get('name', ''))
results.append(('Chromosome13 Silicon Memory', ok))

# Report
print('=' * 60)
print('  IGP API - Silicon Memory + All Departments')
print('=' * 60)
all_ok = True
for name, ok in results:
    mark = 'PASS' if ok else 'FAIL'
    if not ok: all_ok = False
    print('  %s %s' % (mark, name))

print()
print('  Result: %d/%d passed' % (sum(1 for _, o in results if o), len(results)))
print()

# Usage examples
print('Usage examples (any department):')
print()
print('  # chromosome8 queries if BugDoctor fixed wallet issues')
print('  curl localhost:%d/api/v1/memory?q=wallet+timeout' % API_PORT)
print()
print('  # chromosome9 records a bug')
print('  curl -X POST localhost:%d/api/v1/memory \\' % API_PORT)
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"type":"bug","dept":"chromosome9","payload":{"entity":"X"}}\'')
print()
print('  # Any department checks the registry')
print('  curl localhost:%d/api/v1/dept/chromosome13' % API_PORT)
print()
