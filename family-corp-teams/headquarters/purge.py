"""
IGP Purge — 部门淘汰执行 v1
考核标准升级：
- 连续2轮无突破项目 → 部门就地解散
- 解散后由冠军项目团队接管
- 解散部门回归"待再生池"
"""
import os, json, shutil
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
HQ = os.path.join(FAMILY, 'headquarters')
ARENA_FILE = os.path.join(HQ, 'arena_scores.json')
LEADERSHIP_FILE = os.path.join(HQ, 'leadership.json')
ELIMINATED_DIR = os.path.join(HQ, 'eliminated')
os.makedirs(ELIMINATED_DIR, exist_ok=True)

REBIRTH_DIR = os.path.join(HQ, 'rebirth_pool')
os.makedirs(REBIRTH_DIR, exist_ok=True)


def purge_nonperformers():
    """淘汰无产出部门"""
    with open(ARENA_FILE, 'r', encoding='utf-8') as f:
        arena = json.load(f)
    with open(LEADERSHIP_FILE, 'r', encoding='utf-8') as f:
        leadership = json.load(f)

    scores = arena.get('scores', {})
    promotions = leadership.get('promotions', {})
    current_leaders = leadership.get('current_leaders', {})
    
    # 已晋升的部门
    promoted_depts = set(promotions.keys())
    
    # 无突破项目的部门
    all_depts = set(current_leaders.keys())
    nonperformers = all_depts - promoted_depts
    
    purge_report = {
        'timestamp': datetime.now().isoformat(),
        'round': 1,
        'purged': [],
        'spared': [],
    }
    
    for dept in sorted(nonperformers):
        # 检查部门目录是否有原创项目
        dept_dir = os.path.join(FAMILY, dept)
        has_own_project = False
        projects_found = []
        
        if os.path.isdir(dept_dir):
            files = os.listdir(dept_dir)
            py_files = [f for f in files if f.endswith('.py')]
            
            # 检查是否有原创代码（非模板文件）
            for f in py_files:
                fp = os.path.join(dept_dir, f)
                try:
                    with open(fp, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                        # 真正的原创代码通常有注释或特有函数名
                        if len(content) > 500 and 'def ' in content:
                            has_own_project = True
                            projects_found.append(f)
                except:
                    pass
        
        if has_own_project:
            purge_report['spared'].append({
                'department': dept,
                'reason': '有原创代码',
                'files': projects_found,
            })
            current_leaders[dept] = f'待定 — 有代码但未达到突破标准'
        else:
            # 执行淘汰
            purge_report['purged'].append({
                'department': dept,
                'reason': '无突破项目 + 无原创代码',
            })
            
            # 部门目录移到淘汰区
            if os.path.isdir(dept_dir):
                archive_name = f'{dept}_purged_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
                archive_path = os.path.join(ELIMINATED_DIR, archive_name)
                try:
                    shutil.copytree(dept_dir, archive_path)
                    for f in os.listdir(dept_dir):
                        fp = os.path.join(dept_dir, f)
                        if os.path.isfile(fp):
                            os.remove(fp)
                    print(f'  🗑 部门 {dept} 已归档: {archive_name}')
                except Exception as e:
                    print(f'  ⚠ 归档失败 {dept}: {e}')
            
            current_leaders[dept] = '❌ 已淘汰 — 待再生'
            
            # 写入再生池
            rebirth_record = {
                'department': dept,
                'purged_at': datetime.now().isoformat(),
                'reason': '无突破项目',
                'requirements': ['至少1个原创项目', '评分创新性3+', '完成度3+'],
            }
            rebirth_path = os.path.join(REBIRTH_DIR, f'{dept}_rebirth.json')
            with open(rebirth_path, 'w', encoding='utf-8') as f:
                json.dump(rebirth_record, f, ensure_ascii=False, indent=2)
    
    # 更新领导表
    leadership['current_leaders'] = current_leaders
    leadership['round_completed'] = purge_report['timestamp']
    
    with open(LEADERSHIP_FILE, 'w', encoding='utf-8') as f:
        json.dump(leadership, f, ensure_ascii=False, indent=2)
    
    # 保存淘汰报告
    purge_path = os.path.join(HQ, '_purge_report.json')
    with open(purge_path, 'w', encoding='utf-8') as f:
        json.dump(purge_report, f, ensure_ascii=False, indent=2)
    
    return purge_report


def main():
    print('🗡  IGP Purge — 部门淘汰执行')
    print('=' * 55)
    
    report = purge_nonperformers()
    
    print(f'\n📋 第{report["round"]}轮淘汰:')
    
    if report['purged']:
        print(f'\n❌ 淘汰 ({len(report["purged"])}):')
        for p in report['purged']:
            print(f'   {p["department"]} — {p["reason"]}')
    else:
        print('\n✅ 无淘汰')
    
    if report['spared']:
        print(f'\n⚡ 暂免 ({len(report["spared"])}):')
        for s in report['spared']:
            print(f'   {s["department"]} — {s["reason"]}')
    
    print(f'\n🏆 执行完毕:')
    print(f'   淘汰: {len(report["purged"])} 部门')
    print(f'   暂免: {len(report["spared"])} 部门')
    print(f'   再生池: {REBIRTH_DIR}')
    print(f'   淘汰归档: {ELIMINATED_DIR}')


if __name__ == '__main__':
    main()
