"""Debug individual test failures"""
import subprocess, sys, os

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
td = os.path.join(V5, 'tests')

fails = [
    'test_code_analyzer.py',
    'test_fastmcp_exporter.py',
    'test_smart_router.py',
    'test_guardian_policy.py',
    'test_incremental_scanner.py',
    'test_logger_context.py',
    'test_mcp_client.py',
    'test_result_monad.py',
    'test_agent_commerce.py',
    'test_commerce_pk.py',
]

for f in fails:
    path = os.path.join(td, f)
    r = subprocess.run([sys.executable, '-W', 'ignore', '-u', path], capture_output=True, timeout=10, text=True, encoding='utf-8')
    out = r.stdout.strip() if r.stdout else ''
    err = r.stderr.strip() if r.stderr else ''
    err_short = err[:300] if err else ''
    
    # find which test failed
    last_lines = out.split('\n')[-5:] if out else []
    result_line = last_lines[-1] if last_lines else ''
    
    print(f"=== {f} === exit={r.returncode}")
    if err_short:
        print(f"  ERR: {err_short}")
    else:
        print(f"  OUT: {result_line}")
        # show FAIL lines
        for li in last_lines[:-1]:
            if 'FAIL' in li:
                print(f"  {li.strip()}")
