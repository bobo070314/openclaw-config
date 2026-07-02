"""
IGP 研发部 V6 — 产品注册表
自动扫描 v5/ 目录下所有 .py 文件，提取产品信息，生成注册表 + 版本号
"""
from __future__ import annotations
import ast
import json
import os
import re
import warnings
from typing import Any, Dict, List
from datetime import datetime, timezone


# 压制所有 SyntaxWarning — 扫描其他文件时外部文件的raw string问题不影响结果
warnings.filterwarnings('ignore', category=SyntaxWarning)


# 版本号生成：基于文件hash + 修改时间
def make_version(filepath: str) -> str:
    """生成语义化版本号 — 基于文件内容hash"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            src = f.read()
        h = str(hash(src) & 0xFFFFFF)[-4:]
        return f"1.0.0-alpha.{h}"
    except Exception:
        return "0.0.0-dev"


def extract_public_api(filepath: str) -> List[str]:
    """提取文件中的公共API签名"""
    sigs = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            src = f.read()
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                sigs.append(f"{node.name}(...)->Any")
            elif isinstance(node, ast.ClassDef) and not node.name.startswith('_'):
                sigs.append(f"class {node.name}")
    except Exception:
        pass
    return sigs


def get_doc_first_line(filepath: str) -> str:
    """提取文件docstring第一行作为产品描述"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            src = f.read()
        tree = ast.parse(src)
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                return node.value.value.split('\n')[0].strip()
    except Exception:
        pass
    return ""


# 已知产品映射（手工标记，后续可自动化）
PRODUCT_CATALOG = {
    # 染色体0: 基础架构
    "v5_fission_engine": {"name": "FissionEngine", "chromosome": 0, "stage": "beta", "type": "engine"},
    "v5_mutation_fission": {"name": "MutationFission", "chromosome": 0, "stage": "alpha", "type": "engine"},
    "v5_mutation_fission_live": {"name": "MutationFissionLive", "chromosome": 0, "stage": "alpha", "type": "engine"},
    "v5_code_analyzer": {"name": "CodeAnalyzer", "chromosome": 0, "stage": "alpha", "type": "analyzer"},
    
    # 染色体1: MCP
    "igp_mcp_v5_server": {"name": "MCPServer", "chromosome": 1, "stage": "beta", "type": "protocol"},
    "igp_mcp_v5_client": {"name": "MCPClient", "chromosome": 1, "stage": "beta", "type": "protocol"},
    "mcp_v2_upgrade": {"name": "MCPv2Upgrade", "chromosome": 1, "stage": "beta", "type": "upgrade"},
    "fastmcp_export": {"name": "FastMCPExport", "chromosome": 1, "stage": "beta", "type": "protocol"},
    
    # 染色体2: A2A
    "a2a_v2_upgrade": {"name": "A2Av2", "chromosome": 2, "stage": "beta", "type": "protocol"},
    
    # 染色体3: 市场
    "v5_market_upgrade": {"name": "MarketUpgrade", "chromosome": 3, "stage": "alpha", "type": "market"},
    
    # 染色体4: 路由
    "provider_router": {"name": "ProviderRouter", "chromosome": 4, "stage": "alpha", "type": "router"},
    "provider_pk": {"name": "ProviderPK", "chromosome": 4, "stage": "alpha", "type": "router"},
    "v5_provider_upgrade": {"name": "ProviderUpgrade", "chromosome": 4, "stage": "alpha", "type": "upgrade"},
    "v5_provider_router_v2": {"name": "ProviderRouterV2", "chromosome": 4, "stage": "alpha", "type": "router"},
    "v5_smart_router": {"name": "SmartRouter", "chromosome": 4, "stage": "alpha", "type": "router"},
    "provider_abstraction": {"name": "ProviderAbstraction", "chromosome": 4, "stage": "alpha", "type": "router"},
    
    # 染色体5: 安全
    "guardian_act": {"name": "GuardianAct", "chromosome": 5, "stage": "alpha", "type": "security"},
    "guardian_plan": {"name": "GuardianPlan", "chromosome": 5, "stage": "alpha", "type": "security"},
    "guardian_policy": {"name": "GuardianPolicy", "chromosome": 5, "stage": "alpha", "type": "security"},
    
    # 染色体6: 商业
    "agent_commerce_v2": {"name": "CommerceV2", "chromosome": 6, "stage": "ga", "type": "commerce"},
    "commerce_pk_v2": {"name": "CommercePK", "chromosome": 6, "stage": "beta", "type": "commerce"},
    
    # 染色体7: AgentOS
    "agent_os_kernel": {"name": "AgentOSKernel", "chromosome": 7, "stage": "alpha", "type": "os"},
    "agent_os_scheduler": {"name": "AgentOSScheduler", "chromosome": 7, "stage": "alpha", "type": "os"},
    "agent_os_shell": {"name": "AgentOSShell", "chromosome": 7, "stage": "alpha", "type": "os"},
    "v5_agent_os_upgrade": {"name": "AgentOSUpgrade", "chromosome": 7, "stage": "alpha", "type": "upgrade"},
    
    # 染色体8: AP2
    "ap2_protocol": {"name": "AP2Protocol", "chromosome": 8, "stage": "alpha", "type": "protocol"},
    "ap2_wallet": {"name": "AP2Wallet", "chromosome": 8, "stage": "alpha", "type": "wallet"},
    "v5_ap2_upgrade": {"name": "AP2Upgrade", "chromosome": 8, "stage": "alpha", "type": "upgrade"},
    "v5_crypto_kit": {"name": "CryptoKit", "chromosome": 8, "stage": "beta", "type": "security"},
    
    # 染色体9: Bug修复
    "v5_bug_doctor": {"name": "BugDoctor", "chromosome": 9, "stage": "ga", "type": "analyzer"},
    "v5_incremental_scanner": {"name": "IncrementalScanner", "chromosome": 9, "stage": "alpha", "type": "analyzer"},
    
    # 染色体10: 逻辑推理
    "v5_symbolic_engine": {"name": "SymbolicEngine", "chromosome": 10, "stage": "beta", "type": "engine"},
    "v5_logic_upgrade": {"name": "LogicUpgrade", "chromosome": 10, "stage": "alpha", "type": "upgrade"},
    
    # 染色体11: 类型/度量
    "v5_complexity_analyzer": {"name": "ComplexityAnalyzer", "chromosome": 11, "stage": "beta", "type": "analyzer"},
    
    # 染色体12: 自动测试
    "v5_auto_tester": {"name": "AutoTester", "chromosome": 12, "stage": "beta", "type": "tester"},
    "v5_auto_tester_v2": {"name": "AutoTesterV2", "chromosome": 12, "stage": "alpha", "type": "tester"},
    "v5_result_monad": {"name": "ResultMonad", "chromosome": 12, "stage": "alpha", "type": "monad"},
    "v5_safe_runner": {"name": "SafeRunner", "chromosome": 12, "stage": "alpha", "type": "runner"},
    "v5_logger_context": {"name": "LoggerContext", "chromosome": 12, "stage": "alpha", "type": "logger"},
    
    # 工具类
    "v5_skills_registry": {"name": "SkillsRegistry", "chromosome": 0, "stage": "beta", "type": "tool"},
    "v5_dashboard": {"name": "Dashboard", "chromosome": 0, "stage": "beta", "type": "tool"},
    "v5_ghost_patrol": {"name": "GhostPatrol", "chromosome": 0, "stage": "beta", "type": "tool"},
    "v5_closed_loop_pipeline": {"name": "ClosedLoopPipeline", "chromosome": 0, "stage": "ga", "type": "pipeline"},
    "v5_engine_loop": {"name": "EngineLoop", "chromosome": 0, "stage": "beta", "type": "pipeline"},
    "v5_pk_arena": {"name": "PKArena", "chromosome": 0, "stage": "beta", "type": "arena"},
    "v5_final_all": {"name": "FinalAll", "chromosome": 0, "stage": "beta", "type": "verifier"},
    "v5_job_engine": {"name": "JobEngine", "chromosome": 13, "stage": "alpha", "type": "hr"},
    
    # 变异体
    "mutation_secure_result": {"name": "SecureResult", "chromosome": 14, "stage": "research", "type": "mutation"},
    "mutation_watchdog_runner": {"name": "WatchdogRunner", "chromosome": 14, "stage": "research", "type": "mutation"},
    "mutation_audit_router": {"name": "AuditRouter", "chromosome": 15, "stage": "research", "type": "mutation"},
}


def scan_v5_directory(base_dir: str) -> Dict[str, Any]:
    """扫描 v5/ 目录，构建完整产品注册表"""
    registry = {
        "registry_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_products": 0,
        "products": {},
    }
    
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if not f.endswith('.py') or f.startswith('__'):
                continue
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, base_dir)
            module_key = f.replace('.py', '')
            
            version = make_version(fp)
            api = extract_public_api(fp)
            doc = get_doc_first_line(fp)
            
            catalog = PRODUCT_CATALOG.get(module_key, {})
            
            product = {
                "file": rel,
                "version": version,
                "stage": catalog.get("stage", "research"),
                "type": catalog.get("type", "unknown"),
                "chromosome": catalog.get("chromosome", 0),
                "display_name": catalog.get("name", module_key),
                "description": doc or catalog.get("description", ""),
                "public_api_count": len(api),
                "public_apis": api[:10],
                "changelog": [f"{version}: Initial registration"],
                "dependents": [],
                "metrics": {"calls": 0, "avg_latency_ms": 0, "error_rate": 0},
            }
            registry["products"][module_key] = product
    
    registry["total_products"] = len(registry["products"])
    return registry


if __name__ == '__main__':
    import sys
    v5_dir = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
    registry = scan_v5_directory(v5_dir)
    
    out_path = os.path.join(v5_dir, 'v6', 'product_registry.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    
    print(f"产品注册表: {out_path}")
    print(f"总计: {registry['total_products']} 个产品")
    
    # 按stage统计
    stages = {}
    for p in registry['products'].values():
        s = p['stage']
        stages[s] = stages.get(s, 0) + 1
    print(f"生命周期分布: {stages}")
    
    # 按染色体统计
    chroms = {}
    for p in registry['products'].values():
        c = p['chromosome']
        chroms[c] = chroms.get(c, 0) + 1
    print(f"染色体分布: {dict(sorted(chroms.items()))}")
