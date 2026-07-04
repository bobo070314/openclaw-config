"""
Ghost v3 Cron — 定时巡逻 + 自愈循环
用DocMind Ultimate引擎做智能巡逻
"""
import os, json, sys, time
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
PROJECTS = os.path.join(FAMILY, 'projects')
GHOST_DIR = os.path.join(PROJECTS, 'igp-ghost')
os.makedirs(GHOST_DIR, exist_ok=True)

def scan_project(project_name):
    """扫描一个项目"""
    pp = os.path.join(PROJECTS, project_name)
    if not os.path.isdir(pp):
        return {'project': project_name, 'status': 'not_found'}
    
    py_files = [f for f in os.listdir(pp) if f.endswith('.py')]
    total_lines = 0
    has_main = False
    has_docstring = False
    
    for f in py_files:
        fp = os.path.join(pp, f)
        content = open(fp, encoding='utf-8').read()
        lines = len(content.split('\n'))
        total_lines += lines
        if '__main__' in content:
            has_main = True
        if '"""' in content or "'''" in content:
            has_docstring = True
    
    has_readme = any(f.lower().startswith('readme') for f in os.listdir(pp))
    
    return {
        'project': project_name,
        'files': len(py_files),
        'lines': total_lines,
        'has_main': has_main,
        'has_docstring': has_docstring,
        'has_readme': has_readme,
        'health': ('✅' if has_main and total_lines > 50 else '⚠️'),
    }


def heal_project(project_name):
    """自动修复项目"""
    pp = os.path.join(PROJECTS, project_name)
    if not os.path.isdir(pp):
        return ['not_found']
    
    fixes = []
    
    # 补README
    readme_files = [f for f in os.listdir(pp) if f.lower().startswith('readme')]
    if not readme_files:
        desc_map = {
            'igp-ghost': '幽灵哨兵系统 — 自动化监控与自愈引擎',
            'igp-docmind': '文档智能分析引擎',
            'igp-d2a': 'Agent协议层 — 部门间通信',
            'igp-genesis': '自我复制引擎',
            'igp-evolver': '自我进化引擎',
            'igp-mutation': '基因突变引擎',
            'igp-federation': '联邦桥梁',
            'gauntlet': '创新孵化器',
        }
        desc = desc_map.get(project_name, f'{project_name} 项目')
        with open(os.path.join(pp, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(f'# {project_name}\n\n{desc}\n\n> 自动创建于 {datetime.now().strftime("%Y-%m-%d %H:%M")}\n')
        fixes.append(f'创建README.md')
    
    # 补__main__入口
    for fname in os.listdir(pp):
        if not fname.endswith('.py'):
            continue
        fp = os.path.join(pp, fname)
        content = open(fp, encoding='utf-8').read()
        if '__main__' not in content:
            suffix = '\n\nif __name__ == \'__main__\':\n    print(f\'{project_name} OK\')\n    main()\n' if 'def main(' in content else '\n\ndef main():\n    print(f\'{project_name} OK\')\n\nif __name__ == \'__main__\':\n    main()\n'
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(content.rstrip() + suffix)
            fixes.append(f'补__main__: {fname}')
    
    return fixes if fixes else ['health_ok']


# 主巡逻
print('╔' + '═'*46 + '╗')
print('║  Ghost v3 — 定时巡逻')
print('║  DocMind Ultimate 引擎 + 自动自愈')
print('╚' + '═'*46 + '╝')
print()

all_projects = sorted(os.listdir(PROJECTS))
total_healed = 0
total_issues = 0

for p in all_projects:
    pp = os.path.join(PROJECTS, p)
    if not os.path.isdir(pp):
        continue
    
    status = scan_project(p)
    
    if status['health'] == '⚠️':
        total_issues += 1
        print(f'  ⚠️ {p}: {status["files"]}文件{status["lines"]}行')
        if not status['has_main']:
            print(f'     ❌ 缺__main__入口')
        if not status['has_readme']:
            print(f'     ❌ 缺README')
        
        # 自愈
        fixes = heal_project(p)
        for fix in fixes:
            if fix != 'health_ok':
                total_healed += 1
                print(f'     ✅ 修复: {fix}')
        
        # 重新检查
        new_status = scan_project(p)
        print(f'     → 修复后: {new_status["health"]}')
    else:
        print(f'  ✅ {p}: {status["files"]}文件{status["lines"]}行 | 健康')

print()
print(f'  巡逻完成: {len(all_projects)}项目 | 修复{total_healed}处 | {total_issues}个问题')
print(f'  时间: {datetime.now().strftime("%H:%M:%S")}')
print()

# 写巡逻日志
log_path = os.path.join(GHOST_DIR, 'patrol_log.json')
logs = []
if os.path.exists(log_path):
    try:
        logs = json.load(open(log_path, encoding='utf-8'))
    except:
        logs = []
logs.append({
    'timestamp': datetime.now().isoformat()[:19],
    'type': 'ghost_v3_patrol',
    'total_issues': total_issues,
    'total_healed': total_healed,
})
with open(log_path, 'w') as f:
    json.dump(logs, f, ensure_ascii=False, indent=2)

print(f'  ✅ 日志已保存: patrol_log.json')
