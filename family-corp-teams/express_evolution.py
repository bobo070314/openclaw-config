"""
虚拟时间加速进化引擎
每个问题生命周期 = 10秒，而非3天
"""
import os
import json
import datetime
import time
from pathlib import Path

BASE_DIR = Path(r"D:\bobo\openclaw-foreign\workspace")
TEAMS_DIR = BASE_DIR / "family-corp-teams"

EVOLUTION_LOG = TEAMS_DIR / "evolution_log.json"
COST_LOG = TEAMS_DIR / "cost_log.json"
TICKET_COUNTER = TEAMS_DIR / "ticket_counter.json"

# ============================================================
# 虚拟时间加速器
# ============================================================
VIRTUAL_TIME_SCALE = {
    "discovery_to_dispatch": 3,     # 发现问题→派发完成: 3秒
    "dispatch_to_solution": 3,      # 派发→3队出齐方案: 3秒  
    "review_to_conclusion": 2,      # 回溯→得出结论: 2秒
    "conclusion_to_stored": 2,      # 结论→入实践库: 2秒
}
TOTAL_CYCLE = sum(VIRTUAL_TIME_SCALE.values())  # 10秒

# ============================================================
# 1. 极速工单系统
# ============================================================
def fast_create_ticket(watcher_name, problem_desc, department, severity="P2"):
    counter = {"next_id": 1}
    if TICKET_COUNTER.exists():
        with open(TICKET_COUNTER) as f:
            counter = json.load(f)
    
    ticket_id = f"EVO-{counter['next_id']:04d}"
    counter["next_id"] += 1
    with open(TICKET_COUNTER, "w") as f:
        json.dump(counter, f, indent=2)
    
    ticket = {
        "ticket_id": ticket_id,
        "source": watcher_name,
        "problem": problem_desc,
        "department": department,
        "severity": severity,
        "created": datetime.datetime.now().isoformat(),
        "status": "open",
        "virtual_cycle_ms": 0,
    }
    
    tickets_file = TEAMS_DIR / "pending_tickets.json"
    tickets = []
    if tickets_file.exists():
        with open(tickets_file) as f:
            tickets = json.load(f)
    tickets.append(ticket)
    with open(tickets_file, "w") as f:
        json.dump(tickets, f, indent=2, ensure_ascii=False)
    
    print(f"🎫 [{ticket_id}] 新工单 ({VIRTUAL_TIME_SCALE['discovery_to_dispatch']}秒内派发)")
    return ticket_id

# ============================================================
# 2. 快速派发（3秒）
# ============================================================
def fast_dispatch(ticket_id, department):
    tickets_file = TEAMS_DIR / "pending_tickets.json"
    with open(tickets_file) as f:
        tickets = json.load(f)
    
    for t in tickets:
        if t["ticket_id"] == ticket_id:
            t["teams_dispatched"] = True
            t["dispatched_at"] = datetime.datetime.now().isoformat()
    
    with open(tickets_file, "w") as f:
        json.dump(tickets, f, indent=2, ensure_ascii=False)
    
    print(f"📦 [{ticket_id}] 已派发到 {department} 的3个团队 (盲盒)")
    return True

# ============================================================
# 3. 三队同时提交方案（3秒）
# ============================================================
def triple_submit(ticket_id, department, solutions):
    """
    solutions = [
        {"team": "team1", "approach": "...", "token_cost": 0, "quality": 9},
        {"team": "team2", "approach": "...", "token_cost": 0, "quality": 7},
        {"team": "team3", "approach": "...", "token_cost": 500, "quality": 8},
    ]
    """
    for sol in solutions:
        tc = sol.get("token_cost", sol.get("tokens_consumed", 0))
        record_token_cost(ticket_id, department, sol["team"], tc)
    
    print(f"🧠 [{ticket_id}] 3个团队方案已出 ({VIRTUAL_TIME_SCALE['dispatch_to_solution']}秒)")
    for sol in solutions:
        tc = sol.get("token_cost", sol.get("tokens_consumed", 0))
        token_str = f"{tc} token" if tc > 0 else "0 token ✅"
        print(f"   {sol['team']}: {sol['quality']}/10分 | {token_str}")
    
    return solutions

# ============================================================
# 4. 极速回溯（2秒）
# ============================================================
def fast_review(ticket_id, department, solutions):
    """2秒出结论：选最优、淘汰最差、标记需本地化"""
    
    # 评分 = quality - token_cost / 500（惩罚规则：每500 token扣1分）
    for sol in solutions:
        tc = sol.get("token_cost", sol.get("tokens_consumed", 0))
        penalty = tc / 500
        sol["final_score"] = sol["quality"] - penalty
        sol["token_free"] = tc == 0
        sol["token_cost"] = tc
    
    # 排序
    ranked = sorted(solutions, key=lambda s: -s["final_score"])
    winner = ranked[0]
    loser = ranked[-1]
    
    # 标准化解决方案字段
    normalized_solutions = []
    for sol in solutions:
        ns = dict(sol)
        ns["tokens_consumed"] = ns.get("token_cost", 0)
        normalized_solutions.append(ns)

    # 记录到进化日志
    data = load_evolution_data()
    round_id = len(data["rounds"]) + 1
    
    round_entry = {
        "round_id": round_id,
        "ticket_id": ticket_id,
        "department": department,
        "submitted": datetime.datetime.now().isoformat(),
        "solutions": normalized_solutions,
        "winner": winner["team"],
        "loser": loser["team"],
        "winner_score": winner["final_score"],
        "loser_score": loser["final_score"],
        "virtual_duration_ms": TOTAL_CYCLE * 1000,
    }
    data["rounds"].append(round_entry)
    
    # 反哺最佳实践
    data["best_practices"].append({
        "origin": ticket_id,
        "approach": winner["approach"],
        "department": department,
        "team": winner["team"],
        "created": datetime.datetime.now().isoformat(),
        "token_free": winner["token_free"],
    })
    
    # 淘汰最差
    data["eliminated_approaches"].append({
        "team": loser["team"],
        "approach": loser["approach"],
        "department": department,
        "ticket_id": ticket_id,
        "reason": f"评分垫底 ({loser['final_score']}分)",
        "eliminated_at": datetime.datetime.now().isoformat(),
    })
    
    # 如果获胜方案消耗了token → 标记"待本地化"
    if not winner["token_free"]:
        print(f"   ⚠️ 优化方案消耗了token，已标记为[待本地化]")
    
    save_evolution_data(data)
    
    # 更新工单
    tickets_file = TEAMS_DIR / "pending_tickets.json"
    with open(tickets_file) as f:
        tickets = json.load(f)
    for t in tickets:
        if t["ticket_id"] == ticket_id:
            t["status"] = "resolved"
            t["resolution"] = {
                "winner": winner["team"],
                "winner_approach": winner["approach"],
                "loser": loser["team"],
            }
    with open(tickets_file, "w") as f:
        json.dump(tickets, f, indent=2, ensure_ascii=False)
    
    print(f"🏆 [{ticket_id}] 回溯完成 ({VIRTUAL_TIME_SCALE['review_to_conclusion']}秒)")
    print(f"   🥇 最优: {winner['team']} ({winner['final_score']:.1f}分)")
    print(f"   🗑️  淘汰: {loser['team']} ({loser['final_score']:.1f}分)")
    print(f"   📚 已入最佳实践库 ({VIRTUAL_TIME_SCALE['conclusion_to_stored']}秒内)")
    
    return round_id

# ============================================================
# 5. Token成本记录
# ============================================================
def record_token_cost(ticket_id, department, team_id, tokens):
    data = {"total_tokens": 0, "saved_tokens": 0, "savings_rate": 0, "records": []}
    if COST_LOG.exists():
        with open(COST_LOG) as f:
            data = json.load(f)
    
    data["records"].append({
        "ticket_id": ticket_id,
        "department": department,
        "team_id": team_id,
        "tokens": tokens,
        "timestamp": datetime.datetime.now().isoformat(),
    })
    data["total_tokens"] += tokens
    # 估算节约：本地解决的token按3倍算省下来的
    if tokens == 0:
        data["saved_tokens"] += 3000  # 假设本地解决可省3K token
    data["savings_rate"] = round(
        data["saved_tokens"] / (data["total_tokens"] + data["saved_tokens"]) * 100, 1
    ) if data["total_tokens"] + data["saved_tokens"] > 0 else 75
    
    with open(COST_LOG, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ============================================================
# 辅助
# ============================================================
def load_evolution_data():
    if EVOLUTION_LOG.exists():
        with open(EVOLUTION_LOG, encoding='utf-8') as f:
            return json.load(f)
    return {
        "created": datetime.datetime.now().isoformat(),
        "rounds": [],
        "best_practices": [],
        "eliminated_approaches": [],
    }

def save_evolution_data(data):
    with open(EVOLUTION_LOG, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ============================================================
# 6. 全自动极速推演（演示用）
# ============================================================
def run_express_cycle(problem, department, solutions, severity="P2"):
    """
    完整极速进化周期 = 约10秒
    """
    print(f"\n{'='*60}")
    print(f"⚡ 极速进化周期: [{department}] {problem[:40]}...")
    print(f"{'='*60}")
    
    # 阶段1: 发现问题→创建工单→派发（3秒）
    t0 = time.time()
    ticket_id = fast_create_ticket("express_watcher", problem, department, severity)
    time.sleep(0.5)
    fast_dispatch(ticket_id, department)
    t1 = time.time()
    print(f"   阶段1: {t1-t0:.1f}秒 (目标3秒)")
    
    # 阶段2: 3队出方案（3秒）
    time.sleep(0.3)
    submit_solutions = triple_submit(ticket_id, department, solutions)
    t2 = time.time()
    print(f"   阶段2: {t2-t1:.1f}秒 (目标3秒)")
    
    # 阶段3: 回溯→结论→入库（4秒）
    time.sleep(0.5)
    round_id = fast_review(ticket_id, department, submit_solutions)
    t3 = time.time()
    print(f"   阶段3: {t3-t2:.1f}秒 (目标4秒)")
    
    # 统计成本
    with open(COST_LOG) as f:
        cost_data = json.load(f)
    print(f"\n💰 当前节约率: {cost_data['savings_rate']}%")
    
    total_time = t3 - t0
    print(f"\n⏱️  全程耗时: {total_time:.1f}秒 (虚拟加速)")
    print(f"✅ 进化轮次 #{round_id} 完成")
    
    return ticket_id

# ============================================================
# 7. 批量推演：模拟10个连续问题
# ============================================================
def batch_express(problems):
    """
    连续处理10个问题，展示自动进化效果
    """
    print("="*70)
    print("⚡⚡⚡ 极速进化批量推演（10个问题同时跑）")
    print("="*70)
    
    results = []
    
    for i, prob in enumerate(problems):
        ticket_id = run_express_cycle(
            problem=prob["desc"],
            department=prob["dept"],
            solutions=prob["solutions"],
        )
        results.append(ticket_id)
    
    print("\n" + "="*70)
    print("📊 推演总结")
    print("="*70)
    print(f"总问题数: {len(problems)}")
    
    with open(COST_LOG) as f:
        cost_data = json.load(f)
    print(f"当前节约率: {cost_data['savings_rate']}%")
    
    with open(EVOLUTION_LOG, encoding='utf-8') as f:
        evo_data = json.load(f)
    print(f"进化轮次: {len(evo_data['rounds'])}")
    print(f"最佳实践库: {len(evo_data['best_practices'])} 条")
    print(f"已淘汰方案: {len(evo_data['eliminated_approaches'])} 个")
    
    return results

# ============================================================
# 跑一个单次极速周期演示
# ============================================================
if __name__ == "__main__":
    # 单次极速周期
    run_express_cycle(
        problem="caipiao1前端8088端口500错误，前端无法加载",
        department="frontend",
        solutions=[
            {"team": "先锋战队(Next.js)", "approach": "Playwright定位路由→修复Python路径+重启服务", "token_cost": 0, "quality": 9},
            {"team": "优雅战队(Vue3)", "approach": "Vue3重写前端适配层+兼容脚本", "token_cost": 0, "quality": 7},
            {"team": "极速战队(Hono)", "approach": "Hono快速重写临时前端+查GitHub参考", "token_cost": 500, "quality": 8},
        ],
    )
    
    # 演示批量推演（注释掉，以防影响单个演示）
    # batch_express([])
