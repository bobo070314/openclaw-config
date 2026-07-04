"""
IGP DocMind — 突变分支体系
不是一条筋走到底，是同一棵树的枝条往不同方向长
每支独立计算/独立变异/独立评分

枝条体系:
  主干: DocMind v4 企业级文档引擎
  ├─ 枝A: 金融风控专用 (数字精读/异常检测/合规扫描)
  ├─ 枝B: 代码逆向分支 (源码分析/反编译/依赖树)
  ├─ 枝C: 语义压缩分支 (极致压缩比/向量化)
  └─ 枝D: 知识图谱分支 (实体提取/关系推理)
"""
import os, sys, json, re, hashlib, math, random
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
DOCMIND_DIR = os.path.join(FAMILY, 'projects', 'igp-docmind')
os.makedirs(DOCMIND_DIR, exist_ok=True)


class BranchMutator:
    """
    枝条突变器 — 给每个分支分配独立策略
    不同分支对同一份文档会给出不同结论
    就像树的不同枝条对阳光雨露反应不一样
    """
    
    def __init__(self, branch_id, mutation_vector):
        self.branch_id = branch_id
        self.mutation_vector = mutation_vector  # 突变向量: 一组权重
        self.age = 0
        self.score = 5.0
        self.offspring = []
    
    def process(self, text):
        """用本分支的突变向量处理文档"""
        self.age += 1
        
        # 突变向量决定怎么解析
        weights = self.mutation_vector
        paragraphs = re.split(r'\n\s*\n', text)
        
        # 按权重不同的方式解析
        if weights.get('depth_first', 0) > 0.6:
            # 深度优先：深挖每一个结构
            structures = self._deep_parse(paragraphs)
        elif weights.get('width_first', 0) > 0.6:
            # 广度优先：快速扫全貌
            structures = self._wide_parse(paragraphs)
        elif weights.get('key_value', 0) > 0.6:
            # KV抽取向：专门提取键值对
            structures = self._kv_parse(paragraphs)
        elif weights.get('code_assert', 0) > 0.6:
            # 代码检测向：找代码/模式
            structures = self._code_parse(paragraphs)
        else:
            # 混合型
            structures = self._mixed_parse(paragraphs, weights)
        
        return structures
    
    def _deep_parse(self, paragraphs):
        """深度解析：标题层级树"""
        tree = {'root': [], 'depth': 0, 'headers': 0, 'tables': 0}
        current_path = [tree['root']]
        
        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
            h = re.match(r'^(#+)\s+(.+)', p)
            if h:
                level = len(h.group(1))
                entry = {'level': level, 'text': h.group(2), 'children': []}
                
                while len(current_path) > level:
                    current_path.pop()
                while len(current_path) <= level:
                    current_path.append(current_path[-1])
                
                current_path[level-1].append(entry)
                current_path[level] = entry['children']
                tree['headers'] += 1
            elif re.search(r'\|.*\|.*\|', p):
                tree['tables'] += 1
                current_path[-1].append({'type': 'table', 'text': p[:80]})
        
        tree['depth'] = max(1, tree['headers'])
        return tree
    
    def _wide_parse(self, paragraphs):
        """广度解析：统计特征"""
        return {
            'stats': {
                'total': len(paragraphs), 
                'headers': sum(1 for p in paragraphs if re.match(r'^#+\s', p)),
                'tables': sum(1 for p in paragraphs if re.search(r'\|.*\|.*\|', p)),
                'lists': sum(1 for p in paragraphs if re.match(r'^\s*[*-]\s', p)),
                'codes': sum(1 for p in paragraphs if re.search(r'```', p)),
            },
            'avg_len': sum(len(p) for p in paragraphs) / max(len(paragraphs), 1),
        }
    
    def _kv_parse(self, paragraphs):
        """KV抽取"""
        kvs = {}
        for p in paragraphs:
            m = re.findall(r'(\w[\w\s]+?):\s*([^,\n]+)', p)
            for k, v in m:
                kvs[k.strip()] = v.strip()
        return {'key_values': kvs, 'count': len(kvs)}
    
    def _code_parse(self, paragraphs):
        """代码检测"""
        codes = []
        for p in paragraphs:
            if re.search(r'```', p):
                lang = re.search(r'```(\w+)', p)
                codes.append({'lang': lang.group(1) if lang else 'unknown', 'len': len(p)})
            elif re.search(r'(def |class |import |function )', p):
                codes.append({'type': 'inline_code', 'sample': p[:60]})
        return {'code_blocks': codes, 'count': len(codes)}
    
    def _mixed_parse(self, paragraphs, weights):
        """混合解析"""
        result = {}
        for key in weights:
            if key == 'depth_first' and weights[key] > 0.3:
                result['deep'] = self._deep_parse(paragraphs)
            if key == 'width_first' and weights[key] > 0.3:
                result['wide'] = self._wide_parse(paragraphs)
        return result
    
    def mutate(self, force=False):
        """分枝自我突变（每3代一次或强制）"""
        if self.age % 3 != 0 and not force:
            return None
        
        # 随机轻微调整突变向量
        old_vector = dict(self.mutation_vector)
        for key in self.mutation_vector:
            self.mutation_vector[key] = max(0, min(1, self.mutation_vector[key] + random.uniform(-0.15, 0.15)))
        # 归一化保持总权重
        total = sum(self.mutation_vector.values())
        if total > 0:
            for key in self.mutation_vector:
                self.mutation_vector[key] /= total
        
        return {'branch': self.branch_id, 'old': old_vector, 'new': dict(self.mutation_vector)}
    
    def spawn(self, new_branch_id):
        """分裂出一个子分枝"""
        # 基于当前向量生成新的突变向量
        new_vector = dict(self.mutation_vector)
        # 随机挑一个维度极端化
        key_to_amplify = random.choice(list(new_vector.keys()))
        new_vector[key_to_amplify] = min(1, new_vector[key_to_amplify] + 0.3)
        # 归一化
        total = sum(new_vector.values())
        if total > 0:
            for k in new_vector:
                new_vector[k] /= total
        
        child = BranchMutator(new_branch_id, new_vector)
        self.offspring.append(new_branch_id)
        return child
    
    def report(self):
        return {
            'branch': self.branch_id,
            'age': self.age,
            'score': round(self.score, 1),
            'vector': self.mutation_vector,
            'offspring': self.offspring,
        }


class DocMindTree:
    """
    分支树 — 一棵树往不同方向长
    每个分支用不同策略处理文档，结果不一样
    """
    
    def __init__(self):
        # 主干4个初始分支，各自不同的突变向量
        self.branches = {}
        self._seed()
    
    def _seed(self):
        seeds = [
            ('branch-A-finance', {'depth_first': 0.7, 'width_first': 0.1, 'key_value': 0.15, 'code_assert': 0.05},
             '金融风控分支: 深挖结构 + KV提取'),
            ('branch-B-code', {'code_assert': 0.7, 'depth_first': 0.2, 'width_first': 0.05, 'key_value': 0.05},
             '代码分析分支: 找代码块 + 依赖模式'),
            ('branch-C-compress', {'width_first': 0.6, 'key_value': 0.3, 'depth_first': 0.05, 'code_assert': 0.05},
             '语义压缩分支: 扫全貌 + 抽K-V'),
            ('branch-D-graph', {'key_value': 0.5, 'depth_first': 0.3, 'width_first': 0.15, 'code_assert': 0.05},
             '知识图谱分支: KV抽取 + 层级结构'),
        ]
        for bid, vec, desc in seeds:
            self.branches[bid] = BranchMutator(bid, vec)
    
    def process_all(self, text, source='demo'):
        """所有分支同时分析同一份文档"""
        results = {}
        for bid, branch in self.branches.items():
            results[bid] = branch.process(text)
        return results
    
    def mutate_all(self):
        """所有分支同步突变"""
        mutations = {}
        for bid, branch in self.branches.items():
            m = branch.mutate()
            if m:
                mutations[bid] = m
        return mutations
    
    def score_all(self, text_length):
        """基于文档长度给分支评分（长文档更适合deep分支）"""
        for bid, branch in self.branches.items():
            vector = branch.mutation_vector
            score = 5.0
            
            if text_length > 500 and vector.get('depth_first', 0) > 0.4:
                score += 3  # 长文档深度策略加分
            elif text_length < 100 and vector.get('width_first', 0) > 0.4:
                score += 3  # 短文档广度策略加分
            if vector.get('key_value', 0) > 0.4 and re.search(r':\s', 'a: b'):  # 有KV模式
                score += 2
            
            branch.score = score
    
    def report_tree(self):
        """输出整棵树状态"""
        lines = ['IGP DocMind — 分支树状态', '']
        for bid, branch in self.branches.items():
            r = branch.report()
            vec_str = ' | '.join(f'{k}={v:.2f}' for k, v in r['vector'].items())
            lines.append(f'  🌿 {r["branch"]:25s} 年龄:{r["age"]} 分:{r["score"]} 子:{len(r["offspring"])}')
            lines.append(f'     向量: {vec_str}')
            if r['offspring']:
                lines.append(f'     子枝: {", ".join(r["offspring"])}')
            lines.append('')
        return '\n'.join(lines)


def demo_tree():
    """演示分支树"""
    tree = DocMindTree()
    
    test_docs = {
        '金融季报': '''# 2026-Q2 金融季报
营收: ¥15.2M | 净利: ¥3.1M | 增长: +34.8%

## 风险指标
不良率: 0.87% | 拨备率: 182% | 资本充足: 14.2%

## 持仓结构
- 固收: 42% | - 权益: 33% | - 现金: 18% | - 其他: 7%''',
        
        '代码审查': '''# Code Review Report

def calculate_risk(portfolio):
    """风险评估函数"""
    total_risk = 0
    for asset in portfolio:
        total_risk += asset.risk_weight * asset.value
    return total_risk / sum(a.value for a in portfolio)

## 关键问题
1. float溢出风险 - P0级别
2. 缺少None检查 - P1级别''',

        '压缩测试': '''DeepSeek提出视觉因果流
核心: 视觉Token可压缩80%仍准确
实现: DeepEncoder V2架构
结果: 256 tokens 替代 1120 tokens
提升: 32.9% 阅读顺序准确率''',
    }
    
    print('= ' * 30)
    print('  IGP DocMind — 分支树体系')
    print('  "不是一条筋，是一棵树往不同方向长"')
    print('= ' * 30)
    print()
    
    for doc_name, doc_text in test_docs.items():
        print('━' * 45)
        print(f'📄 {doc_name} ({len(doc_text)}字)')
        print('━' * 45)
        
        # 所有分支分析
        results = tree.process_all(doc_text)
        tree.score_all(len(doc_text))
        
        for bid, result in results.items():
            branch = tree.branches[bid]
            r = branch.report()
            
            # 按分支类型展示不同结果
            if 'finance' in bid:
                kv = result.get('key_values', {}) or result.get('key-values', {})
                if isinstance(result, dict):
                    kv_count = len(result.get('key_values', {}))
                    if 'wide' in result:
                        kv_count = result['wide'].get('stats', {}).get('headers', 0)
                    lines_count = result.get('depth', 0) if isinstance(result, dict) else 0
                else:
                    kv_count = 0
                print(f'  🌿 {bid:25s} 分: {r["score"]} | 深度: {result.get("depth", "N/A")}')
            
            elif 'code' in bid:
                codes = result.get('code_blocks', [])
                if isinstance(result, dict) and 'wide' in result:
                    stats = result['wide']['stats']
                    print(f'  🌿 {bid:25s} 分: {r["score"]} | 代码块: {stats.get("codes", 0)}')
                else:
                    print(f'  🌿 {bid:25s} 分: {r["score"]} | 代码块: {len(codes)}')
            
            elif 'compress' in bid:
                stats = result.get('wide', {}).get('stats', {})
                if isinstance(result, dict) and not result.get('wide'):
                    stats = result.get('stats', {})
                print(f'  🌿 {bid:25s} 分: {r["score"]} | 统计: {stats.get("total", 0)}段 {stats.get("headers", 0)}标题')
            
            elif 'graph' in bid:
                kvs = result.get('key_values', {})
                if isinstance(result, dict) and 'deep' in result:
                    d = result['deep']
                    print(f'  🌿 {bid:25s} 分: {r["score"]} | 层级: {d.get("depth", 0)}层 {d.get("tables", 0)}表')
                else:
                    print(f'  🌿 {bid:25s} 分: {r["score"]} | KV: {len(kvs)}个')
        
        print()
    
    # 突变演示
    print('━' * 45)
    print('🧬 分支突变（每3代自动变异）')
    print('━' * 45)
    for i in range(3):
        for bid, branch in tree.branches.items():
            branch.age += 1
            if branch.age % 3 == 0:
                m = branch.mutate()
                if m:
                    old = m['old']
                    new = m['new']
                    print(f'  {bid} 突变:')
                    for k in old:
                        delta = new[k] - old[k]
                        arrow = '↑' if delta > 0 else ('↓' if delta < 0 else '→')
                        if abs(delta) > 0.01:
                            print(f'      {k}: {old[k]:.3f} {arrow} {new[k]:.3f}')
    print()
    
    # 分裂演示：从金融分支分裂出子分支
    finance = tree.branches['branch-A-finance']
    child = finance.spawn('branch-E-fintech')
    tree.branches['branch-E-fintech'] = child
    print('🐣 分支分裂: branch-A-finance → branch-E-fintech')
    print(f'  父向量: {finance.mutation_vector}')
    print(f'  子向量: {child.mutation_vector}')
    print()
    
    # 最终树状态
    print('= ' * 30)
    print(tree.report_tree())
    print('= ' * 30)
    
    # 保存状态
    state = {
        'timestamp': datetime.now().isoformat()[:19],
        'total_branches': len(tree.branches),
        'branches': {bid: t.report() for bid, t in tree.branches.items()},
    }
    with open(os.path.join(DOCMIND_DIR, 'branch_tree.json'), 'w') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print('  ✅ 状态已保存: branch_tree.json')


def main():
    demo_tree()


if __name__ == '__main__':
    main()
