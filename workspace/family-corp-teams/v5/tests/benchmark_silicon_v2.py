"""IGP 硅胶体记忆 v2 — LoCoMo风格Benchmark

对标 Mem0 LoCoMo: 91.6分 (全量LLM评估)
我们的评估: 零token方式，用召回率@k + MRR + NDCG
"""
import sys, os, math, json, time
sys.path.insert(0, r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\silicon_memory')
sys.path.insert(0, r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5')

from v5_silicon_memory import SiliconMemory

print('=' * 70)
print('  IGP 硅胶体记忆 v2 — 对标 Mem0 LoCoMo Benchmark')
print('  全零token评估 (纯检索指标)')
print('=' * 70)
print()

# ============================================================
# 构建测试集: 50条记忆 + 10个查询
# ============================================================
sm = SiliconMemory()

# 测试记忆 (模拟24小时各部门实际场景)
test_memories = [
    # Bug类
    ("AP2_Wallet验证签名失败: 'int' object has no attribute 'points'", {'entity':'AP2_Wallet','dept':'chromosome8'}, ['bug','signature']),
    ("SmartRouter路由到provider-B时返回503超时", {'entity':'SmartRouter','dept':'chromosome4'}, ['bug','router']),
    ("AgentOS Shell执行'run'命令时EOFError", {'entity':'AgentOS','dept':'chromosome7'}, ['bug','shell']),
    ("CI/CD pipeline第5步fail: subprocess encoding GBK", {'entity':'Pipeline','dept':'chromosome18'}, ['bug','ci']),
    ("PRD queue死锁: 并发提交时索引冲突", {'entity':'PRD','dept':'chromosome19'}, ['bug','concurrency']),
    ("LifecycleManager过期产品清理失败: NoneType error", {'entity':'Lifecycle','dept':'chromosome3'}, ['bug','lifecycle']),
    
    # 修复记录
    ("AP2_Wallet签名改用CryptoKit.SignatureVerifier, 超时Retry 3次", {'entity':'AP2_Wallet','dept':'chromosome8'}, ['fix','signature']),
    ("SmartRouter加fallback: provider-A超时自动降级到provider-C", {'entity':'SmartRouter','dept':'chromosome4'}, ['fix','router']),
    ("AgentOS Shell改用Popen(text=False)解决EOFError", {'entity':'AgentOS','dept':'chromosome7'}, ['fix','subprocess']),
    ("Pipeline加$env:PYTHONIOENCODING=utf-8解决GBK问题", {'entity':'Pipeline','dept':'chromosome18'}, ['fix','encoding']),
    
    # 部署记录
    ("硅胶体记忆v1部署: 4类20函数259行, 93%覆盖率", {'entity':'SiliconMemory','dept':'chromosome13'}, ['deploy']),
    ("MCPv2协议升级完成: FastMCP+A2A联合", {'entity':'MCP','dept':'chromosome1'}, ['deploy','protocol']),
    ("HTTP API上线: 22条路由, heartbeat自动保活", {'entity':'API','dept':'chromosome18'}, ['deploy','api']),
    ("部门注册表v3: 染色体扩展到19个", {'entity':'DepartmentRegistry','dept':'chromosome0'}, ['deploy','org']),
    
    # 性能数据
    ("CryptoKit签名速度: 原来2.1s -> 优化后0.8s (3倍提升)", {'entity':'CryptoKit','dept':'chromosome8'}, ['perf']),
    ("测试覆盖率: 从36% -> 93% (99/106类)", {'entity':'TestCoverage','dept':'chromosome12'}, ['perf','test']),
    ("AutoTester: 148测试140通过 -> 删8个 -> 140/140", {'entity':'AutoTester','dept':'chromosome12'}, ['perf','test']),
    
    # 外部技术
    ("吸收BM25S: BM25公式纯Python实现, 零依赖", {'entity':'BM25S','dept':'chromosome13'}, ['absorb','search']),
    ("吸收CoverUp: FSE 2025论文, AST扫描->安全测试", {'entity':'CoverUp','dept':'chromosome0'}, ['absorb','testing']),
    ("吸收Mem0: 四信号检索设计 (BM25+TF-IDF+实体+时间)", {'entity':'Mem0','dept':'chromosome13'}, ['absorb','memory']),
    ("吸收Letta: 三级记忆迁移 (hot/warm/cold)", {'entity':'Letta','dept':'chromosome13'}, ['absorb','memory']),
    ("吸收DocAgent: Meta ACL 2025, 岗位说明书引擎", {'entity':'DocAgent','dept':'chromosome0'}, ['absorb','hr']),
    
    # 决策记录
    ("决定: 所有Commerce锁定FREE_MODE=True, 禁止真实交易", {'entity':'Commerce','dept':'chromosome6'}, ['decision']),
    ("决定: 研发卡住先上GitHub找答案, 不自己编评分", {'entity':'Strategy','dept':'chromosome0'}, ['decision','rule']),
    ("决定: CI/CD pipeline 9/9全通过方可部署", {'entity':'Pipeline','dept':'chromosome0'}, ['decision','quality']),
    
    # 工具使用
    ("igp-run.ps1: PowerShell包装器根治引号问题", {'entity':'CLI','dept':'chromosome18'}, ['tool','cli']),
    ("run_inline.py: 7个快捷命令替代WebChat内联按钮", {'entity':'CLI','dept':'chromosome18'}, ['tool','cli']),
    ("check_all.bat: 一键全链路检测", {'entity':'CLI','dept':'chromosome18'}, ['tool','cli']),
    ("sitecustomize.py: 全局UTF-8修复Windows编码", {'entity':'Python','dept':'chromosome0'}, ['tool','encoding']),
    
    # 组织结构
    ("IGP金字塔: 12部门36团队+3参谋部", {'entity':'Org','dept':'chromosome0'}, ['org']),
    ("染色体分裂: 12->19 (新增硅胶记忆/基础设施/DevOps/核心/产品)", {'entity':'Org','dept':'chromosome0'}, ['org','fission']),
    ("SWAT突击队: 3人, 紧急事件跨部门处理", {'entity':'SWAT','dept':'chromosome0'}, ['org']),
]

for text, meta, tags in test_memories:
    sm.remember(text, meta, tags)

print(f'  测试集: {len(test_memories)}条记忆')
print()

# ============================================================
# 10个查询 + 人工标注的期望结果
# ============================================================
queries = [
    ('wallet signature fail', ['AP2_Wallet', 'signature', 'CryptoKit']),
    ('router timeout provider', ['SmartRouter', 'provider']),
    ('deploy API', ['API', 'deploy']),
    ('test coverage percentage', ['TestCoverage', 'AutoTester', 'coverage']),
    ('encoding bug fix', ['Pipeline', 'encoding', 'GBK']),
    ('memory system', ['SiliconMemory', 'Mem0', 'Letta', 'memory']),
    ('CI CD pipeline', ['Pipeline', 'CI']),
    ('org chart department', ['Org', 'DepartmentRegistry']),
    ('absorb external technology', ['BM25S', 'CoverUp', 'Mem0', 'Letta', 'DocAgent', 'absorb']),
    ('CLI tool powershell', ['CLI', 'powershell', 'run_inline']),
]

# ============================================================
# 评估
# ============================================================
total_recall = 0
total_precision = 0
total_mrr = 0
total_ndcg = 0
n = len(queries)

print(f'  {"查询":<28} {"召回":>5} {"精确":>5} {"MRR":>5} {"NDCG":>5}')
print('  ' + '-' * 50)

for q, expected in queries:
    results = sm.recall(q)
    epis = results.get('episodic', [])
    
    # 提取前10个结果
    top10_texts = []
    for e in epis[:10]:
        text = str(e.get('payload', {}).get('text', ''))
        top10_texts.append(text)
    
    # 召回率: 期望关键词在top10中出现的比例
    recalled = 0
    for exp in expected:
        found = False
        for txt in top10_texts:
            if exp.lower() in txt.lower():
                found = True
                break
        if found:
            recalled += 1
    recall = recalled / len(expected)
    
    # 精确率: top5中有用的比例
    useful = 0
    for txt in top10_texts[:5]:
        if any(e.lower() in txt.lower() for e in expected):
            useful += 1
    precision = useful / min(5, len(top10_texts)) if top10_texts else 0
    
    # MRR: 第一个相关结果的排位倒数
    first_rank = None
    for i, txt in enumerate(top10_texts[:10]):
        if any(e.lower() in txt.lower() for e in expected):
            first_rank = i + 1
            break
    mrr = 1.0 / first_rank if first_rank else 0.0
    
    # NDCG@5: 折损累积增益
    dcg = 0.0
    idcg = 0.0
    for i in range(min(5, len(top10_texts))):
        rel = 1.0 if any(e.lower() in top10_texts[i].lower() for e in expected) else 0.0
        dcg += rel / math.log2(i + 2)
    for i in range(min(5, recalled)):
        idcg += 1.0 / math.log2(i + 2)
    ndcg = dcg / idcg if idcg > 0 else 0.0
    
    total_recall += recall
    total_precision += precision
    total_mrr += mrr
    total_ndcg += ndcg
    
    print(f'  {q:<28} {recall*100:>4.0f}% {precision*100:>4.0f}% {mrr*100:>4.0f}% {ndcg*100:>4.0f}%')

# 综合
avg_recall = total_recall / n * 100
avg_precision = total_precision / n * 100
avg_mrr = total_mrr / n * 100
avg_ndcg = total_ndcg / n * 100

# LoCoMo风格综合分数: 召回率*0.4 + 精确率*0.3 + MRR*0.2 + NDCG*0.1
composite = avg_recall * 0.4 + avg_precision * 0.3 + avg_mrr * 0.2 + avg_ndcg * 0.1

print()
print('=' * 70)
print('  IGP 硅胶体记忆 v2 — 最终评分')
print('=' * 70)
print(f'  平均召回率@{10}: {avg_recall:.1f}%')
print(f'  平均精确率@{5}:  {avg_precision:.1f}%')
print(f'  平均MRR:        {avg_mrr:.1f}%')
print(f'  平均NDCG@5:     {avg_ndcg:.1f}%')
print()
print(f'  综合得分:        {composite:.1f}/100')
print()
print('  对比:')
print(f'    Mem0 LoCoMo       91.6 (全量LLM评估, 不同测试集)')
print(f'    IGP 硅胶体 v2     {composite:.1f} (纯检索, 零token)')
print(f'    差距:             {91.6 - composite:.1f}分')
print()
print('  差距分析:')
print('    1. Mem0用向量嵌入理解语义: 同义词/反义词/上下文')
print('    2. Mem0用LLM提取关键信息: 从长文本中定位核心')
print('    3. 我们是关键词子词匹配: 精度高但查全率受限')
print('    4. 硅胶体优势: 零token成本, Mem0每次检索~1.2K token')
print()
print('  升级路线:')
print('    80分以下: 当前关键词搜索 ✅')
print('    80-90:  加载简单hash嵌入（10行代码, 零依赖）')
print('    90+:     需要向量库（有外部依赖）')
print()
print(f'  硅胶体 v2 结论: 零token对标 LoCoMo {composite:.1f}/100, 够用级别')
print('=' * 70)
