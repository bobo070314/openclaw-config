"""
知识进化引擎 v2 — knowledge.py + DocMind DNA编码融合
从关键词索引 → 序列对齐 + 突变检测
"""
import os, json, re
from datetime import datetime

FAMILY = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams"
PROJECTS = os.path.join(FAMILY, 'projects')
INDEX_FILE = os.path.join(os.path.dirname(__file__), 'index_evo.json')

# DNA编码器：把代码行当碱基编码
def code_to_dna(text):
    mapping = {'i':'A','m':'T','p':'G','r':'C','o':'C','t':'G','s':'A','f':'T','d':'G','e':'A','l':'T','n':'C','h':'G','a':'A','c':'T','b':'C','u':'G'}
    dna = ''
    for ch in text.lower():
        if ch in mapping:
            dna += mapping[ch]
            if len(dna) >= 100:
                break
    return dna

# 序列对齐搜索
def dna_search(dna, query_dna):
    if not dna or not query_dna:
        return 0
    matches = sum(1 for i in range(len(dna)-len(query_dna)+1) if dna[i:i+len(query_dna)] == query_dna)
    return matches

def build_index():
    index = {}
    for root, dirs, files in os.walk(PROJECTS):
        for fname in files:
            if not fname.endswith('.py'):
                continue
            fp = os.path.join(root, fname)
            content = open(fp, encoding='utf-8').read()
            rel = os.path.relpath(fp, FAMILY)
            dna = code_to_dna(content)
            words = set(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', content.lower()))
            index[rel] = {'path': rel, 'len': len(content), 'dna': dna, 'words': len(words)}
    json.dump(index, open(INDEX_FILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return index

def search(query):
    index = json.load(open(INDEX_FILE, encoding='utf-8'))
    query_dna = code_to_dna(query)
    results = []
    for fpath, info in index.items():
        query_words = set(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', query.lower()))
        content_words = set(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', query.lower()))  # placeholder
        dna_score = dna_search(info['dna'], query_dna)
        results.append((fpath, dna_score))
    results.sort(key=lambda x: -x[1])
    return results[:5]

def main():
    index = build_index()
    print(json.dumps({'files': len(index), 'status': 'evo_ok'}))

if __name__ == '__main__':
    main()
