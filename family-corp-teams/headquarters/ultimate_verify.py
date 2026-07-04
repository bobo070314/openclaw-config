"""终极验证 — 所有核心脚本一次性跑通检查"""
import subprocess, sys, json, time, os

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'

targets = [
    ('DocMind v1', os.path.join(FAMILY, 'projects', 'igp-docmind', 'docmind.py')),
    ('DocMind v2', os.path.join(FAMILY, 'projects', 'igp-docmind', 'docmind_v2.py')),
    ('DocMind v3', os.path.join(FAMILY, 'projects', 'igp-docmind', 'docmind_v3.py')),
    ('Pipeline', os.path.join(FAMILY, 'projects', 'igp-docmind', 'pipeline_integrate.py')),
    ('Ghost', os.path.join(FAMILY, 'projects', 'igp-ghost', 'ghost.py')),
    ('D2A', os.path.join(FAMILY, 'projects', 'igp-d2a', 'agent_protocol.py')),
    ('Genesis', os.path.join(FAMILY, 'projects', 'igp-genesis', 'genesis.py')),
    ('Evolver', os.path.join(FAMILY, 'projects', 'igp-evolver', 'evolver.py')),
    ('Mutation', os.path.join(FAMILY, 'projects', 'igp-mutation', 'mutate.py')),
    ('Harbinger', os.path.join(FAMILY, 'headquarters', 'harbinger.py')),
    ('RealScore', os.path.join(FAMILY, 'headquarters', 'realscore.py')),
    ('Oracle', os.path.join(FAMILY, 'headquarters', 'oracle.py')),
]

env = {**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'}

results = []
print('IGP 全面验证 — 12核武器齐射')
print('=' * 50)
print()

for name, path in targets:
    if not os.path.exists(path):
        print(f'  -- {name:15s} | 文件不存在: {path}')
        continue
    
    start = time.time()
    try:
        proc = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=120, env=env)
        elapsed = round(time.time() - start, 2)
        ok = proc.returncode == 0
        output_line = proc.stdout.split('\n')[1] if proc.stdout else '(silent)'
    except subprocess.TimeoutExpired:
        elapsed = round(time.time() - start, 2)
        ok = False
        output_line = '(timeout)'
    except Exception as e:
        elapsed = round(time.time() - start, 2)
        ok = False
        output_line = str(e)[:60]
    
    lines = len(open(path).readlines())
    mark = '  ✅' if ok else '  ❌'
    print(f'{mark} {name:15s} | {elapsed:>5.1f}s | {lines:>4d}行 | {output_line.strip()[:70]}')
    results.append({'name': name, 'ok': ok, 'time': elapsed, 'lines': lines})

total = sum(1 for r in results if r['ok'])
total_lines = sum(r['lines'] for r in results)
total_time = round(sum(r['time'] for r in results), 1)

print()
print('=' * 50)
print(f'🏆 验证完成: {total}/{len(results)} 通过 ({round(total/len(results)*100)}%)')
print(f'📊 总计: {total_lines}行 Python | 耗时: {total_time}s | 0 Token')
print(f'📦 项目数: 8 | Agent集群: DocMind v3 (4自我复制Agent)')
