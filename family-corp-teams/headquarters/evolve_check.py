"""
IGP 活体进化指令 — 全部门/全项目级同步

不是脚本互相喂饭，是每个部门要做自己的独立进化分支：
  - 吸收不同领域的技术
  - 完全不同的世界观
  - 竞争出最优方向

当前可分配方向:
1. 金融风险评估（吞噬Bloomberg/量化）
2. 生物信息学（吞噬DNA对齐/蛋白质折叠）
3. 音乐/音频分析（吞噬MIDI/频谱分析）
4. 网络安全分析（吞噬日志分析/入侵检测）
5. 代码审计（吞噬AST/静态分析）
6. 知识图谱构建（吞噬neo4j/图算法）

先确认当前全貌再分配
"""
import os, json, subprocess, sys, time
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
HQ = os.path.join(FAMILY, 'headquarters')
PROJECTS = os.path.join(FAMILY, 'projects')

# 检查当前有什么
env = {**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'}

def run_script(path, timeout=20):
    if not os.path.exists(path):
        return None, 'not_found'
    try:
        start = time.time()
        proc = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout, env=env)
        return proc.returncode == 0, round(time.time() - start, 2)
    except subprocess.TimeoutExpired:
        return False, f'timeout>{timeout}s'
    except Exception as e:
        return False, str(e)[:40]

def count_project(p):
    pp = os.path.join(PROJECTS, p)
    py_files = [f for f in os.listdir(pp) if f.endswith('.py')] if os.path.isdir(pp) else []
    lines = 0
    for f in py_files:
        try:
            lines += len(open(os.path.join(pp, f)).readlines())
        except:
            pass
    return len(py_files), lines

print(f'IGP 活体进化检查 — {datetime.now().strftime("%H:%M:%S")}')
print('=' * 50)

# 1. 所有项目状态
projects = sorted(os.listdir(PROJECTS)) if os.path.isdir(PROJECTS) else []
print(f'\n项目数: {len(projects)}')
for p in projects:
    py_count, lines = count_project(p)
    ok, runtime = run_script(os.path.join(PROJECTS, p, f'{p.replace("igp-", "").replace("-", "_")}.py') 
        if p.startswith('igp-') else os.path.join(PROJECTS, p, '__init__.py'), 10)
    if not ok:
        # 尝试找__main__块
        for f in ['agent_protocol.py', 'bridge.py', 'bridge_v2.py', 'docmind.py', 'docmind_v4.py', 'init.py']:
            fp = os.path.join(PROJECTS, p, f)
            ok, runtime = run_script(fp, 10)
            if ok:
                break
    status = '✅' if ok else '   '
    rt = runtime if isinstance(runtime, (int, float)) else 0
    print(f'  {status} {p:25s} | {py_count}个文件 | {lines:>4d}行 | {rt}s')

# 2. HQ
print(f'\nHQ脚本状态:')
hq_files = [f for f in sorted(os.listdir(HQ)) if f.endswith('.py') and not f.startswith('_')]
for f in hq_files:
    fp = os.path.join(HQ, f)
    lines = len(open(fp).readlines())
    print(f'  {f:30s} | {lines:>4d}行')

# 3. 可分配方向
print(f'\n可部署方向:')
directions = [
    ('金融风控',  '吞噬Quant/金融模型'),
    ('DNA进化',   '吞噬基因组对齐'),
    ('音频分析',  '吞噬MIDI/频谱'),
    ('安全审计',  '吞噬入侵检测'),
    ('代码AST',   '吞噬静态分析'),
    ('知识图谱',  '吞噬图算法'),
]
for i, (d, desc) in enumerate(directions, 1):
    print(f'  {i}. {d:12s} → {desc}')

print(f'\nOK。')
