"""
吸收可视化看板 — 看IGP全部门吸收状态
"""
import os, json
from datetime import datetime

FAMILY = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams"
PROJECTS = os.path.join(FAMILY, 'projects')
ABSORB_DIR = os.path.join(FAMILY, 'headquarters', 'absorb')

def scan():
    data = {'projects': {}, 'absorb': {}, 'timestamp': datetime.now().isoformat()[:19]}
    for p in sorted(os.listdir(PROJECTS)):
        pp = os.path.join(PROJECTS, p)
        if not os.path.isdir(pp):
            continue
        inj = [f for f in os.listdir(pp) if f.endswith('.md') and ('DNA' in f or 'LLM' in f or 'D2A' in f or '金融' in f or 'GLM' in f or '异形' in f or '规则' in f or '数字' in f or '诊断' in f)]
        has_readme = any(f.lower().startswith('readme') for f in os.listdir(pp))
        py_count = len([f for f in os.listdir(pp) if f.endswith('.py')])
        data['projects'][p] = {
            'py_files': py_count,
            'has_readme': has_readme,
            'injections': len(inj),
        }
    data['absorb'] = {'codebase-memory-mcp': '吸收于 11:17'}
    return data

def render_table(data):
    print('IGP 吸收可视化')
    print('=' * 50)
    print(f'{'项目':20s} {'py':4s} {'README':8s} {'注射':5s}')
    print('-' * 50)
    for p, info in sorted(data['projects'].items()):
        rm = '✅' if info['has_readme'] else '❌'
        inj = str(info['injections'])
        bar = '█' * info['py_files']
        print(f'{p:20s} {info["py_files"]:4d} {rm:8s} {inj:5s} | {bar}')
    print('-' * 50)
    print(f'吸收: {len(data["absorb"])}家')

def main():
    data = scan()
    render_table(data)
    json.dump(data, open(os.path.join(os.path.dirname(__file__), 'absorb_state.json'), 'w'))

if __name__ == '__main__':
    main()
