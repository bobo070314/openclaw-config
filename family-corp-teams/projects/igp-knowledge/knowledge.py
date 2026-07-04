"""
IGP AI知识库向量化 — 本地Embedding搜索
用DocMind做本地文档智能检索
"""
import os, sys, json, re
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
OUT = os.path.join(FAMILY, 'projects', 'igp-knowledge')
os.makedirs(OUT, exist_ok=True)

# 简单向量搜索（不用第三方库，用词频+倒排索引）
class TinyVectorDB:
    """超轻量本地Embedding"""
    
    def __init__(self):
        self.docs = []
        self.index = {}  # word → [doc_id]
    
    def add(self, doc_id, text):
        self.docs.append({'id': doc_id, 'text': text})
        idx = len(self.docs) - 1
        words = set(re.findall(r'[a-zA-Z\u4e00-\u9fff]+', text.lower()))
        for w in words:
            if w not in self.index:
                self.index[w] = []
            self.index[w].append(idx)
    
    def search(self, query, top=3):
        words = set(re.findall(r'[a-zA-Z\u4e00-\u9fff]+', query.lower()))
        scores = {}
        for w in words:
            if w in self.index:
                for idx in self.index[w]:
                    scores[idx] = scores.get(idx, 0) + 1
        
        sorted_results = sorted(scores.items(), key=lambda x: -x[1])
        results = []
        for idx, score in sorted_results[:top]:
            results.append({
                'id': self.docs[idx]['id'],
                'text': self.docs[idx]['text'][:100],
                'score': score,
            })
        return results


# 创建知识库
print('╔' + '═'*46 + '╗')
print('║  IGP知识库 v1 — 本地向量搜索')
print('╚' + '═'*46 + '╝')
print()

db = TinyVectorDB()

# 索引所有项目文件
all_projects = sorted(os.listdir(os.path.join(FAMILY, 'projects')))
total_files = 0

for p in all_projects:
    pp = os.path.join(FAMILY, 'projects', p)
    if not os.path.isdir(pp):
        continue
    for f in os.listdir(pp):
        fp = os.path.join(pp, f)
        if not os.path.isfile(fp) or not (f.endswith('.py') or f.endswith('.md')):
            continue
        try:
            text = open(fp, encoding='utf-8').read()
            doc_id = f'{p}/{f}'
            db.add(doc_id, text[:5000])  # 最多5K字
            total_files += 1
        except:
            pass

print(f'  索引完成: {total_files}文件 | {len(db.docs)}文档块 | {len(db.index)}关键词')
print()

# 测试搜索
test_queries = ['DocMind', '自愈', '进化', '淘汰', '金融']
for q in test_queries:
    results = db.search(q)
    if results:
        print(f'  🔍 "{q}":')
        for r in results:
            print(f'     [{r["score"]}] {r["id"]}')
            print(f'         {r["text"]}')
    else:
        print(f'  🔍 "{q}": 无结果')
    print()

# 保存
with open(os.path.join(OUT, 'knowledge_base.json'), 'w') as f:
    json.dump({
        'total_docs': len(db.docs),
        'total_words': len(db.index),
        'created_at': datetime.now().isoformat()[:19],
    }, f)

import json as j2
with open(os.path.join(OUT, 'index_data.json'), 'w') as f:
    j2.dump({'docs': db.docs, 'index': {k: v for k, v in list(db.index.items())[:100]}}, f, ensure_ascii=False, indent=2)

print(f'  ✅ 已保存: knowledge_base.json + index_data.json')
print(f'  📍 {OUT}')

if __name__ == '__main__':
    print('OK')
