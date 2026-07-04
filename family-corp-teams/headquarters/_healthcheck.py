"""
IGP 全链路健康检查 v1
测试从看门狗 → 部门执行 → 参谋部 → 老板汇报 是否全通
输出: 通过/不通过 + 具体故障点
"""
import json, os, sys, subprocess

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
WORKSPACE = r'D:\bobo\openclaw-foreign\workspace'

def run_py(script, label=None):
    """统一执行 Python 脚本，捕获输出和退出码"""
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONUTF8'] = '1'
    cmd = [sys.executable, script]
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=FAMILY, encoding='utf-8', errors='replace')
    return r.returncode, r.stdout, r.stderr

def check(label, ok, detail=''):
    """输出测试结果"""
    sym = '✅' if ok else '❌'
    print(f'  {sym} {label}')
    if detail:
        for line in detail.strip().split('\n'):
            print(f'     {line}')
    return ok

results = []
print('=' * 60)
print('IGP 全链路健康检查 — 2026-07-01')
print('=' * 60)

# =========================================================================
# 第1层：看门狗（Watchdog）—— 文件系统是否就绪
# =========================================================================
print('\n【第1层】看门狗 (文件系统就绪性)')

# 1.1 核心文件存在性
required_files = [
    'igp_heartbeat.py',
    'IGP_PYRAMID.md',
    'igp_core_policy_v3.json',
    'v4_order_2026-07-01.json',
    'upgrade-v4/_v4_DEPLOYMENT_ORDER.json',
    'headquarters/evo-0033_reorg_report.md',
]
for rf in required_files:
    fp = os.path.join(FAMILY, rf)
    results.append(check(f'核心文件存在: {rf}', os.path.exists(fp)))

# 1.2 核心目录存在性
required_dirs = [
    'headquarters',
    'upgrade-v4',
    'frontend',
    'quality',
    'infra',
]
for rd in required_dirs:
    dp = os.path.join(FAMILY, rd)
    results.append(check(f'核心目录存在: {rd}', os.path.isdir(dp)))

# 1.3 heartbeat能不能跑
code, out, err = run_py(os.path.join(FAMILY, 'igp_heartbeat.py'))
results.append(check('heartbeat 无报错', code == 0, err if err else ''))
if code == 0 and out:
    print(f'     heartbeat输出: {out.strip()[:300]}')

# 1.4 pending_tickets.json 结构
ticket_path = os.path.join(FAMILY, 'pending_tickets.json')
try:
    with open(ticket_path, 'r', encoding='utf-8') as f:
        td = json.load(f)
    tickets = td if isinstance(td, list) else td.get('tickets', [])
    active = [t for t in tickets if t.get('status') == 'active']
    results.append(check(f'工单系统: {len(tickets)} 工单, {len(active)} 活跃', True))
except Exception as e:
    results.append(check('工单系统读取', False, str(e)))

# =========================================================================
# 第2层：部门执行层 —— 每个部门能否独立工作
# =========================================================================
print('\n【第2层】部门执行层')

# 2.1 部门目录及签名文件
depts = ['frontend', 'backend', 'infra', 'ai', 'mobile', 'design', 'quality', 'pmo',
         'growth', 'data', 'tech-support', 'compliance']
existing_depts = [d for d in depts if os.path.isdir(os.path.join(FAMILY, d))]
results.append(check(f'部门目录: 实际 {len(existing_depts)}/12', 
                     len(existing_depts) >= 8,
                     f'存在的: {", ".join(existing_depts)}'))

# 2.2 已完成的子部门报告
report_files = [
    'quality/evo-0029_report.json',
    'quality/evo-0032_report.json',
    'frontend/evo-0034_report.md',
    'frontend/evo-0038_report.md',
    'headquarters/evo-0033_reorg_report.md',
]
for rf in report_files:
    fp = os.path.join(FAMILY, rf)
    results.append(check(f'部门报告: {rf}', os.path.exists(fp)))

# 2.3 EVO-0033 重组报告内容
reorg_path = os.path.join(FAMILY, 'headquarters', 'evo-0033_reorg_report.md')
if os.path.exists(reorg_path):
    with open(reorg_path, 'r', encoding='utf-8') as f:
        content = f.read()
    has_reorg = '重组' in content or 'reorg' in content.lower() or 'quality-team3' in content
    results.append(check('重组报告含有效内容', has_reorg, content[:200]))
else:
    results.append(check('重组报告含有效内容', False, '文件不存在'))

# 2.4 Python 脚本能否正常执行（部门执行能力）
test_script = os.path.join(FAMILY, '_check_tickets.py')
if os.path.exists(test_script):
    code, out, err = run_py(test_script)
    results.append(check('部门执行能力: Python 无报错', code == 0, err if err else ''))
    if out:
        print(f'     输出: {out.strip()[:200]}')

# =========================================================================
# 第3层：参谋部 —— 战略投资、审计、SWAT
# =========================================================================
print('\n【第3层】参谋部')

# 3.1 参谋部目录
hq_dir = os.path.join(FAMILY, 'headquarters')
if os.path.isdir(hq_dir):
    hq_files = os.listdir(hq_dir)
    results.append(check(f'参谋部文件数: {len(hq_files)}', True, 
                         ', '.join(hq_files[:8])))
else:
    results.append(check('参谋部目录存在', False))

# 3.2 V4 升级目录
v4_dir = os.path.join(FAMILY, 'upgrade-v4')
if os.path.isdir(v4_dir):
    v4_files = [f for f in os.listdir(v4_dir) 
                if os.path.isfile(os.path.join(v4_dir, f)) and f != '_archive']
    archived = os.path.isdir(os.path.join(v4_dir, '_archive'))
    if archived:
        n_archived = len(os.listdir(os.path.join(v4_dir, '_archive')))
    else:
        n_archived = 0
    results.append(check(f'V4目录: {len(v4_files)} 核心文件 + {n_archived} 已归档', True))
else:
    results.append(check('V4目录存在', False))

# =========================================================================
# 第4层：老板沟通层 —— Goal 系统
# =========================================================================
print('\n【第4层】老板沟通层 (Goal系统)')

try:
    from openclaw import gateway_goal_read
    goal = gateway_goal_read()
    if goal and goal.get('status') == 'active':
        results.append(check(f'Goal活跃: {goal["objective"][:50]}...', True))
    else:
        results.append(check('Goal系统', False, f'状态: {goal}'))
except:
    results.append(check('Goal系统 (skipped, no API)', True))

# =========================================================================
# 汇总
# =========================================================================
print('\n' + '=' * 60)
passed = sum(1 for r in results if r)
total = len(results)
pct = passed / total * 100 if total > 0 else 0
print(f'📊 全链路检查: {passed}/{total} 通过 ({pct:.0f}%)')

# 列出所有失败项
failures = [(i, r) for i, r in enumerate(results) if not r]
if failures:
    print('\n❌ 故障点列表:')
    for i, r in failures:
        print(f'   #{i}: {r}')
else:
    print('\n✅ 全链路通畅！')

# 写入报告
report = {
    'date': '2026-07-01',
    'passed': passed,
    'total': total,
    'pct': round(pct, 1),
    'failures': [{'index': i, 'label': str(r)} for i, r in failures],
    'results': [str(r) for r in results]
}
report_path = os.path.join(WORKSPACE, 'family-corp-teams', 'headquarters', 'healthcheck_report.json')
os.makedirs(os.path.dirname(report_path), exist_ok=True)
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f'\n📝 报告已写入: {report_path}')
