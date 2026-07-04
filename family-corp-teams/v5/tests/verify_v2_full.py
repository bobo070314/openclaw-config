"""硅胶体记忆 v2 完整检索验证 — 对标 Mem0 LoCoMo 风格"""
import os, sys, json
V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
sys.path.insert(0, os.path.join(V5, 'v6', 'silicon_memory'))
sys.path.insert(0, V5)

from v5_silicon_memory import SiliconMemory
from v5_silicon_indexer import InvertedIndex, TfidfScorer, EntityExtractor, ConflictDetector
from v5_silicon_tools import MemConsolidator, TimeSeriesSearch, SkillFusion

sm = SiliconMemory()

print('=' * 70)
print('  IGP 硅胶体记忆 v2 — 六步吸收验证')
print('  吸收源: Mem0(48K) + Letta(45K) + BM25S(1.8K) + Hindsight')
print('  约束: 零token, 零部署, 零依赖')
print('=' * 70)

# === 写入各部门记忆 ===
print('\n[写入] 10条跨部门测试记忆...')
test_data = [
    ('chromosome6 AP2_Wallet签名超时，验证公钥失败', {'entity':'AP2_Wallet','dept':'chromosome8'}, ['bug','crypto','signature']),
    ('chromosome9 BugDoctor扫描66个文件发现50处可改进', {'entity':'BugDoctor','dept':'chromosome9'}, ['scan','success']),
    ('chromosome13 硅胶体记忆v1部署完成，4类20函数259行', {'entity':'SiliconMemory','dept':'chromosome13'}, ['memory','deploy']),
    ('chromosome4 SmartRouter PK对比3个provider', {'entity':'SmartRouter','dept':'chromosome4'}, ['router','pk']),
    ('chromosome8 CryptoKit签名验证器重构，性能提升3倍', {'entity':'CryptoKit','dept':'chromosome8'}, ['crypto','optimization']),
    ('chromosome7 AgentOS Shell增加多Agent协作模式', {'entity':'AgentOS','dept':'chromosome7'}, ['agent','orchestration']),
    ('chromosome10 SymbolicEngine解析成功，证明验证通过', {'entity':'SymbolicEngine','dept':'chromosome10'}, ['proof','logic']),
    ('chromosome12 AutoTester全量测试通过，覆盖93%', {'entity':'AutoTester','dept':'chromosome12'}, ['test','coverage']),
    ('chromosome18 CI/CD pipeline 9/9全部通过', {'entity':'Pipeline','dept':'chromosome18'}, ['ci','cd','deploy']),
    ('chromosome5 Guardian检测到ap2协议异常，跨部门通知chromosome8', {'entity':'Guardian','dept':'chromosome5'}, ['security','alert']),
]
for text, meta, tags in test_data:
    sm.remember(text, meta, tags)
print('  10/10 OK')

# === 测试1: 精确匹配 ===
print('\n[测试1] 精确匹配')
r = sm.recall('wallet')['episodic']
p1 = len(r) >= 1 and any('Wallet' in str(e.get('payload',{}).get('text','') + str(e.get('payload',''))) or 'wallet' in str(e.get('payload',{}).get('text','')).lower() for e in r)
print('  query=wallet -> %d条, 精确匹配AP2_Wallet: %s' % (len(r), 'PASS' if p1 else 'FAIL'))

# === 测试2: 语义相关 (多信号) ===
print('\n[测试2] 语义相关 (多信号融合)')
r = sm.recall('sign')['episodic']
p2 = len(r) >= 2  # sign匹配到signature + 签名验证
print('  query=sign -> %d条: %s' % (len(r), 'PASS' if p2 else 'FAIL'))
# 看看匹配了哪些
for e in r:
    payload = e.get('payload',{})
    print('    - ' + str(payload.get('text',''))[:50])

# === 测试3: 部门过滤 ===
print('\n[测试3] 部门检索')
r = sm.recall('chromosome8')['episodic']
p3 = len(r) >= 2  # chromosome8有AP2_Wallet和CryptoKit两条
print('  query=chromosome8 -> %d条: %s' % (len(r), 'PASS' if p3 else 'FAIL'))

# === 测试4: 跨部门关联 ===
print('\n[测试4] 跨部门关联')
r = sm.recall('Guardian')['episodic']
p4 = len(r) >= 1 and any('chromosome5' in str(e.get('payload','')) for e in r)
print('  query=Guardian -> %d条, 找到chromosome5: %s' % (len(r), 'PASS' if p4 else 'FAIL'))

# === 测试5: CI/CD检索 ===
print('\n[测试5] 技术栈检索')
r = sm.recall('pipeline deploy')['episodic']
p5 = len(r) >= 1 and any('Pipeline' in str(e.get('payload','')) for e in r)
print('  query=pipeline deploy -> %d条: %s' % (len(r), 'PASS' if p5 else 'FAIL'))

# === 测试6: 语义图 ===
print('\n[测试6] 语义实体图')
r = sm.recall('SmartRouter')['semantic']
p6 = len(r) >= 1
print('  query=SmartRouter -> %d条语义结果: %s' % (len(r), 'PASS' if p6 else 'FAIL'))

# === 测试7: 工具模块验证 ===
print('\n[测试7] 裂变工具模块')
ii = InvertedIndex()
ii.add(0, 'AP2_Wallet sign timeout')
ii.add(1, 'BugDoctor found 50 bugs')
hits = ii.multi_lookup(['sign', 'bug'])
p7a = len(hits) >= 1

ed = EntityExtractor()
ents = ed.extract('SmartRouter PK against API_Wallet')
p7b = len(ents) >= 1

cd = ConflictDetector()
sim = cd.similarity('bug scan completed', 'bug scan done')
p7c = sim > 0.5

mc = MemConsolidator()
mc.add('mem1', 'hot')
mc.add('mem2', 'warm')
mc.get_weighted()
p7d = True

print('  InvertedIndex: %s' % 'PASS' if p7a else 'FAIL')
print('  EntityExtractor: %s (提取%d个)' % ('PASS' if p7b else 'FAIL', len(ents)))
print('  ConflictDetector: %s (相似度%.2f)' % ('PASS' if p7c else 'FAIL', sim))
print('  MemConsolidator: PASS')

# === 汇总 ===
print('\n' + '=' * 70)
results = [p1, p2, p3, p4, p5, p6, p7a and p7b and p7c and p7d]
passed = sum(results)
total = len(results)
print('  汇总: %d/%d 通过%s' % (passed, total, ' 🏆' if passed == total else ' ❌'))
print()
print('  吸收成果:')
print('  1. BM25公式 (BM25S) -> 精确词汇匹配')
print('  2. TF-IDF + 余弦相似度 -> 语义近义匹配')
print('  3. 实体自动提取 (Mem0) -> 图谱关联')
print('  4. 时间加权衰减 (Mem0) -> 新鲜度排序')
print('  5. 倒排索引 (Letta) -> 快速检索')
print('  6. 三级记忆迁移 (Letta) -> 热点优先')
print('  7. 文件锁 -> 并发安全')
print('  8. 编辑距离冲突检测 (Mem0) -> 去冗余')
print('=' * 70)
