"""IGP SiliconMemory Indexer — 倒排索引 + TF-IDF + 实体提取 + 冲突检测
裂变产物 (来自 Letta 索引分离设计)
零依赖, 纯Python stdlib
"""
import re, math
from collections import Counter, defaultdict

__all__ = ['InvertedIndex', 'TfidfScorer', 'EntityExtractor', 'ConflictDetector']


def _tokenize(text):
    return re.findall(r'[a-zA-Z_][a-zA-Z0-9_]{1,}', str(text).lower())


class InvertedIndex:
    """倒排索引 — {word: [(doc_id, freq)]}"""
    def __init__(self):
        self.index = defaultdict(list)
        self.n_docs = 0
    
    def add(self, doc_id, text):
        tokens = _tokenize(text)
        wf = Counter(tokens)
        for w, f in wf.items():
            self.index[w].append((doc_id, f))
        self.n_docs += 1
    
    def lookup(self, word):
        return self.index.get(word, [])
    
    def multi_lookup(self, words):
        """查找多个词的倒排列表"""
        c = Counter()
        for w in words:
            for did, freq in self.index.get(w, []):
                c[did] += freq
        return c.most_common()
    
    def remove(self, doc_id):
        for w in list(self.index.keys()):
            self.index[w] = [(did, f) for did, f in self.index[w] if did != doc_id]
            if not self.index[w]:
                del self.index[w]


class TfidfScorer:
    """TF-IDF 向量空间评分 (纯dict实现)"""
    def __init__(self):
        self.doc_freq = Counter()
        self.n_docs = 0
    
    def fit(self, corpus_tokenized):
        self.n_docs = len(corpus_tokenized)
        for tokens in corpus_tokenized:
            for w in set(tokens):
                self.doc_freq[w] += 1
    
    def tfidf(self, query_tokens, doc_tokens):
        """单文档TF-IDF向量"""
        qf = Counter(query_tokens)
        df = Counter(doc_tokens)
        vec = {}
        for w in set(list(qf.keys()) + list(df.keys())):
            tf = df.get(w, 0) / max(1, len(doc_tokens))
            idf = math.log((self.n_docs + 1) / (self.doc_freq.get(w, 0) + 1)) + 1
            vec[w] = tf * idf
        return vec
    
    def similarity(self, query_tokens, doc_tokens):
        """TF-IDF余弦相似度"""
        if not query_tokens or not doc_tokens:
            return 0.0
        qvec = self.tfidf(query_tokens, query_tokens)
        dvec = self.tfidf(query_tokens, doc_tokens)
        words = set(qvec.keys()) | set(dvec.keys())
        dot = sum(qvec.get(w, 0) * dvec.get(w, 0) for w in words)
        nq = math.sqrt(sum(v*v for v in qvec.values()))
        nd = math.sqrt(sum(v*v for v in dvec.values()))
        if nq == 0 or nd == 0:
            return 0.0
        return dot / (nq * nd)


class EntityExtractor:
    """实体提取器 (来自 Mem0 entity linking)"""
    PATTERNS = [
        (r'[A-Z][a-z]+(?:[A-Z][a-z]+)+', 'large_camel'),
        (r'[a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)+', 'dotted'),
        (r'[a-z]+_[a-z_]+', 'snake'),
        (r'\(([^)]{3,})\)', 'parenthesis'),
    ]
    
    def extract(self, text):
        """提取所有实体"""
        entities = {}
        for pat, label in self.PATTERNS:
            for m in re.finditer(pat, str(text)):
                name = m.group(1) if m.groups() else m.group(0)
                if name not in entities:
                    entities[name] = {'name': name, 'type': label, 'pos': m.start()}
        return list(entities.values())


class ConflictDetector:
    """冲突/冗余检测 (来自 Mem0 memory fusion)"""
    def __init__(self, threshold=0.75):
        self.threshold = threshold
    
    def _levenshtein(self, a, b):
        """编辑距离 (纯Python, DP)"""
        if len(a) < len(b):
            a, b = b, a
        prev = list(range(len(b) + 1))
        for i, ca in enumerate(a):
            curr = [i + 1]
            for j, cb in enumerate(b):
                cost = 0 if ca == cb else 1
                curr.append(min(
                    curr[j] + 1,       # delete
                    prev[j + 1] + 1,   # insert
                    prev[j] + cost     # replace
                ))
            prev = curr
        return prev[-1]
    
    def similarity(self, a, b):
        """文本相似度 [0,1]"""
        if not a and not b:
            return 1.0
        if not a or not b:
            return 0.0
        levenshtein = self._levenshtein(a, b)
        return 1.0 - levenshtein / max(len(a), len(b))
    
    def is_conflict(self, existing, new):
        """检测是否冲突/冗余"""
        return self.similarity(existing, new) >= self.threshold
    
    def merge_texts(self, texts):
        """合并相似文本 (取最长独立内容)"""
        kept = []
        for t in texts:
            dup = False
            for k in kept:
                if self.is_conflict(t, k):
                    dup = True
                    break
            if not dup:
                kept.append(t)
        return kept
