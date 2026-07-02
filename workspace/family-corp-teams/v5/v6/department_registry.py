"""IGP 部门注册 v3 — 染色体/部门/文件映射登记表"""
import os

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'

# 完整部门注册表
REGISTRY = {
    # === 原有 15 个染色体部门 ===
    'chromosome1': {
        'name': 'MCP协议部',
        'dir': 'chromosomes/chromosome1/infra',
        'files': ['igp_mcp_pk.py', 'mcp_v2_upgrade.py', 'fastmcp_export.py', 'igp_mcp_v5_server.py', 'igp_mcp_v5_client.py'],
        'tests': ['test_mcp_v2_upgrade_mcphandler.py']
    },
    'chromosome2': {
        'name': 'A2A协议部',
        'dir': 'chromosomes/chromosome2/infra',
        'files': ['a2a_v2_upgrade.py'],
        'tests': []
    },
    'chromosome3': {
        'name': '市场扩展部',
        'dir': 'chromosomes/chromosome3/infra',
        'files': ['v5_market_upgrade.py', 'skill_pk.py'],
        'tests': []
    },
    'chromosome4': {
        'name': 'Provider路由器',
        'dir': 'chromosomes/chromosome4/infra',
        'files': ['provider_abstraction.py', 'provider_pk.py', 'provider_router.py', 'v5_provider_router_v2.py', 'v5_provider_upgrade.py', 'v5_smart_router.py'],
        'tests': ['test_smart_router.py', 'test_v5_provider_upgrade_provider.py', 'test_v5_smart_router_router.py', 'test_v5_smart_router_smartrouter.py']
    },
    'chromosome5': {
        'name': '治理/政策部',
        'dir': 'chromosomes/chromosome5/infra',
        'files': ['guardian_act.py', 'guardian_plan.py', 'guardian_policy.py', 'skill_pk.py', 'test_manual.py'],
        'tests': ['test_guardian_policy.py', 'test_guardian_act_guardianact.py']
    },
    'chromosome6': {
        'name': '商业部',
        'dir': 'chromosomes/chromosome6/infra',
        'files': ['agent_commerce_v2.py', 'commerce_pk_v2.py'],
        'tests': ['test_agent_commerce.py']
    },
    'chromosome7': {
        'name': 'Agent OS部',
        'dir': 'chromosomes/chromosome7/infra',
        'files': ['agent_os_kernel.py', 'agent_os_scheduler.py', 'agent_os_shell.py', 'v5_agent_os_upgrade.py'],
        'tests': ['test_v5_agent_os_upgrade_agentos.py']
    },
    'chromosome8': {
        'name': 'AP2协议部',
        'dir': 'chromosomes/chromosome8/infra',
        'files': ['ap2_protocol.py', 'ap2_wallet.py', 'v5_ap2_upgrade.py', 'v5_crypto_kit.py'],
        'tests': ['test_v5_ap2_upgrade_dualwallet.py', 'test_v5_ap2_upgrade_paymentwallet.py', 'test_v5_crypto_kit_cryptokit.py', 'test_v5_crypto_kit_keymanager.py', 'test_v5_crypto_kit_signatureverifier.py']
    },
    'chromosome9': {
        'name': 'Bug检查部',
        'dir': 'chromosomes/chromosome9/infra',
        'files': ['v5_bug_doctor.py', 'v5_incremental_scanner.py'],
        'tests': ['test_bug_doctor.py', 'test_incremental_scanner.py']
    },
    'chromosome10': {
        'name': '逻辑推理部',
        'dir': 'chromosomes/chromosome10/infra',
        'files': ['v5_symbolic_engine.py', 'v5_logic_upgrade.py'],
        'tests': ['test_symbolic_engine.py', 'test_v5_logic_upgrade_knowledgebase.py', 'test_v5_logic_upgrade_symbolicenginev2.py']
    },
    'chromosome11': {
        'name': '类型/度量部',
        'dir': 'chromosomes/chromosome11/infra',
        'files': ['v5_complexity_analyzer.py'],
        'tests': ['test_complexity_analyzer.py']
    },
    'chromosome12': {
        'name': '自动测试部',
        'dir': 'chromosomes/chromosome12/infra',
        'files': ['v5_auto_tester.py', 'v5_auto_tester_v2.py', 'v5_result_monad.py', 'v5_safe_runner.py', 'v5_logger_context.py'],
        'tests': ['test_v5_auto_tester_v2_autotester.py', 'test_v5_auto_tester_v2_testsuite.py', 'test_v5_auto_tester_v2_testresult.py',
                  'test_v5_result_monad_ok.py', 'test_v5_safe_runner_saferunner.py', 'test_v5_logger_context_loggercontext.py']
    },
    'chromosome0': {
        'name': '变异裂变中心',
        'dir': 'chromosomes/chromosome0/infra',
        'files': ['v5_mutation_fission.py', 'v5_code_analyzer.py'],
        'tests': ['test_v5_mutation_fission_autofixscanner.py', 'test_v5_mutation_fission_fissionengine.py', 'test_v5_mutation_fission_mutationengine.py']
    },
    'chromosome14_smart_routing': {
        'name': '智能路由部',
        'dir': 'chromosomes/chromosome14_smart_routing/infra',
        'files': [],
        'tests': []
    },
    'chromosome15_audit_security': {
        'name': '审计安全部',
        'dir': 'chromosomes/chromosome15_audit_security/infra',
        'files': [],
        'tests': []
    },
    
    # === 新部门 ===
    'chromosome13_silicon_memory': {
        'name': '硅胶体记忆部',
        'dir': 'v6/silicon_memory',
        'files': ['v5_silicon_memory.py'],
        'tests': ['test_v5_silicon_memory.py']
    },
    'chromosome16_infrastructure': {
        'name': 'IGP基础设施部',
        'dir': 'v6/api + v6/cli',
        'files': ['igp_api.py', 'igp_api_client.py', 'api_runner.py', 'igp_heartbeat.py', 'start_api.bg.py', 'igp_cli.py'],
        'tests': []
    },
    'chromosome17_devops': {
        'name': 'DevOps部',
        'dir': 'v6/ci',
        'files': ['pipeline.py', 'deploy.py', 'ci_pre_push.py', 'setup_hooks.py'],
        'tests': []
    },
    'chromosome18_core_engine': {
        'name': '核心引擎部',
        'dir': 'v5 顶层',
        'files': ['v5_dashboard.py', 'v5_engine_loop.py', 'v5_fission_engine.py', 'v5_ghost_patrol.py',
                  'v5_pk_battle.py', 'v5_pk_arena.py', 'v5_closed_loop_pipeline.py', 'v5_defect_audit.py'],
        'tests': []
    },
    'chromosome19_product_delivery': {
        'name': '产品交付部',
        'dir': 'v6/prd + v6/review + v6/lifecycle + v6/metrics',
        'files': ['prd_queue.py', 'v6_review_agents.py', 'v6_lifecycle.py', 'metrics_collector.py', 'metrics_reporter.py'],
        'tests': ['test_lifecycle.py', 'test_prd_queue.py', 'test_v6_review_agents_architect.py', 'test_v6_review_agents_compat.py', 'test_v6_review_agents_security.py']
    },
}

# 参谋部
HQ_FILES = {
    'SWAT突击队': ['swat_team.py'],
    '审计部': ['chromosome15_audit_security/infra'],
    '战略投资部': ['v5_github_scanner.py'],
}

print("=" * 70)
print("  IGP 部门注册表 v3")
print("=" * 70)
print()

total_code = 0
total_tests = 0

for chrom in sorted(REGISTRY.keys()):
    dept = REGISTRY[chrom]
    code_n = len(dept['files'])
    test_n = len(dept['tests'])
    total_code += code_n
    total_tests += test_n
    print(f"  {chrom:<30} | {dept['name']:<16} | {code_n:>2}文件 {test_n:>2}测试")
    # 列出测试归属
    if test_n > 0:
        for t in dept['tests']:
            print(f"    ├─ {t}")

print()
print(f"  合计: {len(REGISTRY)} 部门 | {total_code} 源文件 | {total_tests} 测试文件")
print()
print("  参谋部:")
for hq, files in HQ_FILES.items():
    print(f"    {hq}: {', '.join(files)}")
print()
print("=" * 70)
print("  硅胶体记忆 → chromosome13_silicon_memory  ✅ 已注册")
print("  API/CLI/SDK → chromosome16_infrastructure ✅ 已注册")
print("  CI/CD       → chromosome17_devops          ✅ 已注册")
print("  核心引擎    → chromosome18_core_engine      ✅ 已注册")
print("  产品交付    → chromosome19_product_delivery ✅ 已注册")
print("=" * 70)
