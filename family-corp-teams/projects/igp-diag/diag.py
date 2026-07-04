"""
IGP一键诊断 — 项目健康检查脚本
"""
import os, sys, json
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'

def health_score(project_name):
    pp = os.path.join(FAMILY, 'projects', project_name)
    if not os.path.isdir(pp):
        return 0
    score = 0
    py_files = [f for f in os.listdir(pp) if f.endswith('.py')]
    score += min(len(py_files) * 10, 30)
    total_lines = 0
    has_main = False
    for f in py_files:
        content = open(os.path.join(pp, f), encoding='utf-8').read()
        total_lines += len(content.split('\n'))
        if '__main__' in content:
            has_main = True
    if total_lines > 50:
        score += 20
    if has_main:
        score += 20
    readme = any(f.lower().startswith('readme') for f in os.listdir(pp))
    if readme:
        score += 20
    return min(score, 100)

def main():
    print('IGP 一键诊断\n')
    issues = 0
    for p in sorted(os.listdir(os.path.join(FAMILY, 'projects'))):
        score = health_score(p)
        bar = '█' * (score // 10)
        status = '✅' if score >= 80 else '⚠️' if score >= 60 else '❌'
        print(f'  {status} {p:18s} | {score:3d}/100 {bar}')
        if score < 80:
            issues += 1
    print(f'\n  诊断完成: {issues}个项目有问题')
    return 0  # 诊断本身成功，不报错

if __name__ == '__main__':
    sys.exit(main())
