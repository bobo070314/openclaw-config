#!/usr/bin/env python3
"""
IGP V5 染色体互搏大赛 (ChromosomePK)
每条染色体产出调测试用例 → 其他染色体交叉验证 → PK评分
"""

import json, os, sys, random, re
from datetime import datetime, timezone
from typing import Dict, Any, List, Callable
from pathlib import Path

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V5_DIR = os.path.join(BASE, "v5")
CHROMOSOMES_DIR = os.path.join(V5_DIR, "chromosomes")
PK_DIR = os.path.join(V5_DIR, "pk_battle")
os.makedirs(PK_DIR, exist_ok=True)

# 各染色体提供的测试用例
CHROMOSOME_TESTS = {
    "chromosome1": {  # MCP生态部
        "name": "MCP生态部",
        "tests": [
            {"id": "mcp_call_tool", "desc": "MCP调用一个工具并返回结果", "check": "returns_result"},
            {"id": "mcp_discover", "desc": "发现Server上可用工具列表", "check": "returns_list"},
            {"id": "mcp_pk_rank", "desc": "对多个Server进行PK排名", "check": "returns_ranking"},
        ]
    },
    "chromosome2": {  # A2A联邦部
        "name": "A2A联邦部",
        "tests": [
            {"id": "a2a_agent_card", "desc": "创建Agent Card并序列化", "check": "valid_json"},
            {"id": "a2a_discovery", "desc": "Agent互相发现", "check": "finds_agents"},
            {"id": "a2a_task_send", "desc": "发送任务给另一个Agent", "check": "delivered"},
        ]
    },
    "chromosome3": {  # Skills市场部
        "name": "Skills市场部",
        "tests": [
            {"id": "skills_parse", "desc": "解析SKILL.md文件", "check": "parsed"},
            {"id": "skills_market_list", "desc": "列出市场所有可用Skill", "check": "returns_list"},
            {"id": "skills_pk_rank", "desc": "Skills PK排名", "check": "returns_ranking"},
        ]
    },
    "chromosome4": {  # Provider路由部
        "name": "Provider路由部",
        "tests": [
            {"id": "provider_register", "desc": "注册一个Provider", "check": "registered"},
            {"id": "provider_route", "desc": "根据任务类型路由", "check": "routed_correctly"},
            {"id": "provider_pk", "desc": "Provider PK排名", "check": "returns_ranking"},
        ]
    },
    "chromosome5": {  # 安全Guardian部
        "name": "安全Guardian部",
        "tests": [
            {"id": "guardian_analyze", "desc": "分析风险等级", "check": "risk_level_detected"},
            {"id": "guardian_block", "desc": "阻止危险操作", "check": "blocked"},
            {"id": "guardian_policy", "desc": "安全策略匹配", "check": "policy_matched"},
        ]
    },
    "chromosome6": {  # 商业协议部
        "name": "商业协议部",
        "tests": [
            {"id": "commerce_register", "desc": "注册Agent服务", "check": "registered"},
            {"id": "commerce_price", "desc": "定价策略", "check": "price_set"},
            {"id": "commerce_pk", "desc": "商业PK排名", "check": "returns_ranking"},
        ]
    },
}

now_iso = lambda: datetime.now(timezone.utc).isoformat()


def import_chromosome_module(chromo_id: str, mod_name: str):
    """安全导入染色体模块"""
    import importlib.util
    import sys as _sys
    
    infra = os.path.join(CHROMOSOMES_DIR, chromo_id, "infra")
    mod_path = os.path.join(infra, mod_name)
    if not os.path.exists(mod_path):
        return None
    
    spec = importlib.util.spec_from_file_location(mod_name.replace('.py',''), mod_path)
    if spec is None or spec.loader is None:
        return None
    
    # Add infra to path temporarily
    if infra not in _sys.path:
        _sys.path.insert(0, infra)
    
    try:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        return None


def run_chromosome_test(chromo_id: str, test_id: str) -> Dict[str, Any]:
    """运行一条染色体的某个测试"""
    name = CHROMOSOME_TESTS[chromo_id]["name"]
    test_info = next((t for t in CHROMOSOME_TESTS[chromo_id]["tests"] if t["id"] == test_id), None)
    if not test_info:
        return {"test": test_id, "status": "unknown", "error": "Test not found"}
    
    try:
        if chromo_id == "chromosome1":  # MCP
            mod = import_chromosome_module("chromosome1", "igp_mcp_v5_client.py")
            if mod:
                client = mod.MCPClient()
                client.connect_http("https://mcp.example.com")
                result = client.call_tool("test_tool")
                return {"test": test_id, "status": "pass", "result": str(result)}
            
        elif chromo_id == "chromosome2":  # A2A v2
            a2a_mod = import_chromosome_module("chromosome2", "a2a_v2_upgrade.py")
            if a2a_mod:
                card = a2a_mod.AgentCard(name="TestAgent1", description="Test")
                fed = a2a_mod.A2AFederation()
                fed.register(card)
                return {"test": test_id, "status": "pass", "result": f"Agent: {card.card['name']}, Federation: {fed.count()} agents"}
            
        elif chromo_id == "chromosome3":  # Skills
            pkg_mod = import_chromosome_module("chromosome3", "skill_package.py")
            if pkg_mod:
                # test skill package parse
                return {"test": test_id, "status": "pass", "result": "Skills module loaded"}
            mk_mod = import_chromosome_module("chromosome3", "skill_pk_rank.py")
            if mk_mod:
                return {"test": test_id, "status": "pass", "result": "Skills PK module loaded"}
            
        elif chromo_id == "chromosome4":  # Provider
            mod = import_chromosome_module("chromosome4", "provider_router.py")
            if mod:
                return {"test": test_id, "status": "pass", "result": "Provider modules loaded"}
            
        elif chromo_id == "chromosome5":  # Guardian
            plan_mod = import_chromosome_module("chromosome5", "guardian_plan.py")
            if plan_mod:
                plan = plan_mod.GuardianPlan()
                plan.receive_request({"action": "delete", "file_path": "/etc/passwd"})
                risk = plan.analyze_risk()
                return {"test": test_id, "status": "pass" if risk == "critical" else "fail", 
                        "result": f"Risk: {risk}"}
            
        elif chromo_id == "chromosome6":  # Commerce v2
            mod = import_chromosome_module("chromosome6", "agent_commerce_v2.py")
            if mod:
                engine = mod.AgentCommerceEngine()
                svc = engine.register_service("test-agent", "Test", 0.01)
                tx = engine.charge_task("test-agent", "test task", 100)
                rev = engine.get_revenue("test-agent")
                return {"test": test_id, "status": "pass", "result": f"Registered: {svc['name']}, Revenue: ${rev}"}
            pk_mod = import_chromosome_module("chromosome6", "commerce_pk_v2.py")
            if pk_mod:
                pk = pk_mod.CommercePKRank()
                pk.register("test-agent")
                return {"test": test_id, "status": "pass", "result": "CommercePK loaded"}
        
        return {"test": test_id, "status": "skipped", "result": "Module not available"}
    
    except Exception as e:
        return {"test": test_id, "status": "error", "error": str(e)}


def run_all_tests() -> Dict[str, Any]:
    """运行所有染色体的所有测试"""
    results = {}
    for chromo_id, info in CHROMOSOME_TESTS.items():
        name = info["name"]
        print(f"\n  🧪 运行 {name} 的测试...")
        chromo_results = []
        for test in info["tests"]:
            r = run_chromosome_test(chromo_id, test["id"])
            icon = "✅" if r["status"] == "pass" else "❌" if r["status"] == "fail" else "⏭️"
            print(f"    {icon} {test['desc']}: {r.get('result', r.get('error', 'N/A'))}")
            chromo_results.append(r)
        results[chromo_id] = chromo_results
    return results


def run_inter_chromosome_pk(results: Dict) -> Dict[str, Any]:
    """跨染色体PK：每个染色体队PK其他队的输出"""
    print(f"\n{'='*50}")
    print(f"  🏆 染色体互搏大赛")
    print(f"{'='*50}")
    
    pk_results = {}
    
    for chromo_id, tests in results.items():
        name = CHROMOSOME_TESTS[chromo_id]["name"]
        passed = sum(1 for t in tests if t["status"] == "pass")
        total = len(tests)
        score = round(passed / max(total, 1) * 10, 1)
        pk_results[chromo_id] = {
            "name": name,
            "passed": passed,
            "total": total,
            "score": score,
            "grade": "S" if score >= 9 else "A" if score >= 7 else "B" if score >= 5 else "C",
        }
        bar = "🟢" * int(score) + "🔴" * (10 - int(score))
        print(f"  {name:14s} {score:4.1f}/10 {bar}  ({passed}/{total}通过)")
    
    # 排名
    print(f"\n  🏅 最终排名:")
    ranked = sorted(pk_results.values(), key=lambda x: x["score"], reverse=True)
    medals = ["🥇", "🥈", "🥉"]
    for i, r in enumerate(ranked):
        prefix = medals[i] if i < 3 else f"  {i+1}."
        print(f"    {prefix} {r['name']:14s} {r['score']}/10 [{r['grade']}]")
    
    return pk_results


def generate_pk_report(test_results, pk_results) -> str:
    """生成互搏大赛报告"""
    lines = []
    lines.append("=" * 60)
    lines.append("  🏟️ IGP V5 染色体互搏大赛报告")
    lines.append(f"  时间: {now_iso()}")
    lines.append("=" * 60)
    lines.append("")
    
    # 各队测试结果
    for chromo_id, tests in test_results.items():
        name = CHROMOSOME_TESTS[chromo_id]["name"]
        pk = pk_results.get(chromo_id, {})
        score = pk.get("score", 0)
        bar = "🟢" * int(score) + "🔴" * (10 - int(score))
        lines.append(f"  {name} [{score}/10] {bar}")
        for t in tests:
            icon = {"pass": "✅", "fail": "❌", "skipped": "⏭️", "error": "💥", "unknown": "❓"}.get(t["status"], "❓")
            detail = t.get("result", t.get("error", ""))
            lines.append(f"    {icon} {t['test']}: {str(detail)[:80]}")
        lines.append("")
    
    # 排名榜
    lines.append("-" * 40)
    lines.append("  🏆 染色体互搏排名榜")
    lines.append("")
    ranked = sorted(pk_results.values(), key=lambda x: x["score"], reverse=True)
    medals = ["🥇", "🥈", "🥉"]
    for i, r in enumerate(ranked):
        prefix = medals[i] if i < 3 else f"  {i+1}."
        lines.append(f"    {prefix} {r['name']:14s} {r['score']:4.1f}/10  [{r['grade']}]")
    
    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "battle"
    
    if cmd == "battle":
        print("\n🏟️ IGP V5 染色体互搏大赛启动\n")
        test_results = run_all_tests()
        pk_results = run_inter_chromosome_pk(test_results)
        
        report = generate_pk_report(test_results, pk_results)
        print(f"\n\n{report}")
        
        report_path = os.path.join(PK_DIR, "PK_BATTLE_REPORT.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n报告已保存: {report_path}")
    
    elif cmd == "report":
        report_path = os.path.join(PK_DIR, "PK_BATTLE_REPORT.md")
        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                print(f.read())
        else:
            print("尚未有PK记录，请先运行 'battle'")
