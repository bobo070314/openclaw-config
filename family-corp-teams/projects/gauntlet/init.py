"""
IGP Gauntlet — 新项目开放擂台

所有 12 部门都可以在这个擂台上提交自己的创新项目。
这是一个自组织的创新孵化器：每天自动扫描、评估、孵化。
"""
import os, json
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
PROJECTS = os.path.join(FAMILY, 'projects')
GAUNTLET = os.path.join(PROJECTS, 'gauntlet')
os.makedirs(GAUNTLET, exist_ok=True)

gauntlet = {
    'name': 'IGP Gauntlet — 创新擂台',
    'created': datetime.now().isoformat(),
    'mantra': '12部门，12项目，0Token，全本地',
    'lanes': {
        'ghost-team': {
            'path': os.path.join(PROJECTS, 'igp-ghost'),
            'status': 'v3生产中',
        },
        'infra': {
            'path': os.path.join(PROJECTS, 'igp-d2a'),
            'status': 'v2生产中',
        },
        'frontend': os.path.join(PROJECTS, 'igp-dashboard'),
        'backend': os.path.join(PROJECTS, 'd2a-server'),
        'ai': os.path.join(PROJECTS, 'igp-knowledge'),
        'mobile': os.path.join(PROJECTS, 'igp-cli'),
        'design': os.path.join(PROJECTS, 'igp-design'),
        'growth': os.path.join(PROJECTS, 'igp-scanner'),
        'data': os.path.join(PROJECTS, 'igp-data'),
        'tech-support': os.path.join(PROJECTS, 'igp-diag'),
        'compliance': os.path.join(PROJECTS, 'igp-gate'),
        'quality': os.path.join(PROJECTS, 'igp-v4-upgrade'),
    }
}

# 记录当前各部门项目进展
status = {}
for dept, path in gauntlet['lanes'].items():
    if isinstance(path, str):
        exists = os.path.isdir(path)
    elif isinstance(path, dict):
        exists = os.path.isdir(path['path'])
    status[dept] = exists

with open(os.path.join(GAUNTLET, 'gauntlet_status.json'), 'w', encoding='utf-8') as f:
    json.dump({
        'gauntlet': gauntlet,
        'current_status': status,
        'active_projects': sum(1 for v in status.values() if v),
        'total_lanes': len(status),
    }, f, ensure_ascii=False, indent=2)

print(f'IGP Gauntlet 擂台就绪')
print(f'  - 12 部门, 12 车道')
print(f'  - {sum(1 for v in status.values() if v)} 个项目已启动')
print(f'  - 文件: gauntlet_status.json')


if __name__ == '__main__':
    print('Gauntlet initialized and ready')
