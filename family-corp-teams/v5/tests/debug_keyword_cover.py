"""分析记忆-查询关键词覆盖情况"""
import sys, re
sys.path.insert(0, r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\silicon_memory')

# 32条记忆
mem = [
    'AP2_Wallet signature verification failed',
    'SmartRouter route to provider-B returned 503 timeout',
    'AgentOS Shell run command EOFError',
    'CI/CD pipeline step 5 fail subprocess encoding GBK',
    'PRD queue deadlock index collision on concurrent submit',
    'LifecycleManager expired product cleanup failed NoneType error',
    'AP2_Wallet uses CryptoKit SignatureVerifier',
    'SmartRouter fallback provider-A timeout downgrade',
    'AgentOS Shell fixed with Popen text=False',
    'Pipeline fixed with env encoding utf-8 GBK',
    'SiliconMemory v1 deployed 4 classes 20 funcs',
    'MCPv2 protocol upgrade complete FastMCP A2A federation',
    'HTTP API online 22 routes heartbeat auto-recovery',
    'Department registry v3 chromosomes expanded to 19',
    'CryptoKit signature speed 2.1s 0.8s improvement',
    'Test coverage 36% 93% 99 106 classes',
    'AutoTester 148 tests 140 pass removed 8 140 140 all pass',
    'BM25S absorbed BM25 formula pure Python',
    'CoverUp absorbed FSE 2025 paper AST scan safe tests',
    'Mem0 absorbed 4-signal retrieval design BM25 TF-IDF entity time',
    'Letta absorbed 3-tier memory migration hot warm cold',
    'DocAgent absorbed Meta ACL 2025 job description engine',
    'Decision ALL Commerce FREE_MODE True no real payment',
    'Decision RD stuck check GitHub first',
    'Decision CI CD pipeline 9/9 must pass before deploy',
    'igp-run.ps1 PowerShell wrapper for quote issues',
    'run_inline.py 7 shortcuts replace WebChat button',
    'check_all.bat one-click full chain check',
    'sitecustomize.py global UTF-8 fix for Windows encoding',
    'IGP pyramid 12 departments 36 teams 3 HQ units',
    'Chromosome fission 12 to 19 new memory infra devops core product',
    'SWAT team 3 people emergency cross-dept issues',
]

queries = {
    'wallet signature fail': ['wallet','sig','fail'],
    'router timeout provider': ['router','timeout','provider'],
    'deploy API': ['deploy','api'],
    'test coverage percentage': ['test','coverage'],
    'encoding bug fix': ['encoding','fix'],
    'memory system': ['memory','system'],
    'CI CD pipeline': ['ci','cd','pipeline'],
    'org chart department': ['org','chart','department'],
    'absorb external technology': ['absorb','external','technology'],
    'CLI tool powershell': ['cli','powershell'],
}

for q, ks in queries.items():
    print(f'Query: {q}')
    for k in ks:
        matches = [m for m in mem if k.lower() in m.lower()]
        if not matches:
            print(f'  [MISS]  "{k}" -> 记忆里完全没有!')
        else:
            print(f'  [OK {len(matches):2d}x] "{k}" -> {[m[:35] for m in matches[:2]]}')
    print()
