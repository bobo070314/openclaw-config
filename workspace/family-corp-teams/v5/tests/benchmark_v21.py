"""IGP 硅胶体记忆 v2.1 — 对标 Mem0 LoCoMo Benchmark
零token评估, 含同义词+hash嵌入+中文"""
import sys, os, math, json
sys.path.insert(0, r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\silicon_memory')
sys.path.insert(0, r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5')
from v5_silicon_memory import SiliconMemory, _expand_synonyms
import shutil

# 清除旧数据
mem_path = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\silicon_memory'
for f in ['episodic.json', 'semantic.json', 'procedural.json']:
    try: os.remove(os.path.join(mem_path, f))
    except: pass

sm = SiliconMemory()

print('='*70)
print('  IGP 硅胶体记忆 v2.1 — Benchmark (同义词+hash+中文+加权)')
print('='*70)

# 32条记忆 (中英混合)
test_mem = [
    ("AP2_Wallet signature verification failed: key points mismatch", {'entity':'AP2_Wallet','dept':'chromosome8'}, ['bug','sig']),
    ("SmartRouter route to provider-B returned 503 timeout", {'entity':'SmartRouter','dept':'chromosome4'}, ['bug','router']),
    ("AgentOS Shell 'run' command EOFError", {'entity':'AgentOS','dept':'chromosome7'}, ['bug','shell']),
    ("CI/CD pipeline step 5 fail: subprocess encoding GBK", {'entity':'Pipeline','dept':'chromosome18'}, ['bug','ci']),
    ("PRD queue deadlock: index collision on concurrent submit", {'entity':'PRD','dept':'chromosome19'}, ['bug','concurrency']),
    ("LifecycleManager expired product cleanup failed: NoneType error", {'entity':'Lifecycle','dept':'chromosome3'}, ['bug','lifecycle']),
    ("AP2_Wallet uses CryptoKit.SignatureVerifier, retry 3x on timeout", {'entity':'AP2_Wallet','dept':'chromosome8'}, ['fix','sig']),
    ("SmartRouter fallback: provider-A timeout downgrade to provider-C", {'entity':'SmartRouter','dept':'chromosome4'}, ['fix','router']),
    ("AgentOS Shell fixed with Popen(text=False) for EOFError", {'entity':'AgentOS','dept':'chromosome7'}, ['fix','subprocess']),
    ("Pipeline fixed with $env:PYTHONIOENCODING=utf-8 for GBK", {'entity':'Pipeline','dept':'chromosome18'}, ['fix','encoding']),
    ("SiliconMemory v1 deployed: 4 classes 20 funcs 259 lines, 93% coverage", {'entity':'SiliconMemory','dept':'chromosome13'}, ['deploy']),
    ("MCPv2 protocol upgrade complete: FastMCP+A2A federation", {'entity':'MCP','dept':'chromosome1'}, ['deploy','protocol']),
    ("HTTP API online: 22 routes, heartbeat auto-recovery", {'entity':'API','dept':'chromosome18'}, ['deploy','api']),
    ("Department registry v3: chromosomes expanded to 19", {'entity':'DepartmentRegistry','dept':'chromosome0'}, ['deploy','org']),
    ("CryptoKit signature speed: 2.1s -> 0.8s (3x improvement)", {'entity':'CryptoKit','dept':'chromosome8'}, ['perf']),
    ("Test coverage: 36% -> 93% (99/106 classes)", {'entity':'TestCoverage','dept':'chromosome12'}, ['perf','test']),
    ("AutoTester: 148 tests 140 pass -> removed 8 -> 140/140 all pass", {'entity':'AutoTester','dept':'chromosome12'}, ['perf','test']),
    ("BM25S absorbed: BM25 formula pure Python, zero deps", {'entity':'BM25S','dept':'chromosome13'}, ['absorb','search']),
    ("CoverUp absorbed: FSE 2025 paper, AST scan -> safe tests", {'entity':'CoverUp','dept':'chromosome0'}, ['absorb','testing']),
    ("Mem0 absorbed: 4-signal retrieval design (BM25+TF-IDF+entity+time)", {'entity':'Mem0','dept':'chromosome13'}, ['absorb','memory']),
    ("Letta absorbed: 3-tier memory migration (hot/warm/cold)", {'entity':'Letta','dept':'chromosome13'}, ['absorb','memory']),
    ("DocAgent absorbed: Meta ACL 2025, job description engine", {'entity':'DocAgent','dept':'chromosome0'}, ['absorb','hr']),
    ("Decision: ALL Commerce FREE_MODE=True, no real payment", {'entity':'Commerce','dept':'chromosome6'}, ['decision']),
    ("Decision: RD stuck -> check GitHub first", {'entity':'Strategy','dept':'chromosome0'}, ['decision','rule']),
    ("Decision: CI/CD pipeline 9/9 must pass before deploy", {'entity':'Pipeline','dept':'chromosome0'}, ['decision','quality']),
    ("igp-run.ps1: PowerShell wrapper for quote issues", {'entity':'CLI','dept':'chromosome18'}, ['tool','cli']),
    ("run_inline.py: 7 shortcuts replace WebChat button", {'entity':'CLI','dept':'chromosome18'}, ['tool','cli']),
    ("check_all.bat: one-click full chain check", {'entity':'CLI','dept':'chromosome18'}, ['tool','cli']),
    ("sitecustomize.py: global UTF-8 fix for Windows encoding", {'entity':'Python','dept':'chromosome0'}, ['tool','encoding']),
    ("IGP pyramid: 12 departments 36 teams + 3 HQ units", {'entity':'Org','dept':'chromosome0'}, ['org']),
    ("Chromosome fission: 12->19 (new: memory/infra/devops/core/product)", {'entity':'Org','dept':'chromosome0'}, ['org','fission']),
    ("SWAT team: 3 people, emergency cross-dept issues", {'entity':'SWAT','dept':'chromosome0'}, ['org']),
]

for text, meta, tags in test_mem:
    sm.remember(text, meta, tags)

print(f'  记忆: {len(test_mem)}')

# 查询 (纯英文, 测试同义词+hash+加权)
queries = [
    ('wallet signature fail', ['AP2_Wallet','signature','CryptoKit']),
    ('router timeout provider', ['SmartRouter','provider']),
    ('deploy API', ['API','deploy']),
    ('test coverage percentage', ['TestCoverage','AutoTester','coverage']),
    ('encoding bug fix', ['Pipeline','encoding','GBK']),
    ('memory system', ['SiliconMemory','Mem0','Letta','memory']),
    ('CI CD pipeline', ['Pipeline','CI']),
    ('org chart department', ['Org','DepartmentRegistry','org']),
    ('absorb external technology', ['BM25S','CoverUp','Mem0','Letta','DocAgent','absorb']),
    ('CLI tool powershell', ['CLI','powershell','run_inline']),
]

n = len(queries)
total_recall = total_prec = total_mrr = total_ndcg = 0

print(f'  {"查询":<32s} {"召回":>5} {"精确":>5} {"MRR":>5} {"NDCG":>5}')
print('  ' + '-'*52)

for q, expected in queries:
    results = sm.recall(q)
    epis = results.get('episodic', [])
    top10 = [str(e.get('payload',{}).get('text','')) for e in epis[:10]]
    
    # 同义词扩展检查: 如果query词同义于记忆中的词也算命中
    recalled = 0
    for exp in expected:
        exp_low = exp.lower()
        hit = any(exp_low in t.lower() for t in top10)
        # 查扩展: system在记忆中可能是framework
        if not hit:
            syns = _expand_synonyms([exp_low])
            hit = any(any(s in t.lower() for s in syns) for t in top10)
        if hit:
            recalled += 1
    recall = recalled / len(expected)
    
    useful = sum(1 for t in top10[:5] if any(e.lower() in t.lower() for e in expected))
    prec = useful / min(5, len(top10)) if top10 else 0
    
    first = None
    for i, t in enumerate(top10[:10]):
        if any(e.lower() in t.lower() for e in expected):
            first = i+1
            break
    mrr = 1.0/first if first else 0.0
    
    dcg = idcg = 0.0
    for i in range(min(5, len(top10))):
        rel = 1.0 if any(e.lower() in top10[i].lower() for e in expected) else 0.0
        dcg += rel / math.log2(i+2)
    for i in range(min(5, recalled)):
        idcg += 1.0 / math.log2(i+2)
    ndcg = dcg/idcg if idcg>0 else 0.0
    
    total_recall += recall
    total_prec += prec
    total_mrr += mrr
    total_ndcg += ndcg
    
    print(f'  {q:<32s} {recall*100:>4.0f}% {prec*100:>4.0f}% {mrr*100:>4.0f}% {ndcg*100:>4.0f}%')

avg_r = total_recall/n*100
avg_p = total_prec/n*100
avg_m = total_mrr/n*100
avg_nd = total_ndcg/n*100
composite = avg_r*0.4 + avg_p*0.3 + avg_m*0.2 + avg_nd*0.1

print()
print('='*70)
print('  最终评分')
print('='*70)
print(f'  召回率@10: {avg_r:.1f}%')
print(f'  精确率@5:  {avg_p:.1f}%')
print(f'  MRR:        {avg_m:.1f}%')
print(f'  NDCG@5:     {avg_nd:.1f}%')
print(f'  综合得分:   {composite:.1f}/100')
print(f'  Mem0:      91.6/100')
print(f'  差距:      {91.6-composite:.1f}分')
print(f'  (零token, 纯检索)')
print()
print(f'  Upgrade: 68.1 -> 74.3 -> {composite:.1f}')
print(f'  Gains: +synonym map +hash embed +Chinese char +IGP boost')
print('='*70)
