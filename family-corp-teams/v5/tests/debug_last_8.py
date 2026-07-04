"""Quick fix last 8 failures"""
import subprocess, sys, os

TD = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\tests'

# Get exact failure messages
fails = ['test_guardian_act_guardianact.py', 'test_v5_auto_tester_v2_autotester.py',
         'test_v5_auto_tester_v2_testsuite.py', 'test_v5_job_engine_reportwriter.py',
         'test_v5_logic_upgrade_knowledgebase.py',
         'test_v5_mutation_fission_autofixscanner.py', 'test_v5_mutation_fission_fissionengine.py',
         'test_v5_mutation_fission_mutationengine.py']

for tf in fails:
    path = os.path.join(TD, tf)
    r = subprocess.run([sys.executable, '-W', 'ignore', '-u', path], capture_output=True, timeout=10, text=True, encoding='utf-8')
    err = (r.stderr or '')[:200]
    out = r.stdout or ''
    fail_line = [l for l in out.split('\n') if 'FAIL' in l]
    print(f'--- {tf} ---')
    for fl in fail_line:
        print(f'  {fl.strip()}')
    if err:
        print(f'  ERR: {err[:150]}')
