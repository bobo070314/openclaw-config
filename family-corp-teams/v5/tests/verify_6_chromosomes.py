"""验证6个染色体修复"""
import subprocess, sys, os

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
checks = {
    'chromosome3 (Skills市场部)': os.path.join(V5, 'chromosomes', 'chromosome3', 'infra', 'run.py'),
    'chromosome4 (Provider路由部)': os.path.join(V5, 'chromosomes', 'chromosome4', 'infra', 'run.py'),
    'chromosome7 (Agent OS层)': os.path.join(V5, 'chromosomes', 'chromosome7', 'infra', 'run.py'),
    'chromosome8 (AP2支付协议)': os.path.join(V5, 'chromosomes', 'chromosome8', 'infra', 'run.py'),
    'chromosome14 (智能路由部)': os.path.join(V5, 'chromosomes', 'chromosome14_smart_routing', 'infra', 'run.py'),
    'chromosome15 (审计安全部)': os.path.join(V5, 'chromosomes', 'chromosome15_audit_security', 'infra', 'run.py'),
}

all_ok = True
for name, path in checks.items():
    r = subprocess.run([sys.executable, '-W', 'ignore', '-u', path], capture_output=True, timeout=10, text=True, encoding='utf-8')
    ok = r.returncode == 0
    out = (r.stdout or '').strip()
    err = (r.stderr or '').strip()[:100]
    print(f"{'✅' if ok else '❌'} {name:35} exit={r.returncode}")
    if out: print(f"     {out.split(chr(10))[0][:80]}")
    if err: print(f"     err: {err}")
    if not ok: all_ok = False

print(f"\n{'='*50}")
print(f"Total: 6/6 | {'ALL PASS 🏆' if all_ok else 'SOME FAILED ❌'}")
