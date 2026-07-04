"""IGP V5 染色体状态面板 — 独立运行，0错误"""
import subprocess, sys, os, json

BASE = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'

CHROMOSOMES = [
    ('chromosome1',  'MCP生态部'),
    ('chromosome2',  'A2A联邦部'),
    ('chromosome3',  'Skills市场部'),
    ('chromosome4',  'Provider路由部'),
    ('chromosome5',  '安全Guardian部'),
    ('chromosome6',  '商业协议部'),
    ('chromosome7',  'Agent OS层'),
    ('chromosome8',  'AP2支付协议'),
    ('chromosome9',  '代码修补部'),
    ('chromosome10', '逻辑推理部'),
    ('chromosome11', '类型/度量部'),
    ('chromosome12', '自动测试部'),
]

all_pass = True

print('='*60)
print('  IGP V5 染色体状态面板')
print(f'  时间: ', end='')
subprocess.run([sys.executable, '-c', 'from datetime import *; print(datetime.now().strftime("%H:%M:%S"))'],
               timeout=5)

for cid, cname in CHROMOSOMES:
    run_py = os.path.join(BASE, 'chromosomes', cid, 'infra', 'run.py')
    
    if not os.path.isfile(run_py):
        print(f'  ❌ {cid}: {cname} — run.py 不存在')
        all_pass = False
        continue
    
    result = subprocess.run(
        [sys.executable, run_py],
        capture_output=True, text=True, timeout=30,
        encoding='utf-8', cwd=os.path.dirname(run_py)
    )
    
    passed = result.returncode == 0
    if not passed:
        all_pass = False
    
    # 提取关键行
    summary = ''
    if result.stdout:
        for line in result.stdout.split('\n'):
            for kw in ['验证通过', '通过率', '评分', 'ALL PASSED']:
                if kw in line:
                    summary = line.strip()
                    break
            if summary:
                break
    
    mark = '✅' if passed else '❌'
    extra = f' | {summary[:60]}' if summary else ''
    print(f'  {mark} {cid}: {cname}{extra}')

print()
if all_pass:
    print('  🏆 全链通过! 12/12')
else:
    print('  ❌ 存在失败项')
print('='*60)
