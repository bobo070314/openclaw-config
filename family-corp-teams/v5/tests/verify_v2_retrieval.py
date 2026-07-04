"""硅胶体记忆 v2 真实检索验证"""
import sys, json, datetime

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
sys.path.insert(0, V5)
sys.path.insert(0, V5 + r'\v6\silicon_memory')

from v5_silicon_memory import SiliconMemory

sm = SiliconMemory()

print('=' * 60)
print('  硅胶体记忆 v2 — 检索质量验证')
print('=' * 60)

# 写入测试数据（模拟各部门的真实场景）
test_memories = [
    ('chromosome6: AP2_Wallet签名超时，验证公钥失败', {'entity': 'AP2_Wallet', 'dept': 'chromosome8'}, ['bug', 'crypto', 'signature']),
    ('chromosome9: BugDoctor扫描66个文件发现50处可改进', {'entity': 'BugDoctor', 'dept': 'chromosome9'}, ['scan', 'success']),
    ('chromosome13: 硅胶体记忆v1部署完成，4类20函数259行', {'entity': 'SiliconMemory', 'dept': 'chromosome13'}, ['memory', 'deploy']),
    ('chromosome4: SmartRouter PK对比3个provider', {'entity': 'SmartRouter', 'dept': 'chromosome4'}, ['router', 'pk']),
    ('chromosome5: Guardian检测到ap2协议异常，跨部门通知chromosome8', {'entity': 'Guardian', 'dept': 'chromosome5'}, ['security', 'alert']),
    ('chromosome8: CryptoKit签名验证器重构，性能提升3倍', {'entity': 'CryptoKit', 'dept': 'chromosome8'}, ['crypto', 'optimization']),
    ('chromosome7: AgentOS Shell增加多Agent协作模式', {'entity': 'AgentOS', 'dept': 'chromosome7'}, ['agent', 'orchestration']),
    ('chromosome10: SymbolicEngine解析成功，证明验证通过', {'entity': 'SymbolicEngine', 'dept': 'chromosome10'}, ['proof', 'logic']),
    ('chromosome12: AutoTester全量测试通过，覆盖93%', {'entity': 'AutoTester', 'dept': 'chromosome12'}, ['test', 'coverage']),
    ('chromosome18: CI/CD pipeline 9/9全部通过，可直接部署', {'entity': 'Pipeline', 'dept': 'chromosome18'}, ['ci', 'cd', 'deploy']),
]

for text, meta, tags in test_memories:
    sm.remember(text=text, metadata=meta, tags=tags)

print(f'\n 写入: {len(test_memories)}条测试记忆')
print()

# 测试检索
queries = [
    ('wallet', '查找wallet相关'),
    ('bug scan', '查找bug扫描'),
    ('signature', '签名验证'),
    ('crypto', '加密/签名'),
    ('Pipeline deploy', 'CI/CD部署'),
    ('agent', 'Agent/协作'),
]

print(f'  {"查询":<25} {"#结果":>5} {"最佳匹配摘要":>40}')
print('  ' + '-' * 70)

for q, desc in queries:
    results = sm.recall(q)
    epis = results.get('episodic', [])
    n = len(epis)
    best = epis[0][1][:50] if epis else '(无匹配)'
    print(f'  {q:<25} {n:>5} {best:>40}')

print()
print(' 检索评分 (LoCoMo风格):')
print('  精确匹配: 验证wallet提取到AP2_Wallet ->', 'PASS' if any('wallet' in str(r) for r in sm.recall('wallet').get('episodic',[])) else 'FAIL')
print('  实体关联: 验证chromosome8能查到 ->', 'PASS' if any('chromosome8' in str(r) for r in sm.recall('chromosome8').get('episodic',[])) else 'FAIL')
print('  多信号: 验证"sign"查到signature + sign ->', 'PASS' if any('sign' in str(r) for r in sm.recall('sign').get('episodic',[])) else 'FAIL')
print()
print('=' * 60)
print('  硅胶体记忆 v2 检索完毕')
print('=' * 60)
