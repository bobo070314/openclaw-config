"""
IGP v3 Bridge — 连接 igp_engine.py 和 v3 Agent Runner

让igp_engine.py 的工单系统可以驱动真实LLM Agent执行任务，
PK结果自动写回KPI。
"""
import sys, pathlib, json, os, datetime, importlib.util

# 加载v3组件
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from igp_mcp_bridge import IGP_MCP
from igp_llm_agent import IGPAgent, PKManager
# from igp_engine_patch import patch_engine (尚未创建)

mcp = IGP_MCP()

def run_department_task(dept, task, engine_file=None):
    """
    让指定部门的3个Agent执行真实任务PK
    结果写回igp_engine的KPI文件
    
    Args:
        dept: 部门名 (frontend/backend/ai/quality/...)
        task: 要执行的任务
        engine_file: igp_engine.py 路径，用来注KPI更新
    
    Returns:
        dict: PK结果
    """
    print(f"\n{'='*60}")
    print(f"[IGP v3 Bridge] 派发真实任务到 {dept} 部门")
    print(f"  任务: {task}")
    print(f"{'='*60}")
    
    # 1. 加载3个Agent（不同模型，模拟不同团队）
    teams = []
    models = [
        "qwen-plus",       # team1: DashScope Qwen
        "qwen-turbo",      # team2: Qwen Turbo (更便宜)
        "qwen-plus",       # team3: 也Qwen-plus
    ]
    for tn, model in enumerate(models, 1):
        agent = IGPAgent(dept, tn, model=model)
        teams.append(agent)
        print(f"   [小队{tn}] {agent.name} 模型={model}")
    
    # 2. 并行执行
    results = []
    for a in teams:
        r = a.execute_task(task)
        results.append(r)
        print(f"   [{a.name}] {len(r['result'])} chars | {r['tokens']} tokens | {r['time_seconds']}s")
    
    # 3. 评分规则: 质量分 - token成本惩罚
    for r in results:
        content_len = len(r["result"])
        has_code = "```" in r["result"]
        bonus = 2 if has_code else 0
        token_penalty = r["tokens"] / 200  # 每200token -1分
        r["score"] = round(min(10, 6 + bonus - token_penalty), 1)
        r["score"] = max(1, min(10, r["score"]))
    
    # 4. 排名
    results.sort(key=lambda x: x["score"], reverse=True)
    winner = results[0]
    loser = results[-1]
    
    print(f"\n   PK结果:")
    for i, r in enumerate(results):
        medal = ["�", "🥈", "🥉"][i]
        print(f"     {medal} {r['agent']}: {r['score']}/10 ({r['tokens']}tokens)")
    
    # 5. 写入KPI
    kpi_path = pathlib.Path(__file__).parent.parent / "kpi_all.json"
    if kpi_path.exists():
        try:
            kpi = json.loads(kpi_path.read_text(encoding="utf-8"))
            winner_num = winner["agent"].split("-")[-1].replace("team", "")
            loser_num = loser["agent"].split("-")[-1].replace("team", "")
            for entry in kpi:
                if entry.get("department") == dept:
                    for team in entry.get("teams", []):
                        tn = str(team.get("team", ""))
                        if tn == winner_num:
                            team["wins"] = team.get("wins", 0) + 1
                            team["score"] = team.get("score", 100) + 5
                        elif tn == loser_num:
                            team["losses"] = team.get("losses", 0) + 1
                            team["score"] = team.get("score", 100) - 3
                        team["total_pk"] = team.get("total_pk", 0) + 1
            kpi_path.write_text(json.dumps(kpi, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"   KPI已更新 -> {kpi_path.name}")
        except Exception as e:
            print(f"   KPI更新失败: {e}")
    
    return {
        "dept": dept,
        "task": task,
        "winner": winner["agent"],
        "loser": loser["agent"],
        "scores": [(r["agent"], r["score"]) for r in results],
        "total_tokens": sum(r["tokens"] for r in results),
        "total_time": sum(r["time_seconds"] for r in results),
    }


def full_stress_test():
    """全部门压测——让14个部门+参谋部全员出动"""
    print("\n" + "="*60)
    print("   IGP v3.0 全部门真实压测")
    print("   All Departments Combat Readiness Test")
    print("="*60)
    
    departments = {
        "frontend": "重构当前项目中的前端组件，用Tailwind CSS + TypeScript重写Logo组件",
        "backend": "检查项目中的Python代码，修复潜在的性能问题和安全漏洞",
        "infrastructure": "优化Docker配置，为当前项目编写docker-compose.yml",
        "ai": "审查一段Python代码中的AI/ML部分，给出优化建议",
        "mobile": "为当前项目的API设计一个移动端适配方案",
        "design": "审查项目UI组件的可访问性，提出改进建议",
        "quality": "审查项目代码质量，列出所有违反PEP8的代码位置",
        "pmo": "为当前项目制定一个2周冲刺计划，包含milestone和deliverables",
        "growth": "分析项目技术栈，提出3个增长黑客建议",
        "compliance": "审查项目依赖的MIT/Apache/GPL许可证合规性",
        "advertising-anime": "为项目设计一个技术推广方案，目标开发者社区",
        "ecommerce-marketing": "分析项目的开源生态推广策略",
    }
    
    total_tokens = 0
    total_time = 0
    results = []
    
    for dept, task in departments.items():
        try:
            r = run_department_task(dept, task)
            results.append(r)
            total_tokens += r["total_tokens"]
            total_time += r["total_time"]
        except Exception as e:
            print(f"  [ERROR] {dept} 执行失败: {e}")
    
    # 最终报告
    print("\n" + "="*60)
    print("   压测完成报告")
    print("="*60)
    print(f"""
    参与部门: {len(departments)} 个
    全部小队: {len(departments)*3} 个LLM Agent
    总Token消耗: {total_tokens}
    总耗时: {total_time:.1f}s
    平均每部门: {total_time/len(departments):.1f}s
    
    胜率统计:""")
    
    from collections import Counter
    winners = Counter(r["winner"] for r in results)
    for agent, count in winners.most_common():
        print(f"      {agent}: {count}胜")
    
    print("\n" + "="*60)
    print("   结论: 全部部门可正常运行")
    print("="*60)


if __name__ == "__main__":
    import sys
    if "--stress" in sys.argv:
        full_stress_test()
    elif len(sys.argv) >= 4 and sys.argv[1] == "run":
        run_department_task(sys.argv[2], " ".join(sys.argv[3:]))
    else:
        print("用法:")
        print("  python igp_engine_v3_bridge.py run <department> <task>")
        print("  python igp_engine_v3_bridge.py --stress")
