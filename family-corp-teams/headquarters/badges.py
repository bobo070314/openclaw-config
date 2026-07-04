"""
IGP 勋章系统 — 部门激励 v1
每个部门完成任务自动获得勋章
勋章可以累积、升级、展示
"""
import os, json
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
BADGE_FILE = os.path.join(FAMILY, 'headquarters', 'badges.json')

# 勋章定义
BADGES = {
    'first_project': {
        'name': '🔥 开山鼻祖',
        'desc': '完成第一个自主研发项目',
        'icon': '🔥',
    },
    'pipeline_pioneer': {
        'name': '⚡ 流水线先锋',
        'desc': '跑通监控→通信→自愈→汇报全链路',
        'icon': '⚡',
    },
    'self_replicator': {
        'name': '🧬 基因复制者',
        'desc': '参与Agent自我复制',
        'icon': '🧬',
    },
    'bug_hunter': {
        'name': '🐛 猎虫者',
        'desc': '发现并修复一个真实bug',
        'icon': '🐛',
    },
    'zero_token': {
        'name': '💎 零耗大师',
        'desc': '0 token完成项目',
        'icon': '💎',
    },
    'fast_shipper': {
        'name': '🚀 极速发货',
        'desc': '30分钟内交付项目',
        'icon': '🚀',
    },
    'quality_guardian': {
        'name': '🛡 质量卫士',
        'desc': '代码评分8分以上',
        'icon': '🛡',
    },
    'agent_builder': {
        'name': '🤖 Agent建筑师',
        'desc': '创建或升级Agent模块',
        'icon': '🤖',
    },
}

# 当前获奖部门
AWARDS = {
    'infra-team2': {
        'department': 'infra',
        'badges': ['first_project', 'zero_token', 'agent_builder'],
        'note': 'D2A Agent协议研发并集成到V4',
    },
    'ghost-team': {
        'department': 'frontend',
        'badges': ['first_project', 'zero_token', 'bug_hunter', 'fast_shipper'],
        'note': 'Ghost v1→v2 检测+自愈+报警',
    },
    'hq-swat': {
        'department': 'headquarters',
        'badges': ['pipeline_pioneer', 'self_replicator'],
        'note': 'Nexus融合系统 + Genesis自我复制',
    },
}

def load_or_init():
    if os.path.exists(BADGE_FILE):
        with open(BADGE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'version': 'v1',
        'badge_definitions': BADGES,
        'awards': {},
        'leaderboard': {}
    }

def award_badge(dept_name, badge_key, note=''):
    data = load_or_init()
    if dept_name not in data['awards']:
        data['awards'][dept_name] = {
            'department': dept_name,
            'badges': [],
            'note': note,
            'total': 0,
        }
    
    dept = data['awards'][dept_name]
    if badge_key not in dept['badges']:
        dept['badges'].append(badge_key)
        dept['total'] = len(dept['badges'])
        dept['note'] = note or dept['note']
    
    # 更新排行榜
    depts_ranked = sorted(
        data['awards'].values(),
        key=lambda x: x['total'],
        reverse=True
    )
    data['leaderboard'] = {
        'updated': datetime.now().isoformat(),
        'rankings': [
            {
                'rank': i + 1,
                'department': d['department'],
                'badges': d['total'],
                'badge_list': [BADGES.get(b, {}).get('name', b) for b in d['badges']],
                'note': d['note'],
            }
            for i, d in enumerate(depts_ranked)
        ]
    }
    
    with open(BADGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return data

def render_leaderboard():
    data = load_or_init()
    print(f'{"="*55}')
    print(f'  🏆 IGP 集团部门勋章排行榜')
    print(f'{"="*55}')
    print()
    for entry in data.get('leaderboard', {}).get('rankings', []):
        badges_str = ' '.join(entry['badge_list'])
        print(f'  #{entry["rank"]}  {entry["department"]}')
        print(f'     勋章: {entry["badges"]}枚 | {badges_str}')
        print(f'     业绩: {entry["note"]}')
        print()
    print(f'{"="*55}')

# 批量授予
def batch_award():
    for dept_name, info in AWARDS.items():
        for badge in info['badges']:
            award_badge(dept_name, badge, info['note'])
    render_leaderboard()

if __name__ == '__main__':
    batch_award()
