"""
IGP Arena — 擂台评分系统 v1
每个部门的突破项目自动评分
评分最高者立刻升任部门领导
"""
import os, json
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
PROJECTS = os.path.join(FAMILY, 'projects')
HQ = os.path.join(FAMILY, 'headquarters')
LEADERSHIP_FILE = os.path.join(HQ, 'leadership.json')
ARENA_FILE = os.path.join(HQ, 'arena_scores.json')

# 评分维度
def score_project_innovation(project_dir, project_name):
    """创新性评分 1-5"""
    score = 1
    
    # 检查README/BEST_PRACTICE
    readme = os.path.join(project_dir, 'README.md')
    bp = os.path.join(project_dir, 'BEST_PRACTICE.md')
    if os.path.exists(readme) or os.path.exists(bp):
        score += 1
    
    # 检查是否有多文件
    files = [f for f in os.listdir(project_dir) if os.path.isfile(os.path.join(project_dir, f))]
    py_files = [f for f in files if f.endswith('.py')]
    
    if len(py_files) >= 2:
        score += 1
    if len(py_files) >= 3:
        score += 1
    
    # 检查是否有测试/验证文件
    has_test = any('test' in f.lower() or 'verify' in f.lower() for f in py_files)
    if has_test:
        score += 1
    
    # 特定项目加分
    innovation_bonus = {
        'genesis': 2,  # 自我复制 — 最高创新
        'evolver': 2,  # 自我进化
        'mutation': 2, # 基因突变
        'nexus': 1,    # 融合系统
        'd2a': 1,      # Agent通信
        'ghost': 1,    # 幽灵哨兵
    }
    for key, bonus in innovation_bonus.items():
        if key in project_name.lower():
            score = min(5, score + bonus)
    
    return min(5, max(1, score))


def score_project_completion(project_dir):
    """完成度评分 1-5"""
    score = 1
    files = [f for f in os.listdir(project_dir) if os.path.isfile(os.path.join(project_dir, f))]
    py_files = [f for f in files if f.endswith('.py')]
    
    # 文件数量
    if len(py_files) >= 1:
        score += 1
    if len(py_files) >= 3:
        score += 1
    
    # 有文档
    has_doc = any(f.endswith('.md') for f in files)
    if has_doc:
        score += 1
    
    # 有配置文件
    has_json = any(f == 'FEEDBACK.json' or f.endswith('_feedback.json') for f in files)
    if has_json:
        score += 1
    
    return min(5, max(1, score))


def evaluate_all_projects():
    """评估所有项目"""
    results = {}
    
    for p in sorted(os.listdir(PROJECTS)):
        pp = os.path.join(PROJECTS, p)
        if not os.path.isdir(pp):
            continue
        
        innovation = score_project_innovation(pp, p)
        completion = score_project_completion(pp)
        total = innovation * completion
        
        results[p] = {
            'innovation': innovation,
            'completion': completion,
            'total_score': total,
            'files': len([f for f in os.listdir(pp) if os.path.isfile(os.path.join(pp, f))]),
        }
    
    return results


def assign_leadership(project_scores):
    """根据项目评分分配领导职位"""
    # 项目→部门映射
    project_to_dept = {
        'igp-ghost': 'frontend',
        'd2a-server': 'backend',
        'igp-d2a': 'infra',
        'igp-knowledge': 'ai',
        'igp-cli': 'mobile',
        'igp-design': 'design',
        'igp-evolver': 'quality',
        'igp-genesis': 'headquarters',
        'igp-mutation': 'headquarters',
        'igp-scanner': 'growth',
        'igp-data': 'data',
        'igp-diag': 'tech-support',
        'igp-gate': 'compliance',
        'igp-dashboard': 'frontend',
        'igp-federation': 'infra',
        'igp-publish': 'growth',
        'igp-patrol': 'infra',
        'gauntlet': 'headquarters',
    }
    
    # 按部门分组
    dept_projects = {}
    for proj, score in project_scores.items():
        dept = project_to_dept.get(proj, 'unknown')
        if dept not in dept_projects:
            dept_projects[dept] = []
        dept_projects[dept].append((proj, score['total_score']))
    
    # 每个部门选最佳项目
    promotions = {}
    for dept, projs in dept_projects.items():
        if not projs:
            continue
        best = max(projs, key=lambda x: x[1])
        promotions[dept] = {
            'project': best[0],
            'score': best[1],
            'reason': f'以项目 {best[0]} (评分 {best[1]}) 升任 {dept} 总监',
        }
    
    return promotions


def main():
    print('🏟 IGP Arena — 擂台评分系统')
    print('=' * 55)
    
    # 评估所有项目
    scores = evaluate_all_projects()
    
    print(f'\n📊 项目评分排行:')
    ranked = sorted(scores.items(), key=lambda x: x[1]['total_score'], reverse=True)
    
    for rank, (proj, score) in enumerate(ranked, 1):
        sym = '🏆' if rank == 1 else '🥇' if rank <= 3 else '  '
        bar = '█' * score['total_score'] + '░' * (25 - score['total_score'])
        print(f'  {sym} #{rank} {proj}')
        print(f'     创新 {score["innovation"]} × 完成 {score["completion"]} = {score["total_score"]}分')
    
    # 分配领导
    print(f'\n📋 领导任命:')
    promotions = assign_leadership(scores)
    
    for dept, info in sorted(promotions.items()):
        print(f'  ✅ {dept} → {info["project"]} ({info["score"]}分)')
        print(f'     理由: {info["reason"]}')
    
    # 保存结果
    arena_data = {
        'timestamp': datetime.now().isoformat(),
        'scores': scores,
        'ranking': [
            {'rank': i+1, 'project': p, 'score': s['total_score'],
             'innovation': s['innovation'], 'completion': s['completion']}
            for i, (p, s) in enumerate(ranked)
        ],
        'promotions': promotions,
    }
    
    with open(ARENA_FILE, 'w', encoding='utf-8') as f:
        json.dump(arena_data, f, ensure_ascii=False, indent=2)
    
    # 更新 leadership.json
    with open(LEADERSHIP_FILE, 'r', encoding='utf-8') as f:
        leadership = json.load(f)
    
    for dept, info in promotions.items():
        if dept in leadership['current_leaders']:
            leadership['promotions'][dept] = info['project']
            leadership['current_leaders'][dept] = f'{info["project"]}团队 ({info["score"]}分)'
    
    with open(LEADERSHIP_FILE, 'w', encoding='utf-8') as f:
        json.dump(leadership, f, ensure_ascii=False, indent=2)
    
    # 冠军宣布
    champion = ranked[0]
    print(f'\n🏆 冠军项目: {champion[0]} — {champion[1]["total_score"]}分')
    print(f'   (创新 {champion[1]["innovation"]} × 完成 {champion[1]["completion"]})')
    print(f'\n💼 部门领导已更新 -> headquarters/leadership.json')
    print(f'📊 擂台评分已保存 -> headquarters/arena_scores.json')


if __name__ == '__main__':
    main()
