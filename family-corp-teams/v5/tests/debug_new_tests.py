"""Debug batch tests — check first err"""
import subprocess, sys, os

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
td = os.path.join(V5, 'tests')
new_tests = [f for f in sorted(os.listdir(td)) if f.startswith('test_') and f.endswith('.py')
             and f not in ['test_bug_doctor.py','test_complexity_analyzer.py','test_lifecycle.py',
                           'test_prd_queue.py','test_symbolic_engine.py','run_tests.py',
                           'debug_loader.py','debug_bugdoctor.py','debug_loader2.py',
                           'debug_fix_job.py','fix_syntaxwarn_jobengine.py','verify_6_chromosomes.py',
                           'check_health.py']]

for tf in new_tests[:3]:
    path = os.path.join(td, tf)
    r = subprocess.run([sys.executable, '-W', 'ignore', '-u', path], capture_output=True, timeout=10, text=True, encoding='utf-8')
    err = (r.stderr or '')[:300]
    print(f"=== {tf} === exit={r.returncode}")
    print(f"  {err}")
