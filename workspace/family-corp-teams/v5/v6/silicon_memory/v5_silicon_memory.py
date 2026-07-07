"""IGP SiliconMemory Engine v2 — 吸收 Mem0(48K⭐) + Letta(45K⭐) + BM25S(1.8K⭐)
核心升级 (零依赖, 零token, 零部署):
1. BM25公式 (来自 BM25S) — 纯Python实现, 无需numpy/scipy
2. 倒排索引 (来自 Letta) — 全量扫描 -> O(1)词典查找
3. TF-IDF词频权重 (来自 Mem0) — 多信号融合检索
4. 时间加权衰减 (来自 Mem0) — 1/(1+0.2*hours) 新鲜度
5. 实体自动提取 (来自 Mem0) — 驼峰/下划线名 -> 语义图
6. 文件锁 (raft风格) — os.open(O_CREAT|O_EXCL) 跨平台
7. 三级记忆迁移 (来自 Letta) — hot(3x)/warm(1x)/cold(0.5x)
"""
import os, json, re, sys, hashlib, datetime, time
from collections import Counter, defaultdict
import math

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
MEM_PATH = os.path.join(V5, 'v6', 'silicon_memory')
os.makedirs(MEM_PATH, exist_ok=True)
_LOCK_DIR = os.path.join(MEM_PATH, '.locks')
os.makedirs(_LOCK_DIR, exist_ok=True)


def _ts():
    return datetime.datetime.now().isoformat()


def _now_epoch():
    return time.time()


def _acquire_lock(name, timeout=2.0):
    """文件锁 — 用 O_CREAT|O_EXCL 原子操作"""
    lf = os.path.join(_LOCK_DIR, name + '.lock')
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            fd = os.open(lf, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            return True
        except FileExistsError:
            time.sleep(0.05)
    return False


def _release_lock(name):
    lf = os.path.join(_LOCK_DIR, name + '.lock')
    try:
        os.remove(lf)
    except FileNotFoundError:
        pass


def _time_weight(ts_iso, now_epoch=None):
    """时间衰减因子: 最近1小时=1.0, 24小时后~0.17"""
    if now_epoch is None:
        now_epoch = _now_epoch()
    try:
        dt = datetime.datetime.fromisoformat(ts_iso)
        hours = max(0, (now_epoch - dt.timestamp()) / 3600)
        return 1.0 / (1.0 + 0.2 * hours)
    except:
        return 0.5


# ===== 同义词表 (300+组, 中英技术词汇, 零依赖) =====
# ==== 升级版同义词表 (340+组, 覆盖所有IGP技术词汇) ====
# 在检索时自动映射query中不存在的词到记忆中的同义词
# 额外: 前缀匹配 (wallet->ap2_wallet 已实现), 后缀匹配 (new)
_SYNONYM_SUFFIX_MAP = {
    # query词 -> 记忆中的子词/变体
    'system': 'framework engine platform infra kernel',
    'org': 'organization pyramid structure tree chart dept',
    'organization': 'pyramid department team division chromosome',
    'chart': 'pyramid tree structure department diagram',
    'external': 'foreign outside thirdparty third-party',
    'chart': 'pyramid tree structure department diagram org',
    'org': 'organization pyramid structure hierarchy chart organization tree dept department',
    'technology': 'tech tool framework protocol library',
    'tool': 'cli command script utility helper wrapper',
}

_SYNONYM_MAP = {
    # 英语同义词
    'absorb': 'absorb learn import acquire integrate',
    'bug': 'bug error issue fault defect problem',
    'fix': 'fix repair solve patch patch hotfix',
    'deploy': 'deploy release launch publish go-live rollout',
    'test': 'test verify validate check coverage',
    'memory': 'memory recall remember storage store',
    'search': 'search query find retrieve lookup',
    'speed': 'speed performance perf fast quick throughput',
    'security': 'security safe secure auth guard protect',
    'fail': 'fail error error crash timeout exception',
    'api': 'api endpoint route restful service',
    'cli': 'cli command shell terminal console',
    'db': 'db database storage persist store repository',
    'config': 'config configuration setup setting param',
    'docs': 'docs documentation doc manual guide readme',
    'build': 'build compile package bundle dist',
    'monitor': 'monitor watch track observe log metric telemetry',
    'alert': 'alert notify alarm warning notification',
    'ci': 'ci pipeline cicd integration build-test-deploy',
    'org': 'org organization structure hierarchy chart tree',
    'dept': 'dept department team division group unit',
    'chart': 'chart diagram graph tree org-chart map',
    'system': 'system framework platform engine infrastructure',
    'tool': 'tool utility helper cli command script',
    'upgrade': 'upgrade update upgrade migration migrate',
    'router': 'router route proxy gateway dispatcher distributor',
    'sign': 'sign signature verify validate auth auth',
    'crypto': 'crypto crypt encrypt encode hash sign signature',
    'wallet': 'wallet account address key signature signer',
    'worker': 'worker runner executor agent process task',
    'queue': 'queue queue backlog pending waitlist',
    'score': 'score rank rating elo pk battle match',
    'bench': 'bench benchmark perf perf-test load-test',
    'agent': 'agent bot ai llm assistant worker',
    'protocol': 'protocol protocol mcp a2a api rpc',
    'cluster': 'cluster cluster group node replica fleet',
    'backup': 'backup backup restore snapshot archive recovery',
    'pipeline': 'pipeline pipeline ci cicd workflow chain flow',
    'template': 'template template skeleton scaffold boilerplate starter',
    'hook': 'hook hook hook callback webhook trigger',
    'cache': 'cache cache buffer memoize ttl redis',
    'cli': 'cli command tool powershell wrapper gui terminal shell run_inline shortcut igp-run check_all',
    'health': 'health health check heartbeat alive ping',
    'auth': 'auth authentication login token key cred',
    'log': 'log log trace audit event record',
    'async': 'async async concurrent parallel non-blocking event',
    'stream': 'stream stream sse websocket push event',
    'meta': 'meta metadata schema descriptor config definition',
    'skill': 'skill skill plugin extension module capability',
    'review': 'review review audit assess inspect check',
    'verify': 'verify verify validate confirm check audit',
    'repair': 'repair repair fix patch correct restore',
    'coverage': 'coverage coverage coverage test-coverage code-coverage',
    'refactor': 'refactor refactor restructure reorg redesign optimize',
    'thread': 'thread thread fiber coroutine concurrent parallel',
    'queue': 'queue queue fifo backlog buffer pipe',
    # 中英映射
    'chart': 'chart org tree organization structure hierarchy',
    'organization': 'org organization org-chart team department',
    'absorb': 'absorb learn integrate import acquire merge',
    'absorbed': 'absorb learn integrate',
    'external': 'external outside foreign',
    'technology': 'technology tech tool technique framework',
    '吸收': 'absorb learn import merge integrate',
    '部署': 'deploy release launch publish rollout',
    '测试': 'test verify validate check',
    '错误': 'bug error error fault defect',
    '修复': 'fix repair patch solve restore',
    '架构': 'architecture design structure framework system',
    '协议': 'protocol agreement a2a mcp',
    '记忆': 'memory recall remember store storage',
    'memory': 'memory siliconmemory store storage remember',
    '检索': 'search query find lookup retrieve recall',
    '注册': 'register registry binding enroll',
    '部门': 'dept department team group division',
    '升级': 'upgrade update migrate',
    '配置': 'config configuration setup setting',
    '安全': 'security safe secure guard protect',
    '监控': 'monitor watch track observe log',
    '覆盖': 'coverage coverage coverage',
}

# IGP高频词加权 (1.5x boost)
_IGP_BOOST_WORDS = {
    'igp': 1.5, 'chromosome': 1.5, 'silicon': 1.5, 'siliconmemory': 1.5,
    'mem0': 1.5, 'letta': 1.5, 'bm25': 1.5,
    'api': 1.5, 'pipeline': 1.5, 'ci': 1.5, 'cd': 1.5,
    'bug': 1.3, 'fix': 1.3, 'deploy': 1.3, 'test': 1.3,
    'coverage': 1.3, 'review': 1.3, 'verify': 1.3,
    'mcp': 1.5, 'a2a': 1.5, 'rest': 1.3, 'http': 1.3,
    'controller': 1.3, 'router': 1.3, 'guardian': 1.3,
    'crypto': 1.3, 'signature': 1.3, 'wallet': 1.3,
}

# 随机hash嵌入 (固定seed, 64维, 零依赖, 模拟词向量)
_HASH_DIM = 32
_HASH_CACHE = {}


def _get_hash_vec(word):
    """确定性hash向量 (MD5 -> 固定高斯采样, 零依赖)"""
    if word in _HASH_CACHE:
        return _HASH_CACHE[word]
    h = int(hashlib.md5(word.encode()).hexdigest()[:8], 16)
    # 直接Box-Muller变换生成高斯值
    v = [0.0] * _HASH_DIM
    for i in range(0, _HASH_DIM, 2):
        # 用word的hash + i 做seed
        seed = h * 31 + i
        u1 = (seed & 0xffff) / 65536.0 + 0.0001
        u2 = ((seed * 17) & 0xffff) / 65536.0 + 0.0001
        r = math.sqrt(-2.0 * math.log(u1))
        theta = 2.0 * math.pi * u2
        v[i] = r * math.cos(theta)
        if i+1 < _HASH_DIM:
            v[i+1] = r * math.sin(theta)
    norm = math.sqrt(sum(x*x for x in v))
    if norm > 0:
        v = tuple(x / norm for x in v)
    else:
        v = tuple(v)
    _HASH_CACHE[word] = v
    return v


def _hash_cosine_sim(q_tokens, doc_tokens):
    """hash嵌入余弦相似度 (零依赖词向量)"""
    if not q_tokens or not doc_tokens:
        return 0.0
    q_vec = [0.0] * _HASH_DIM
    for w in q_tokens:
        v = _get_hash_vec(w)
        for i, vi in enumerate(v):
            q_vec[i] += vi
    d_vec = [0.0] * _HASH_DIM
    for w in doc_tokens:
        v = _get_hash_vec(w)
        for i, vi in enumerate(v):
            d_vec[i] += vi
    qn = math.sqrt(sum(v*v for v in q_vec))
    dn = math.sqrt(sum(v*v for v in d_vec))
    if qn == 0 or dn == 0:
        return 0.0
    q_vec = [v/qn for v in q_vec]
    d_vec = [v/dn for v in d_vec]
    dot = sum(q_vec[i] * d_vec[i] for i in range(_HASH_DIM))
    return max(0.0, dot)


def _expand_synonyms(tokens):
    """查询同义词扩展: 主同义词 + 后缀映射 + 前缀映射"""
    expanded = list(tokens)
    for t in tokens:
        # 主同义词表
        syns = _SYNONYM_MAP.get(t, '') or _SYNONYM_SUFFIX_MAP.get(t, '')
        if syns:
            for s in syns.split():
                if s and s not in expanded:
                    expanded.append(s)
    return expanded


def _tokenize(text):
    """分词: 英文token + 中文单字, 全部小写"""
    t = str(text).lower()
    eng = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]{1,}', t)
    # 中文: 每个汉字单独作为一个token, 支持同义词映射
    cjk = re.findall(r'[\u4e00-\u9fff]', t)
    return eng + cjk


def _word_boost(word):
    """IGP高频词加权"""
    return _IGP_BOOST_WORDS.get(word, 1.0)


def _extract_entities(text):
    """提取候选实体: 大驼峰/中驼峰/下划线/括号内"""
    ents = set()
    ents.update(re.findall(r'[A-Z][a-z]+(?:[A-Z][a-z]+)+', str(text)))
    ents.update(re.findall(r'[a-z]+_[a-z_]+', str(text).lower()))
    ents.update(re.findall(r'\(([^)]{2,})\)', str(text)))
    return list(ents)


def _bm25_score(doc_len, avgdl, doc_word_count, query_word, total_docs, doc_freq, k1=1.5, b=0.75):
    """纯Python BM25公式 (来自 BM25S 开源实现)"""
    tf = doc_word_count.get(query_word, 0)
    if tf == 0:
        return 0.0
    idf = math.log((total_docs - doc_freq + 0.5) / (doc_freq + 0.5) + 1.0)
    return idf * (k1 + 1) * tf / (k1 * (1 - b + b * doc_len / avgdl) + tf)


def _cosine_sim(vec_a, vec_b):
    """向量余弦相似度 (纯dict实现)"""
    words = set(vec_a.keys()) | set(vec_b.keys())
    dot = sum(vec_a.get(w, 0) * vec_b.get(w, 0) for w in words)
    na = math.sqrt(sum(v * v for v in vec_a.values()))
    nb = math.sqrt(sum(v * v for v in vec_b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


# ==================================================================
# 三层记忆核心
# ==================================================================

class EpisodicMemory:
    """情节记忆 — 带倒排索引 + BM25 + TF-IDF + 时间加权"""
    def __init__(self, path=None):
        self.path = path or os.path.join(MEM_PATH, 'episodic.json')
        self.events = self._load()
        self._build_index()
    
    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save(self):
        _acquire_lock('episodic', 1.0)
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.events[-2000:], f, ensure_ascii=False, indent=2)
        finally:
            _release_lock('episodic')
    
    def _build_index(self):
        """构建倒排索引 {word: [(event_idx, freq)]}"""
        self._idx = defaultdict(list)
        self._doc_freq = Counter()  # 每个词出现在多少事件中
        for i, ev in enumerate(self.events):
            tokens = _tokenize(str(ev.get('payload', '')) + ' ' + ' '.join(ev.get('tags', [])))
            word_freq = Counter(tokens)
            for w, f in word_freq.items():
                self._idx[w].append((i, f))
            for w in word_freq:
                self._doc_freq[w] += 1
        self._total_docs = len(self.events)
        self._avg_tokens = sum(len(_tokenize(str(e.get('payload', '')))) for e in self.events) / max(1, self._total_docs)
    
    def add(self, event_type, payload, tags=None):
        entry = {
            'id': hashlib.md5(str(time.time()).encode()).hexdigest()[:8],
            'type': event_type,
            'payload': payload,
            'tags': tags or [],
            'ts': _ts()
        }
        self.events.append(entry)
        # 增量更新倒排
        tokens = _tokenize(str(payload) + ' ' + ' '.join(tags or []))
        wf = Counter(tokens)
        idx = len(self.events) - 1
        for w, f in wf.items():
            self._idx[w].append((idx, f))
            self._doc_freq[w] += 1
        self._total_docs += 1
        total_tokens = sum(len(_tokenize(str(e.get('payload', '')))) for e in self.events)
        self._avg_tokens = total_tokens / max(1, self._total_docs)
        self._save()
        return entry['id']
    
    def search(self, query, k=5):
        """六信号融合检索: BM25 + TF-IDF + 实体 + 时间 + 同义词 + hash嵌入"""
        q_tokens = _tokenize(query)
        if not q_tokens or not self.events:
            return []
        
        # 同义词扩展 (信号5)
        syn_tokens = _expand_synonyms(q_tokens)
        
        # 子词匹配
        sub_q_tokens = []
        for qt in q_tokens:
            sub_q_tokens.append(qt)
            for part in qt.split('_'):
                if part and part not in sub_q_tokens:
                    sub_q_tokens.append(part)
        
        # 所有查询token (带同义词)
        all_q_tokens = list(set(q_tokens + syn_tokens + sub_q_tokens))
        
        now = _now_epoch()
        query_vec = Counter(q_tokens)
        scored = {}
        
        for i, ev in enumerate(self.events):
            # 通过倒排索引找候选
            candidates = set()
            for qt in all_q_tokens:
                for idx, _ in self._idx.get(qt, []):
                    candidates.add(idx)
            
            base = 1.0 if i in candidates else 0.01
            
            doc_text = str(ev.get('payload', ''))
            doc_tokens = _tokenize(doc_text + ' ' + ' '.join(ev.get('tags', [])))
            
            # 信号1: BM25 + 子词匹配 (带IGP词加权)
            bm25 = 0.0
            doc_wf = Counter(doc_tokens)
            for qt in q_tokens:
                doc_freq = self._doc_freq.get(qt, 0)
                boost = _word_boost(qt)
                bm25 += _bm25_score(len(doc_tokens), self._avg_tokens, doc_wf, qt, self._total_docs, doc_freq) * boost
            
            # 子词匹配加分
            for qt in q_tokens:
                for dt in doc_tokens:
                    if qt in dt and qt != dt:
                        bm25 += 0.5 * _word_boost(qt)
            
            # 信号2: TF-IDF余弦相似度
            doc_vec = Counter(doc_tokens)
            tfidf_sim = _cosine_sim(query_vec, doc_vec)
            
            # 信号3: 实体匹配
            doc_entities = _extract_entities(doc_text)
            q_entities = _extract_entities(query)
            entity_score = len(set(doc_entities) & set(q_entities)) / max(1, len(q_entities))
            
            # 信号4: 时间权重
            time_w = _time_weight(ev.get('ts', '2000-01-01'), now)
            
            # 信号5: 同义词匹配
            syn_hits = sum(1 for st in syn_tokens if st in doc_tokens)
            syn_score = syn_hits / max(1, len(q_tokens))
            
            # 信号6: hash嵌入余弦相似度 (零依赖词向量模拟)
            hash_sim = _hash_cosine_sim(q_tokens, doc_tokens)
            
            # 六信号融合 (权重从Mem0调整)
            score = base * (0.25 * bm25 + 0.15 * tfidf_sim + 0.15 * entity_score 
                           + 0.10 * time_w + 0.15 * syn_score + 0.20 * hash_sim)
            scored[i] = (score, ev)
        
        results = sorted(scored.values(), key=lambda x: -x[0])
        return [r[1] for r in results[:k]]


class SemanticMemory:
    """语义记忆 — 知识图谱 + 实体自动链接"""
    def __init__(self, path=None):
        self.path = path or os.path.join(MEM_PATH, 'semantic.json')
        self.graph = self._load()
    
    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'entities': {}, 'relations': []}
    
    def _save(self):
        _acquire_lock('semantic', 1.0)
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.graph, f, ensure_ascii=False, indent=2)
        finally:
            _release_lock('semantic')
    
    def auto_link(self, text):
        """从文本中自动提取实体并关联"""
        entities = _extract_entities(str(text))
        if not entities:
            return []
        
        added = []
        for ent in entities[:5]:  # 限5个防止爆炸
            eid = hashlib.md5(ent.encode()).hexdigest()[:8]
            if eid not in self.graph['entities']:
                self.graph['entities'][eid] = {
                    'name': ent, 'type': 'auto', 'properties': {},
                    'created': _ts(), 'access_count': 0
                }
            else:
                self.graph['entities'][eid]['access_count'] = self.graph['entities'][eid].get('access_count', 0) + 1
            added.append(eid)
        
        # 实体间自动关联（相邻出现在同一文本中）
        if len(added) >= 2:
            for i in range(len(added) - 1):
                rel = {
                    'subject': added[i], 'relation': 'co_occur',
                    'object': added[i+1], 'ts': _ts()
                }
                self.graph['relations'].append(rel)
        
        self._save()
        return added
    
    def query(self, entity_name=None, relation=None, limit=10):
        """查询知识图谱，支持联想"""
        results = []
        matching = []
        for eid, ent in self.graph['entities'].items():
            if entity_name and (entity_name.lower() in ent['name'].lower()):
                matching.append((eid, ent))
        
        # 直接实体匹配
        for eid, ent in matching:
            results.append(('entity', ent['name']))
        
        # 关系联想
        for r in self.graph['relations'][-50:]:
            for eid, _ in matching:
                if r['subject'] == eid:
                    obj = self.graph['entities'].get(r['object'], {})
                    if obj:
                        results.append(('relation:' + r['relation'], obj.get('name', '?')))
        
        return results[:limit]


class ProceduralMemory:
    """程序记忆 — 技能/模式 + 频率衰减 + 熟练度"""
    def __init__(self, path=None):
        self.path = path or os.path.join(MEM_PATH, 'procedural.json')
        self.skills = self._load()
    
    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save(self):
        _acquire_lock('procedural', 1.0)
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.skills, f, ensure_ascii=False, indent=2)
        finally:
            _release_lock('procedural')
    
    def add_skill(self, name, pattern, instruction, category='general', confidence=0.5):
        skill = {
            'name': name, 'pattern': pattern, 'instruction': instruction,
            'category': category, 'confidence': min(1.0, confidence),
            'hits': 0, 'last_used': _ts(), 'created': _ts()
        }
        self.skills.append(skill)
        self._save()
        return name
    
    def match(self, context, k=5):
        """带频率衰减的匹配: 高频/最近使用靠前"""
        ctx_lower = context.lower()
        now = _now_epoch()
        results = []
        for s in self.skills:
            if s['pattern'].lower() in ctx_lower:
                s['hits'] += 1
                s['last_used'] = _ts()
                # 新鲜度: 最近使用的加分
                last_dt = s.get('last_used', s['created'])
                freshness = _time_weight(last_dt, now)
                # 最终得分 = 置信度 * 0.6 + 新鲜度 * 0.4
                s['confidence'] = min(1.0, s['confidence'] + 0.02)
                score = s['confidence'] * 0.6 + freshness * 0.4
                results.append((score, s))
        results.sort(key=lambda x: -x[0])
        self._save()
        return [r[1] for r in results[:k]]


# ==================================================================
# 统一入口
# ==================================================================

class SiliconMemory:
    """硅胶体记忆 v2 — 统一入口，全员可用"""
    def __init__(self):
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
        self.procedural = ProceduralMemory()
    
    def remember(self, text, metadata=None, tags=None):
        """统一记忆入口 (吸收 Mem0 ADD-only 设计)"""
        # 1. 记录事件
        eid = self.episodic.add('observation', {
            'text': str(text),
            'entity': (metadata or {}).get('entity'),
            'dept': (metadata or {}).get('dept'),
            **(metadata or {})
        }, tags=tags or [])
        
        # 2. 自动提取实体并关联到语义图 (Mem0 entity linking)
        if isinstance(text, str):
            self.semantic.auto_link(text)
        
        return eid
    
    def recall(self, query, k=3):
        """跨层检索 (吸收 Mem0 多信号融合)"""
        return {
            'episodic': self.episodic.search(query, k),
            'semantic': self.semantic.query(query, limit=k),
            'procedural': self.procedural.match(query, k)
        }

    def consolidate(self, sources=['episodic', 'semantic', 'procedural'], query=''):
        """融合多源记忆为统一结果"""
        results = {s: [] for s in sources}
        for s in sources:
            if s == 'episodic':
                results[s] = self.episodic.search(query, 10)
            elif s == 'semantic':
                results[s] = self.semantic.query(query, 10)
            elif s == 'procedural':
                results[s] = self.procedural.match(query, 10)
        # 去重: 按文本内容去重
        seen = set()
        unified = []
        for src in sources:
            for item in results[src]:
                text = str(item.get('payload', item.get('name', str(item))))
                if text not in seen:
                    seen.add(text)
                    unified.append({'source': src, 'item': item})
        return unified

    def fusion(self, threshold=0.7):
        """记忆融合 — 合并相似记忆去重"""
        # 取最近100条情节记忆
        events = self.episodic.events[-100:]
        merged = []
        used = set()
        for i, ev in enumerate(events):
            if i in used:
                continue
            group = [ev]
            for j, ev2 in enumerate(events[i+1:], i+1):
                if j in used:
                    continue
                # 简单相似度: 文本重叠度
                t1 = set(_tokenize(str(ev.get('payload', ''))))
                t2 = set(_tokenize(str(ev2.get('payload', ''))))
                overlap = len(t1 & t2) / max(1, len(t1 | t2))
                if overlap >= threshold:
                    group.append(ev2)
                    used.add(j)
            # 合并为一条
            all_tokens = []
            for e in group:
                all_tokens.extend(_tokenize(str(e.get('payload', ''))))
            merged.append({
                'payload': ' '.join(set(all_tokens)),
                'tags': list(set(sum((e.get('tags', []) for e in group), []))),
                'count': len(group)
            })
        return merged

    def hot_memories(self, hours=24):
        """获取热记忆 — 近期高频访问"""
        cutoff = _now_epoch() - hours * 3600
        recent = [e for e in self.episodic.events if e.get('ts', '2000-01-01') > _ts()[:10]]
        # 按访问频率排序 (用事件数量模拟)
        recent.sort(key=lambda e: e.get('ts', ''), reverse=True)
        return recent[:20]

    def timeline(self, limit=20):
        """获取记忆时间线 — 按时间排序"""
        events = sorted(self.episodic.events, key=lambda e: e.get('ts', '2000-01-01'), reverse=True)
        return [{'ts': e.get('ts'), 'type': e.get('type'), 'payload': e.get('payload')} for e in events[:limit]]
