"""深度诊断: org chart department 为什么查不到"""
import sys, os, json
sys.path.insert(0, r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\silicon_memory')
sys.path.insert(0, r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5')
from v5_silicon_memory import SiliconMemory, _expand_synonyms, _hash_cosine_sim, _tokenize, _SYNONYM_SUFFIX_MAP

# 先用旧数据看看
mem_path = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\silicon_memory'
ep = os.path.join(mem_path, 'episodic.json')

if os.path.exists(ep):
    with open(ep, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for i, ev in enumerate(data):
        txt = str(ev.get('payload', {}).get('text', ''))
        toks = _tokenize(txt)
        print(f'[{i}] {txt[:60]}')
        print(f'    tokens: {toks[:15]}...')
        
        # 查 "chart" 同义词
        syns = _expand_synonyms(['chart', 'org', 'department'])
        print(f'    syns(org,chart,dep): {syns[:10]}')
        for s in syns:
            if s in toks:
                print(f'    [MATCH] syn "{s}" in tokens!')
        
        # hash余弦
        q = ['chart', 'org', 'department']
        hc = _hash_cosine_sim(q, toks)
        print(f'    hash_cos({q}, ...) = {hc:.4f}')
        print()
else:
    print(f'episodic.json not found at {ep}')
    sm = SiliconMemory()
    results = sm.recall('org chart department')
    print(f'episodic keys: {list(results.keys())}')
    epi = results.get('episodic', [])
    print(f'num results: {len(epi)}')
    for e in epi[:3]:
        print(f'  text: {str(e.get(\"payload\",{}).get(\"text\",\"\"))[:60]}')
        print(f'  score: {e.get(\"score\",\"?\")}')
