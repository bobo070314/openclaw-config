"""Debug scan_file for eval pattern"""
import sys, os, tempfile
sys.path.insert(0, r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome9\infra')
from v5_bug_doctor import BugDoctor

code = "def run(c): return eval(c)\n"
with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(code); tmp = f.name

d = BugDoctor()
bugs = d.scan_file(tmp)
os.unlink(tmp)

print(f"bugs: {len(bugs)}")
for b in bugs:
    print(f"  pattern={b['pattern']} line={b['line']} match={b['match']}")
