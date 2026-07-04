"""
IGP Oracle — 自动日报引擎 v1
每次运行自动扫描所有项目状态，生成日报

0 依赖，纯 Python 3.14
"""
import os, json
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
PROJECTS = os.path.join(FAMILY, 'projects')
MEMORY = r'D:\bobo\openclaw-foreign\workspace\memory'
DAILY = os.path.join(MEMORY, 'oracle_daily.json')
os.makedirs(MEMORY, exist_ok=True)


def scan_projects():
    """扫描 projects/ 下所有项目"""
    projects = {}
    for p in sorted(os.listdir(PROJECTS)):
        pp = os.path.join(PROJECTS, p)
        if os.path.isdir(pp):
            files = [f for f in os.listdir(pp) if os.path.isfile(os.path.join(pp, f))]
            py_files = [f for f in files if f.endswith('.py')]
            md_files = [f for f in files if f.endswith('.md')]
            json_files = [f for f in files if f.endswith('.json')]
            total_lines = 0
            for f in py_files:
                try:
                    with open(os.path.join(pp, f), 'r', encoding='utf-8') as fh:
                        total_lines += len(fh.readlines())
                except:
                    pass
            projects[p] = {
                'files': len(files),
                'python': len(py_files),
                'docs': len(md_files),
                'json': len(json_files),
                'lines_of_code': total_lines,
            }
    return projects


def scan_departments():
    """扫描 12 部门"""
    depts = ['frontend', 'backend', 'infra', 'ai', 'mobile', 'design',
             'quality', 'pmo', 'growth', 'data', 'tech-support', 'compliance']
    result = {}
    for d in depts:
        dp = os.path.join(FAMILY, d)
        if os.path.isdir(dp):
            files = [f for f in os.listdir(dp) if os.path.isfile(os.path.join(dp, f))]
            reports = [f for f in files if 'report' in f.lower() or 'evo' in f.lower()]
            result[d] = {
                'alive': True,
                'files': len(files),
                'reports': len(reports),
            }
        else:
            result[d] = {'alive': False, 'files': 0, 'reports': 0}
    return result


def scan_headquarters():
    """扫描 HQ"""
    hq = os.path.join(FAMILY, 'headquarters')
    if not os.path.isdir(hq):
        return {}
    files = [f for f in os.listdir(hq) if os.path.isfile(os.path.join(hq, f))]
    py_files = [f for f in files if f.endswith('.py')]
    json_files = [f for f in files if f.endswith('.json')]
    return {
        'files': len(files),
        'scripts': len(py_files),
        'reports': len(json_files),
    }


def scan_v4():
    """扫描 V4"""
    v4 = os.path.join(FAMILY, 'upgrade-v4')
    if not os.path.isdir(v4):
        return {}
    py_files = [f for f in os.listdir(v4) if f.endswith('.py') and os.path.isfile(os.path.join(v4, f))]
    return {'scripts': len(py_files)}


def render_ascii_report(projects, depts, hq, v4):
    """渲染 ASCII 日报"""
    lines = []
    lines.append('=' * 55)
    lines.append('  📋 IGP Oracle — 自动日报')
    lines.append(f'  时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    lines.append('=' * 55)
    
    # 项目
    lines.append(f'\n📦 项目 ({len(projects)} 个):')
    total_loc = 0
    for name, info in sorted(projects.items()):
        lines.append(f'  {name}: {info["files"]}文件 | {info["lines_of_code"]}行 | {info["docs"]}篇文档')
        total_loc += info['lines_of_code']
    lines.append(f'  总代码行: {total_loc}')
    
    # 部门
    alive = sum(1 for v in depts.values() if v.get('alive'))
    dead = sum(1 for v in depts.values() if not v.get('alive'))
    lines.append(f'\n🏛 部门 ({alive}/{alive + dead} 存活):')
    for name, info in sorted(depts.items()):
        sym = '✅' if info.get('alive') else '❌'
        if info.get('alive'):
            lines.append(f'  {sym} {name}: {info["files"]}文件, {info["reports"]}份报告')
    
    # HQ
    lines.append(f'\n🏢 HQ: {hq.get("files", 0)}文件 | {hq.get("scripts", 0)}脚本 | {hq.get("reports", 0)}报告')
    
    # V4
    lines.append(f'\n🔧 V4: {v4.get("scripts", 0)} 个脚本')
    
    # 总结
    lines.append(f'\n{"=" * 55}')
    lines.append(f'  累计: {len(projects)} 项目, {total_loc} 行代码')
    lines.append(f'  全部本地, 0 Token 消耗')
    lines.append(f'{"=" * 55}')
    
    return '\n'.join(lines)


def main():
    projects = scan_projects()
    depts = scan_departments()
    hq = scan_headquarters()
    v4 = scan_v4()
    
    report_text = render_ascii_report(projects, depts, hq, v4)
    print(report_text)
    
    # 保存 JSON
    json_report = {
        'timestamp': datetime.now().isoformat(),
        'projects': projects,
        'departments': depts,
        'headquarters': hq,
        'v4': v4,
        'summary': {
            'project_count': len(projects),
            'total_loc': sum(v['lines_of_code'] for v in projects.values()),
            'dept_alive': sum(1 for v in depts.values() if v.get('alive')),
            'zero_token': True,
        }
    }
    with open(DAILY, 'w', encoding='utf-8') as f:
        json.dump(json_report, f, ensure_ascii=False, indent=2)
    
    # 同时写入 memory/2026-07-01.md 附加
    log_path = os.path.join(MEMORY, '2026-07-01.md')
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f'\n\n## IGP Oracle 自动日报 (09:43)\n')
        f.write(f'{report_text}\n')


if __name__ == '__main__':
    main()
