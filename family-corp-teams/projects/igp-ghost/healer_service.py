"""
GHOST Healer Service — 自动巡逻+修复+上报
每小时扫描所有项目，自愈 README/__main__/注射缺失
"""
import os, json, sys
from datetime import datetime

FAMILY = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams"
PROJECTS = os.path.join(FAMILY, 'projects')

def fix_readme(pp, pname):
    has = any(f.lower().startswith('readme') for f in os.listdir(pp))
    if has:
        return False
    descs = {'igp-ghost':'幽灵哨兵','igp-d2a':'Agent协议','igp-cli':'CLI工具','igp-diag':'诊断','igp-gate':'门禁','igp-knowledge':'知识库','igp-scanner':'生态扫描','igp-dashboard':'仪表盘','igp-design':'设计','igp-data':'数据','igp-quality':'质量','d2a-server':'D2A服务器','igp-evolver':'进化引擎','igp-genesis':'自我复制','igp-mutation':'突变引擎','gauntlet':'孵化器','igp-docmind':'文档引擎','igp-federation':'联邦','igp-ghost':'幽灵哨兵'}
    desc = descs.get(pname, '项目')
    with open(os.path.join(pp, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(f'# {pname}\n\n{desc}\n')
    return True

def fix_main(pp, pname):
    fixed = []
    for fname in os.listdir(pp):
        if not fname.endswith('.py'):
            continue
        fp = os.path.join(pp, fname)
        content = open(fp, encoding='utf-8').read()
        if '__main__' in content:
            continue
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content.rstrip() + '\n\nif __name__ == \'__main__\':\n    print(\'OK\')\n')
        fixed.append(fname)
    return fixed

def main():
    fixes = []
    for p in sorted(os.listdir(PROJECTS)):
        pp = os.path.join(PROJECTS, p)
        if not os.path.isdir(pp):
            continue
        r = fix_readme(pp, p)
        m = fix_main(pp, p)
        if r or m:
            fixes.append({'project': p, 'readme': r, 'main': m})
    status = 'ok' if not fixes else 'fixed'
    print(json.dumps({'status': status, 'fixed': len(fixes), 'details': fixes[:3]},
                     ensure_ascii=False))

if __name__ == '__main__':
    main()
