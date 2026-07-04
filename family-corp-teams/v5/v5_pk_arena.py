#!/usr/bin/env python3
"""IGP V5 每日淘汰赛场 —— 计时+排名+淘汰池"""
import os, sys, json, subprocess
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
CHROMO_DIR = os.path.join(BASE, 'chromosomes')
RANKING_FILE = os.path.join(BASE, 'v5_arena_ranking.json')
POOL_FILE = os.path.join(BASE, 'v5_elimination_pool.json')

CHROMOSOMES = {
    '1': 'MCP生态部', '2': 'A2A联邦部', '3': 'Skills市场部',
    '4': 'Provider路由部', '5': '安全Guardian部', '6': '商业协议部',
    '7': 'Agent OS层', '8': 'AP2支付协议',
}

now = lambda: datetime.now(timezone.utc)
today = lambda: now().strftime('%Y-%m-%d')

def run_chromosome(cid, cname):
    """跑一条染色体的run.py，返回(通过数, 总数)"""
    run_py = os.path.join(CHROMO_DIR, f'chromosome{cid}', 'infra', 'run.py')
    run_v2 = os.path.join(CHROMO_DIR, f'chromosome{cid}', 'infra', 'run_v2.py')
    fp = run_v2 if cid == '6' and os.path.exists(run_v2) else run_py
    if not os.path.exists(fp):
        return 0, 1
    try:
        r = subprocess.run([sys.executable, fp], capture_output=True, text=True, timeout=15, encoding='utf-8',
                          cwd=os.path.dirname(fp))
        if r.returncode == 0:
            return 1, 1  # run.py整体算1个测试
        else:
            return 0, 1
    except subprocess.TimeoutExpired:
        return 0, 1

def main():
    print('='*60)
    print('  🏟️ IGP V5 DAILY ARENA — 淘汰赛')
    print(f'  日期: {today()}')
    print('='*60)

    results = {}
    for cid, cname in sorted(CHROMOSOMES.items()):
        passed, total = run_chromosome(cid, cname)
        results[cname] = {'passed': passed, 'total': total, 'id': cid}
        icon = '✅' if passed == total else '❌'
        print(f'  {icon} #{cid} {cname:16s} {passed}/{total}')

    # 排序
    sorted_results = sorted(results.items(), key=lambda x: (-x[1]['passed'], x[1]['id']))

    print(f'\n{"="*60}')
    print('  🏆 排行榜')
    print('='*60)
    medals = ['🥇', '🥈', '🥉']
    for i, (name, info) in enumerate(sorted_results):
        prefix = medals[i] if i < 3 else f'  {i+1}.'
        print(f'  {prefix} {name:16s} {info["passed"]}/{info["total"]} {"✅" if info["passed"]==info["total"] else "❌"}')

    # 淘汰池
    last = sorted_results[-1]
    pool = {'date': today(), 'eliminated': [], 'observe': []}
    if last[1]['passed'] < last[1]['total']:
        pool['observe'].append(last[0])
        print(f'\n  ⚠️ 淘汰观察池: {last[0]}')

    # 读取历史淘汰池
    if os.path.exists(POOL_FILE):
        with open(POOL_FILE, 'r') as f:
            history = json.load(f)
        if not isinstance(history, list):
            history = [history]
        history.append(pool)
    else:
        history = [pool]

    # 连续2次垫底检查
    if len(history) >= 2:
        last_two = [h.get('observe', []) for h in history[-2:]]
        if last_two[0] and last_two[1] and last_two[0] == last_two[1]:
            print(f'  🔴 NOTICE: {last_two[0]} 连续2次垫底，建议人工核查')

    with open(POOL_FILE, 'w') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    # 保存本次排名
    ranking = {name: info for name, info in sorted_results}
    with open(RANKING_FILE, 'w') as f:
        json.dump({'date': today(), 'ranking': ranking}, f, ensure_ascii=False, indent=2)

    print(f'\n  📝 排名: {RANKING_FILE}')
    print(f'  📝 淘汰池: {POOL_FILE}')
    print('='*60)

if __name__ == '__main__':
    main()
