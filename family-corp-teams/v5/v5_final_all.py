"""IGP V5 终极全量验证 —— 12染色体全链路贯通"""
import subprocess, sys, os, json, time

BASE = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
CHROMOSOMES = [
    ('chromosome1',  'MCP生态部',     'igp_mcp_v5_server.py'),
    ('chromosome2',  'A2A联邦部',     'a2a_v2_upgrade.py'),
    ('chromosome3',  'Skills市场部',   'skill_package.py'),
    ('chromosome4',  'Provider路由部', 'provider_router.py'),
    ('chromosome5',  '安全Guardian部', 'guardian_policy.py'),
    ('chromosome6',  '商业协议部',     'agent_commerce_v2.py'),
    ('chromosome7',  'Agent OS层',     'agent_os_kernel.py'),
    ('chromosome8',  'AP2支付协议',    'ap2_protocol.py'),
    ('chromosome9',  '代码修补部',     'v5_bug_doctor.py'),
    ('chromosome10', '逻辑推理部',     'v5_symbolic_engine.py'),
    ('chromosome11', '类型/度量部',    'v5_complexity_analyzer.py'),
    ('chromosome12', '自动测试部',     'v5_auto_tester.py'),
]

print('='*60)
print('  🏆  IGP V5 终极全量验证')
print('  12条染色体 | 闭环7步流水线')
print('  时间:', time.strftime('%H:%M:%S'))
print('='*60)

results = {'passed': 0, 'failed': 0, 'total': 0}

for cid, cname, src in CHROMOSOMES:
    run_py = os.path.join(BASE, 'chromosomes', cid, 'infra', 'run.py')
    src_py = os.path.join(BASE, 'chromosomes', cid, 'infra', src)
    
    # 检查文件存在
    files_exist = os.path.isfile(run_py) and os.path.isfile(src_py)
    
    # 运行验证
    if files_exist:
        r = subprocess.run([sys.executable, run_py], capture_output=True, text=True, 
                          timeout=30, encoding='utf-8', cwd=os.path.dirname(run_py))
        passed = r.returncode == 0
    else:
        passed = False
        r = subprocess.CompletedProcess(args=[], returncode=1, stdout='', stderr='Missing files')
    
    status = '✅' if passed else '❌'
    results['total'] += 1
    if passed:
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # 提取关键行
    key_lines = ''
    if r.stdout:
        for line in r.stdout.split('\n'):
            if '验证通过' in line or '通过率' in line or 'ALL PASSED' in line or '评分' in line:
                key_lines = line.strip()
                break
    if not key_lines and r.stdout:
        last_lines = [l.strip() for l in r.stdout.split('\n')[-3:] if l.strip()]
        key_lines = last_lines[-1] if last_lines else ''
    
    print(f'  {status} {cid}: {cname} | {key_lines or r.stdout[:60]}')

print(f'\n  结果: {results["passed"]}/{results["total"]} 通过')
print(f'  {"🏆 全链路贯通!" if results["failed"] == 0 else "❌ 有失败项"}' )
print('='*60)

# 最终报告
report = {
    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
    'total': results['total'],
    'passed': results['passed'],
    'failed': results['failed'],
    'verdict': 'ALL_PASSED' if results['failed'] == 0 else 'PARTIAL_FAILURE',
}
report_path = os.path.join(BASE, 'V5_FINAL_REPORT.json')
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f'  报告: {report_path}')
