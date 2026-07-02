"""IGP SiliconMemory Tools — 三级迁移 + 时间窗口 + 技能融合
裂变产物 (来自 Letta memory tiers + Hindsight 事件溯源)
零依赖, 纯Python stdlib
"""
import time
from collections import defaultdict

__all__ = ['MemConsolidator', 'TimeSeriesSearch', 'SkillFusion']


class MemConsolidator:
    """三级记忆迁移 (来自 Letta: Working -> Archival -> Core)"""
    LEVELS = ('hot', 'warm', 'cold')
    WEIGHTS = {'hot': 3.0, 'warm': 1.0, 'cold': 0.5}
    THRESHOLDS = {'hot_to_warm': (3, 3600), 'warm_to_cold': (1, 86400)}
    
    def __init__(self):
        self.tiers = {lvl: [] for lvl in self.LEVELS}
    
    def add(self, memory_id, level='hot'):
        if level not in self.LEVELS:
            level = 'warm'
        self.tiers[level].append({
            'id': memory_id,
            'level': level,
            'access_count': 0,
            'last_access': time.time(),
            'created': time.time()
        })
    
    def access(self, memory_id):
        """访问记忆，更新热度"""
        for lvl in self.LEVELS:
            for m in self.tiers[lvl]:
                if m['id'] == memory_id:
                    m['access_count'] += 1
                    m['last_access'] = time.time()
                    return m
        return None
    
    def consolidate(self):
        """执行三级迁移"""
        now = time.time()
        for m in list(self.tiers['hot']):
            if m['access_count'] < self.THRESHOLDS['hot_to_warm'][0] and \
               (now - m['last_access']) > self.THRESHOLDS['hot_to_warm'][1]:
                m['level'] = 'warm'
                self.tiers['warm'].append(m)
                self.tiers['hot'].remove(m)
        
        for m in list(self.tiers['warm']):
            if m['access_count'] < self.THRESHOLDS['warm_to_cold'][0] and \
               (now - m['last_access']) > self.THRESHOLDS['warm_to_cold'][1]:
                m['level'] = 'cold'
                self.tiers['cold'].append(m)
                self.tiers['warm'].remove(m)
    
    def get_weighted(self):
        """获取带权重的所有记忆"""
        results = []
        for lvl in self.LEVELS:
            w = self.WEIGHTS[lvl]
            for m in self.tiers[lvl]:
                results.append((w, m))
        return sorted(results, key=lambda x: -x[0])
    
    def promote(self, memory_id):
        """手动提升到hot"""
        for lvl in ('cold', 'warm'):
            for m in list(self.tiers[lvl]):
                if m['id'] == memory_id:
                    m['level'] = 'hot'
                    m['access_count'] = self.THRESHOLDS['hot_to_warm'][0]
                    self.tiers['hot'].append(m)
                    self.tiers[lvl].remove(m)
                    return True
        return False


class TimeSeriesSearch:
    """时间序列搜索 (来自 Hindsight 事件溯源)"""
    def __init__(self, events=None):
        self.events = events or []
    
    def add_event(self, event):
        self.events.append(event)
    
    def filter_window(self, start_epoch, end_epoch):
        """时间窗口过滤"""
        return [e for e in self.events 
                if start_epoch <= e.get('_time', 0) <= end_epoch]
    
    def hot_events(self, window_secs=3600, min_count=3):
        """检测近期热点"""
        now = time.time()
        recent = self.filter_window(now - window_secs, now)
        # 按type聚合
        type_counts = Counter(e.get('type', 'unknown') for e in recent)
        return {t: c for t, c in type_counts.items() if c >= min_count}
    
    def timeline(self, event_type=None, limit=20):
        """获取时间线 (按时间降序)"""
        filtered = self.events
        if event_type:
            filtered = [e for e in filtered if e.get('type') == event_type]
        return sorted(filtered, key=lambda e: e.get('_time', 0), reverse=True)[:limit]


from collections import Counter

class SkillFusion:
    """技能融合 (同名技能自动合并)"""
    def __init__(self):
        self.skills = {}
    
    def add(self, name, instruction, tags=None):
        if name not in self.skills:
            self.skills[name] = {
                'name': name,
                'instructions': [],
                'tags': set(),
                'version': 0,
                'created': time.time()
            }
        self.skills[name]['instructions'].append(instruction)
        if tags:
            self.skills[name]['tags'].update(tags)
        self.skills[name]['version'] += 1
    
    def fuse(self, name):
        """融合同名技能的所有instruction"""
        if name not in self.skills:
            return None
        sk = self.skills[name]
        # 去重+排序
        unique = list(dict.fromkeys(sk['instructions']))
        # 取出主要和最相关的两个版本
        if len(unique) <= 2:
            fused = '; '.join(unique)
        else:
            fused = unique[0] + ' [variants: ' + '|'.join(unique[1:4]) + ']'
        return {
            'name': name,
            'fused_instruction': fused,
            'versions': sk['version'],
            'tags': list(sk['tags'])
        }
    
    def find_related(self, name, all_skills):
        """找相关技能 (基于名称相似度)"""
        if name not in self.skills:
            return []
        tags = self.skills[name]['tags']
        related = []
        for n, sk in all_skills.items():
            if n != name and (tags & sk['tags']):
                related.append((n, len(tags & sk['tags'])))
        return sorted(related, key=lambda x: -x[1])
