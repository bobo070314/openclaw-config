"""Debug BugDoctor test under exec mode"""
import sys, os, tempfile, traceback

def _bd(code):
    V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
    src = os.path.join(V5, 'chromosomes', 'chromosome9', 'infra', 'v5_bug_doctor.py')
    ns = {}
    exec(open(src, 'r', encoding='utf-8').read(), ns)
    BugDoctor = ns['BugDoctor']
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(code); tmp = f.name
    try:
        d = BugDoctor()
        b = d.scan_file(tmp)
        return b
    except Exception as e:
        traceback.print_exc()
        raise
    finally:
        os.unlink(tmp)

try:
    r = _bd("def run(c): return eval(c)\n")
    print(f"Result ({len(r)}): {[str(x) for x in r]}")
except:
    pass
