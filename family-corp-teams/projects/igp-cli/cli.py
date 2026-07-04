"""
IGP CLI工具集 — Python 0依赖命令行工具
"""
import os, sys, json, argparse
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'

def cmd_status():
    """igp status — 查看项目状态"""
    projects = sorted(os.listdir(os.path.join(FAMILY, 'projects')))
    for p in projects:
        pp = os.path.join(FAMILY, 'projects', p)
        if not os.path.isdir(pp):
            continue
        py_files = [f for f in os.listdir(pp) if f.endswith('.py')]
        total = sum(len(open(os.path.join(pp, f), encoding='utf-8').read().split('\n')) for f in py_files)
        print(f'  {p:18s} | {len(py_files)}文件 | {total}行')

def cmd_heal():
    """igp heal — 自愈检查"""
    for p in sorted(os.listdir(os.path.join(FAMILY, 'projects'))):
        pp = os.path.join(FAMILY, 'projects', p)
        if not os.path.isdir(pp):
            continue
        has_readme = any(f.lower().startswith('readme') for f in os.listdir(pp))
        print(f'  {p:18s} | {"✅ README" if has_readme else "❌ 缺README"}')

def cmd_rank():
    """igp rank — 项目排名"""
    scores = {'igp-docmind': 168, 'igp-ghost': 105, 'igp-d2a': 42, 'igp-federation': 4,
              'igp-evolver': 30, 'igp-genesis': 30, 'igp-mutation': 24, 'gauntlet': 12}
    for name, score in sorted(scores.items(), key=lambda x: -x[1]):
        bar = '█' * (score // 10)
        print(f'  {name:18s} | {score:3d} {bar}')

def main():
    parser = argparse.ArgumentParser(description='IGP CLI 工具集')
    parser.add_argument('cmd', nargs='?', default='status', help='status/heal/rank')
    args = parser.parse_args()
    
    cmds = {
        'status': cmd_status,
        'heal': cmd_heal,
        'rank': cmd_rank,
    }
    
    if args.cmd in cmds:
        print(f'IGP CLI — {args.cmd}\n')
        cmds[args.cmd]()
    else:
        print(f'未知命令: {args.cmd}')
        print(f'可用: {", ".join(cmds.keys())}')


if __name__ == '__main__':
    main()
