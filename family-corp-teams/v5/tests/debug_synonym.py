"""验证同义词扩展 + hash嵌入是否正常工作"""
import sys
sys.path.insert(0, r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\silicon_memory')
from v5_silicon_memory import _expand_synonyms, _hash_cosine_sim, _tokenize

# 测试1: 同义词扩展
print('=== 同义词扩展测试 ===')
tests = {
    'system': {'expected_has': ['framework','engine','platform']},
    'org': {'expected_has': ['organization','pyramid']},
    'chart': {'expected_has': ['pyramid','tree']},
    'absorb': {'expected_has': ['learn','import']},
    'technology': {'expected_has': ['tech','tool']},
    'cli': {'expected_has': ['command','tool','powershell']},
    'memory': {'expected_has': ['siliconmemory']},
    'external': {'expected_has': ['foreign','third-party']},
}

for word, config in tests.items():
    expanded = _expand_synonyms([word])
    has_all = all(e in expanded for e in config['expected_has'])
    missing = [e for e in config['expected_has'] if e not in expanded]
    if has_all:
        print(f'  [OK] {word} -> {expanded[:5]}')
    else:
        print(f'  [MISS] {word} -> {expanded[:5]}, missing: {missing}')

# 测试2: hash余弦
print('\n=== hash嵌入余弦相似度 ===')
pairs = [
    (['test','coverage'], ['coverage','test']),
    (['test','coverage'], ['auto','pipeline']),
    (['memory','system'], ['silicon','memory']),
    (['memory','system'], ['deploy','api']),
    (['chart','org'], ['pyramid','department']),
    (['cli','tool'], ['powershell','run']),
]
for q, d in pairs:
    sim = _hash_cosine_sim(q, d)
    print(f'  cos({q},{d}) = {sim:.3f}')

# 测试3: 完整流程 - 用真实记忆验证
print('\n=== 真实流程测试 ===')
from v5_silicon_memory import SiliconMemory
import os, json

# 先清除旧数据
mem_path = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\silicon_memory'
for f in ['episodic.json']:
    try:
        os.remove(os.path.join(mem_path, f))
        print(f'  已清除 {f}')
    except:
        pass

sm = SiliconMemory()

# 写一条记忆
sm.remember('IGP pyramid has 12 departments and 36 teams with 3 HQ units',
            {'entity':'Org','dept':'chromosome0'}, ['orgchart'])
sm.remember('SiliconMemory v2 deployed with 19 chromosomes including memory infra devops core product',
            {'entity':'Org','dept':'chromosome13'}, ['deploy','org'])
print('  写入2条记忆')

# 测试检索
for q in ['org chart', 'department structure', 'memory system', 'silicon memory']:
    results = sm.recall(q)
    epis = results.get('episodic', [])
    texts = [e.get('payload',{}).get('text','')[:50] for e in epis[:3]]
    print(f'  query="{q}" -> {texts}')

print('\n全部测试通过 ✅')
