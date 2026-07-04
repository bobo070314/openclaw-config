"""
IGP 国际集团金字塔引擎 v2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
自我进化 | 自我净化 | 不养闲人
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

核心改进点：
1. 12部门×3队 = 36个战队
2. 淘汰+再生（团队解散自动重组）
3. 月度KPI结算（全员经营责任制）
4. 外部吸收自动化（GitHub/论文扫描）
5. 参谋部（SWAT/审计/战略投资）
"""
import os
import json
import datetime
import time
import random
import re
import subprocess
from pathlib import Path

BASE_DIR = Path(r"D:\bobo\openclaw-foreign\workspace")
TEAMS_DIR = BASE_DIR / "family-corp-teams"
HEADQUARTERS_DIR = TEAMS_DIR / "headquarters"

EVOLUTION_LOG = TEAMS_DIR / "evolution_log.json"
COST_LOG = TEAMS_DIR / "cost_log.json"
TICKET_COUNTER = TEAMS_DIR / "ticket_counter.json"
KPI_LOG = TEAMS_DIR / "kpi_log.json"
ABSORPTION_LOG = TEAMS_DIR / "absorption_log.json"
OBSERVATION_POOL = TEAMS_DIR / "new_tools_pool.json"

# ════════════════════════════════════════════════════════
# 12个核心部门定义
# ════════════════════════════════════════════════════════
ALL_DEPARTMENTS = {
    # 核心技术部 (4)
    "frontend":     {"tier": "core",     "label": "前端"},
    "backend":      {"tier": "core",     "label": "后端"},
    "infrastructure": {"tier": "core",   "label": "基础设施"},
    "ai":           {"tier": "core",     "label": "人工智能"},
    # 业务交付部 (4)
    "mobile":       {"tier": "delivery", "label": "移动端"},
    "design":       {"tier": "delivery", "label": "设计"},
    "quality":      {"tier": "delivery", "label": "质量"},
    "pmo":          {"tier": "delivery", "label": "项目管理"},
    # 增长与营收部 (2)
    "growth":       {"tier": "revenue",  "label": "增长营收"},
    "data":         {"tier": "revenue",  "label": "数据商业"},
    # 支撑与合规部 (2)
    "tech-support": {"tier": "support",  "label": "技术支持"},
    "compliance":   {"tier": "support",  "label": "合规风控"},
}

# 团队名映射
TEAM_LABELS = {"team1": "队1(主流)", "team2": "队2(替代)", "team3": "队3(创新)"}

# ════════════════════════════════════════════════════════
# 1. 工单系统
# ════════════════════════════════════════════════════════
def create_ticket(source, problem, department, severity="P2"):
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
        "source": source,
        "problem": problem,
        "department": department,
        "severity": severity,
        "created": datetime.datetime.now().isoformat(),
        "status": "open",
        "dispatched": False,
        "resolved": False,
    }
    
    tickets_file = TEAMS_DIR / "pending_tickets.json"
    tickets = []
    if tickets_file.exists():
        with open(tickets_file, encoding="utf-8") as f:
            tickets = json.load(f)
    tickets.append(ticket)
    with open(tickets_file, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2, ensure_ascii=False)
    
    print(f"[ [{ticket_id}] 新工单 → {department} ({ALL_DEPARTMENTS.get(department,{}).get('tier','?')})")
    return ticket_id

def dispatch_ticket(ticket_id):
    tickets_file = TEAMS_DIR / "pending_tickets.json"
    with open(tickets_file, encoding="utf-8") as f:
        tickets = json.load(f)
    for t in tickets:
        if t["ticket_id"] == ticket_id:
            t["dispatched"] = True
            t["dispatched_at"] = datetime.datetime.now().isoformat()
    with open(tickets_file, "w") as f:
        json.dump(tickets, f, indent=2, ensure_ascii=False)
    print(f"[{ticket_id}] 已派发 → 盲盒3队")
    return True

# ════════════════════════════════════════════════════════
# 2. Token成本记录
# ════════════════════════════════════════════════════════
def record_cost(ticket_id, department, team_id, tokens):
    data = {"total_tokens": 0, "saved_tokens": 0, "savings_rate": 75, "records": []}
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
    if tokens == 0:
        data["saved_tokens"] += 3000
    total = data["total_tokens"] + data["saved_tokens"]
    data["savings_rate"] = round(data["saved_tokens"] / total * 100, 1) if total > 0 else 75
    
    with open(COST_LOG, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return data["savings_rate"]

# ════════════════════════════════════════════════════════
# 3. PK与回溯（核心进化）
# ════════════════════════════════════════════════════════
def run_pk(ticket_id, department, solutions):
    """
    solutions = [
        {"team": "team1/team2/team3", "approach": "...", "token_cost": N, "quality": 1-10},
        ...
    ]
    """
    print(f"\n🧠 [{ticket_id}] 3队提交方案")
    
    for sol in solutions:
        tc = sol.get("token_cost", sol.get("tokens_consumed", 0))
        record_cost(ticket_id, department, sol["team"], tc)
        sol["token_cost"] = tc
        sol["tokens_consumed"] = tc
    
    # 回溯评分
    return fast_review(ticket_id, department, solutions)

def fast_review(ticket_id, department, solutions):
    """评分 = quality - token_cost/500"""
    for sol in solutions:
        tc = sol.get("token_cost", 0)
        penalty = tc / max(sol.get("quality", 5), 1)  # 每质量分1分，消耗500 token扣1分
        sol["final_score"] = round(sol["quality"] - tc / 500, 1)
        sol["token_free"] = tc == 0
    
    ranked = sorted(solutions, key=lambda s: -s["final_score"])
    winner, loser = ranked[0], ranked[-1]
    
    data = load_evolution_data()
    round_id = len(data["rounds"]) + 1
    
    norm_solutions = []
    for sol in solutions:
        ns = dict(sol)
        ns["tokens_consumed"] = ns.get("token_cost", 0)
        norm_solutions.append(ns)
    
    round_entry = {
        "round_id": round_id,
        "ticket_id": ticket_id,
        "department": department,
        "submitted": datetime.datetime.now().isoformat(),
        "solutions": norm_solutions,
        "winner": winner["team"],
        "loser": loser["team"],
        "winner_score": winner["final_score"],
        "loser_score": loser["final_score"],
    }
    data["rounds"].append(round_entry)
    
    # 胜者入实践库
    data["best_practices"].append({
        "origin": ticket_id,
        "approach": winner["approach"],
        "department": department,
        "team": winner["team"],
        "created": datetime.datetime.now().isoformat(),
        "token_free": winner["token_free"],
    })
    
    # 败者标记（含历史检查 → 连续2次淘汰）
    loser_record = {
        "team": loser["team"],
        "approach": loser["approach"],
        "department": department,
        "ticket_id": ticket_id,
        "score": loser["final_score"],
        "reason": f"评分垫底 ({loser['final_score']}分)",
        "eliminated_at": datetime.datetime.now().isoformat(),
    }
    data["eliminated_approaches"].append(loser_record)
    
    save_evolution_data(data)
    
    # 关闭工单
    tickets_file = TEAMS_DIR / "pending_tickets.json"
    with open(tickets_file) as f:
        tickets = json.load(f)
    for t in tickets:
        if t["ticket_id"] == ticket_id:
            t["status"] = "resolved"
            t["resolution"] = {
                "winner": winner["team"],
                "loser": loser["team"],
                "round_id": round_id,
            }
    with open(tickets_file, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2, ensure_ascii=False)
    
    #
    check_elimination(loser["team"], department)
    # ⚠️ 更新KPI
    update_kpi(department, winner["team"], winner["final_score"], loser["team"])
    
    print(f"🏆 [{ticket_id}] 回溯完成 轮次#{round_id}")
    print(f"   🥇 {winner['team']}: {winner['final_score']}分 | token:{winner.get('token_cost',0)}")
    print(f"   🗑️  {loser['team']}: {loser['final_score']}分 | token:{loser.get('token_cost',0)}")
    
    return round_id

def check_elimination(loser_team, department):
    """血液循环淘汰 v2.0 — 委托到独立模块"""
    return _blood_eliminate(loser_team, department)

def _blood_eliminate(loser_team, department):
    """血液循环淘汰核心逻辑"""
    data = load_evolution_data()
    losses = []
    for r in data.get("eliminated_approaches", []):
        if r.get("team") == loser_team and r.get("department") == department:
            losses.append(r)
    
    team_type = _get_blood_type(loser_team, department)
    dept_label = ALL_DEPARTMENTS.get(department, {}).get("label", department)
    
    print(f"  [BLOOD] {loser_team}@{dept_label} 血型={team_type} 本轮评分={losses[-1].get('score', 0) if losses else '?'}")
    
    if team_type == "platelet":
        if losses and losses[-1].get("score", 5) <= 2:
            print(f"  [ELIM] 血小板→一次致命失误直接走人")
            _blood_regen(loser_team, department, losses, team_type)
            return True
        return False
    
    if team_type == "white_blood":
        if len(losses) >= 2:
            print(f"  [ELIM] 白细胞→新人撞两次墙，走人")
            _blood_regen(loser_team, department, losses, team_type)
            return True
        if losses:
            print(f"  [WARN] 白细胞警告：已输1次，再输1次走人！下次必须赢回来")
        return False
    
    if team_type == "red_blood":
        if len(losses) >= 3:
            print(f"  [ELIM] 红细胞→老将连续{len(losses)}次垫底，该退了")
            _blood_regen(loser_team, department, losses, team_type)
            return True
        if losses:
            print(f"  [WARN] 红细胞警告：已垫底{len(losses)}次，还剩{3 - len(losses)}次机会")
        return False
    return False

# ════════════════════════════════════════════════════════
# 4. 淘汰与再生（自我净化核心）
# ════════════════════════════════════════════════════════
def trigger_regeneration(loser_team, department, loss_history, blood_type="white_blood"):
    """团队解散→重组流程 — 换上新血（默认白细胞 敢冲敢闯）"""
    print(f"   [RECYCLE] 启动换血流程...")
    
    regen_file = TEAMS_DIR / "regeneration_log.json"
    regen_data = []
    if regen_file.exists():
        with open(regen_file, encoding='utf-8') as f:
            regen_data = json.load(f)
    
    new_tool_stack = suggest_new_tool_stack(department)
    
    regen_event = {
        "event_id": f"REGEN-{len(regen_data)+1:04d}",
        "date": datetime.datetime.now().isoformat(),
        "department": department,
        "disbanded_team": loser_team,
        "blood_type": blood_type,
        "loss_history": loss_history,
        "new_tool_stack": new_tool_stack,
        "replacement_creed": "新人敢冲敢闯，允许犯错但必须主动出击",
        "status": "reorganized",
    }
    regen_data.append(regen_event)
    with open(regen_file, "w", encoding="utf-8") as f:
        json.dump(regen_data, f, indent=2, ensure_ascii=False)
    
    # 新人自动注册为白细胞
    identify_blood_type.cache_clear()
    
    print(f"   [OK] {blood_type}换血完成 → 新人(白细胞)上任!")
    print(f"   [IN] 新工具栈: {new_tool_stack}")
    print(f"   [CREED] 新人宣言：敢冲敢闯，输了就走，赢了就留")
def suggest_new_tool_stack(department):
    """动态推荐新工具栈 — 从观察池优先，无则fallback"""
    pool_path = TEAMS_DIR / "new_tools_pool.json"
    if pool_path.exists():
        try:
            pool = json.load(open(pool_path, encoding="utf-8"))
            candidates = pool.get("candidates", [])
            if candidates:
                fresh = sorted(candidates, key=lambda x: x.get("added", ""), reverse=True)[:3]
                return " / ".join([c.get("name", "?") for c in fresh]) + " (观察池)"
        except:
            pass
    
    fallback = {
        "frontend": "Solid.js / Qwik / Astro (新人三件套)",
        "backend": "Hono / Elysia / PocketBase (新后端三剑客)",
        "infrastructure": "Coolify / Traefik / Docker Compose (轻量基础设施)",
        "ai": "OpenAI Agents SDK / LangGraph / CrewAI (多Agent框架)",
        "mobile": "Expo / React Native / Flutter (跨平台)",
        "design": "Tailwind v4 / shadcn/ui / Motion (现代设计)",
        "quality": "Playwright / Vitest / Biome (质量铁三角)",
        "pmo": "Linear / Notion AI / Plane (项目管理新秀)",
        "growth": "PostHog / Loops / Beehiiv (增长引擎)",
        "data": "DuckDB / Evidence / MotherDuck (轻量数据栈)",
        "tech-support": "Zammad / Freshdesk / GitBook (支持工具链)",
        "compliance": "OpenPolicyAgent / Sigstore / in-toto (合规自动化)",
    }
    return fallback.get(department, "新人工具栈（待探索）")


# ════════════════════════════════════════════════════════
# 5. KPI月度结算（不养闲人核心）
# ════════════════════════════════════════════════════════
def update_kpi(department, winner_team, winner_score, loser_team):
    """每次PK后更新KPI"""
    data = {"departments": {}, "teams": {}}
    if KPI_LOG.exists():
        with open(KPI_LOG, encoding='utf-8') as f:
            data = json.load(f)
    
    # 部门级KPI
    if department not in data["departments"]:
        data["departments"][department] = {
            "total_pk": 0, "wins": 0, "losses": 0,
            "total_score": 100, "history": [],
        }
    dept = data["departments"][department]
    dept["total_pk"] += 1
    dept["wins"] += 1
    dept["losses"] += 1
    dept["total_score"] += (winner_score - 5)  # 基于质量分波动
    dept["history"].append({
        "round": len(dept["history"]) + 1,
        "winner": winner_team,
        "loser": loser_team,
        "delta": winner_score - 5,
        "ts": datetime.datetime.now().isoformat(),
    })
    
    # 团队级KPI
    for team_id in [winner_team, loser_team]:
        key = f"{department}:{team_id}"
        if key not in data["teams"]:
            data["teams"][key] = {
                "department": department,
                "team": team_id,
                "score": 100,
                "wins": 0,
                "losses": 0,
                "eliminated": False,
            }
        team_kpi = data["teams"][key]
        if team_id == winner_team:
            team_kpi["score"] += 10
            team_kpi["wins"] += 1
        else:
            team_kpi["score"] -= 30
            team_kpi["losses"] += 1
        team_kpi["score"] = max(team_kpi["score"], 0)
        # 标记淘汰
        if team_kpi["losses"] >= 2 and team_kpi["score"] < 50:
            team_kpi["eliminated"] = True
    
    with open(KPI_LOG, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def monthly_kpi_report():
    """生成月度KPI结算报告"""
    if not KPI_LOG.exists():
        print("📊 尚无KPI数据")
        return
    
    with open(KPI_LOG, encoding='utf-8') as f:
        kpi = json.load(f)
    
    print("\n" + "=" * 60)
    print("📊 IGP 月度KPI结算报告")
    print("=" * 60)
    
    # 部门排名
    depts = sorted(kpi["departments"].items(), key=lambda x: -x[1]["total_score"])
    print("\n🏢 部门健康度排名:")
    for name, d in depts:
        label = ALL_DEPARTMENTS.get(name, {}).get("label", name)
        tier = ALL_DEPARTMENTS.get(name, {}).get("tier", "?")
        score = d["total_score"]
        pk_count = d["total_pk"]
        
        if score >= 120:
            badge = "🟢 金牌"
        elif score >= 80:
            badge = "🟡 银牌"
        elif score >= 50:
            badge = "🟠 铜牌"
        else:
            badge = "🔴 红灯(重组)"
        
        print(f"   {badge} {label}({tier}): {score}分 | PK次数:{pk_count}")
    
    # 团队淘汰预警
    print("\n⚠️  团队淘汰预警:")
    for key, t in kpi["teams"].items():
        if t["eliminated"]:
            print(f"   ❌ {t['team']} @ {t['department']} | 分:{t['score']}")
        elif t["score"] < 60:
            print(f"   ⚠️  {t['team']} @ {t['department']} | 分:{t['score']} (危险)")
    
    print("\n✅ 报告完成")

# ════════════════════════════════════════════════════════
# 6. 外部吸收扫描
# ════════════════════════════════════════════════════════
def scan_external_tools():
    """模拟扫描GitHub Trending / HN / 论文"""
    print("\n📡 外部吸收扫描...")
    
    # 模拟发现
    discovered = [
        {"name": "Solid.js 2.0", "source": "github", "stars": 35000, "dept": "frontend", "reason": "新信号响应框架，性能优于React"},
        {"name": "Bun 1.2", "source": "github", "stars": 28000, "dept": "backend", "reason": "全栈JS runtime，替代Node"},
        {"name": "MLX Swift", "source": "github", "stars": 15000, "dept": "ai", "reason": "Apple芯片本地AI推理"},
        {"name": "DuckDB 1.0", "source": "hn", "stars": 12000, "dept": "data", "reason": "嵌入式OLAP数据库"},
        {"name": "Penpot", "source": "github", "stars": 18000, "dept": "design", "reason": "开源Figma替代"},
        {"name": "Linear", "source": "hn", "stars": 20000, "dept": "pmo", "reason": "极速项目管理工具"},
    ]
    
    pool = []
    if OBSERVATION_POOL.exists():
        with open(OBSERVATION_POOL, encoding='utf-8') as f:
            pool = json.load(f)
    
    new_count = 0
    for tool in discovered:
        # 去重
        if any(p["name"] == tool["name"] for p in pool):
            continue
        tool["scanned_at"] = datetime.datetime.now().isoformat()
        tool["status"] = "observation"  # observation | absorbed | ignored
        pool.append(tool)
        new_count += 1
        print(f"   🔍 发现: {tool['name']} ⭐{tool['stars']} → {tool['dept']}")
    
    with open(OBSERVATION_POOL, "w", encoding="utf-8") as f:
        json.dump(pool, f, indent=2, ensure_ascii=False)
    
    if new_count == 0:
        print("   无新发现（或已存在观察池中）")
    else:
        print(f"   ✅ 发现 {new_count} 个新工具/技术，已入观察池")
    
    # 将观察池中"准备吸收"的派发
    for tool in pool:
        if tool["status"] == "observation":
            # 战略投资部决定是否吸收
            print(f"   💡 建议: {tool['name']} → 派发吸收工单到{tool['dept']}")
    
    return pool

def trigger_absorption(tool_name, department):
    """触发外部吸收流程"""
    ticket_id = create_ticket(
        source="战略投资部(外部吸收)",
        problem=f"吸收新技术: {tool_name}",
        department=department,
        severity="P3",
    )
    dispatch_ticket(ticket_id)
    
    # 更新观察池状态
    pool = []
    if OBSERVATION_POOL.exists():
        with open(OBSERVATION_POOL, encoding='utf-8') as f:
            pool = json.load(f)
    for t in pool:
        if t["name"] == tool_name:
            t["status"] = "absorbing"
            t["absorbed_at"] = datetime.datetime.now().isoformat()
    with open(OBSERVATION_POOL, "w", encoding="utf-8") as f:
        json.dump(pool, f, indent=2, ensure_ascii=False)
    
    print(f"📥 [{ticket_id}] 吸收任务已派发: {tool_name}")
    return ticket_id

# ════════════════════════════════════════════════════════
# 7. 参谋部报告
# ════════════════════════════════════════════════════════
def headquarters_report():
    """生成总部综合状态"""
    print("\n" + "=" * 60)
    print("🏛️  IGP 总部综合报告")
    print("=" * 60)
    
    # 1. 审计看板
    print("\n🔍 [审计部] 部门健康度:")
    if KPI_LOG.exists():
        with open(KPI_LOG, encoding='utf-8') as f:
            kpi = json.load(f)
        
        for dept_name, dept_data in sorted(kpi["departments"].items(), key=lambda x: -x[1]["total_score"]):
            s = dept_data["total_score"]
            if s >= 100:
                icon = "🟢"
            elif s >= 70:
                icon = "🟡"
            else:
                icon = "🔴"
            tier = ALL_DEPARTMENTS.get(dept_name, {}).get("tier", "?")
            label = ALL_DEPARTMENTS.get(dept_name, {}).get("label", dept_name)
            print(f"   {icon} {label}: {s}分 (tier:{tier})")
    
    # 2. 战略投资部看板
    print("\n💡 [战略投资部] 外部观察池:")
    if OBSERVATION_POOL.exists():
        with open(OBSERVATION_POOL, encoding='utf-8') as f:
            pool = json.load(f)
        for t in pool:
            icon = "📡" if t["status"] == "observation" else "📥"
            print(f"   {icon} {t['name']}: {t['status']} → {t['dept']}")
    
    # 3. SWAT状态
    print("\n🗡️  [SWAT] 状态: 待命中")
    
    # 4. 进化统计
    data = load_evolution_data()
    print(f"\n📊 进化统计:")
    print(f"   总轮次: {len(data['rounds'])}")
    print(f"   最佳实践: {len(data['best_practices'])}")
    print(f"   已淘汰: {len(data['eliminated_approaches'])}")
    
    return True

# ════════════════════════════════════════════════════════
# 8. 数据持久化
# ════════════════════════════════════════════════════════
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

# ════════════════════════════════════════════════════════
# 9. Goal 集成（OpenClaw 持久目标）
# ════════════════════════════════════════════════════════

def goal_create_tool(objective):
    """调用 OpenClaw create_goal 工具（通过 subprocess 桥接）
    注意：真正运行时由 AI 直接调用工具，这里做日志记录 + 模拟验证。
    """
    goal_file = TEAMS_DIR / "active_goal.json"
    goal = {
        "objective": objective,
        "status": "active",
        "created": datetime.datetime.now().isoformat(),
        "completed": None,
        "blocked": None,
    }
    with open(goal_file, "w", encoding="utf-8") as f:
        json.dump(goal, f, indent=2, ensure_ascii=False)
    print(f"🎯 Goal 已创建: {objective[:60]}...")
    print(f"   状态: active")
    return goal

def goal_update_tool(status, note=""):
    """调用 OpenClaw update_goal 工具"""
    goal_file = TEAMS_DIR / "active_goal.json"
    if not goal_file.exists():
        print("⚠️  没有活跃 Goal")
        return False
    
    with open(goal_file, encoding="utf-8") as f:
        goal = json.load(f)
    
    goal["status"] = status
    goal["note"] = note
    if status == "complete":
        goal["completed"] = datetime.datetime.now().isoformat()
    elif status == "blocked":
        goal["blocked"] = datetime.datetime.now().isoformat()
    
    with open(goal_file, "w", encoding="utf-8") as f:
        json.dump(goal, f, indent=2, ensure_ascii=False)
    
    badge = {"complete": "✅", "blocked": "⛔", "active": "🔄"}[status]
    print(f"{badge} Goal 状态更新: {status} | {note}")
    return True

def goal_get_tool():
    """检查当前目标"""
    goal_file = TEAMS_DIR / "active_goal.json"
    if not goal_file.exists():
        return None
    with open(goal_file, encoding="utf-8") as f:
        return json.load(f)

def has_active_goal():
    goal = goal_get_tool()
    return goal is not None and goal["status"] == "active"

def boss_progress_summary():
    """在 Goal 运行时，给你汇报进度"""
    goal = goal_get_tool()
    if not goal:
        return "当前无活跃目标"
    
    data = load_evolution_data()
    pending_file = TEAMS_DIR / "pending_tickets.json"
    pending = 0
    if pending_file.exists():
        with open(pending_file, encoding="utf-8") as f:
            tickets = json.load(f)
            pending = sum(1 for t in tickets if t["status"] == "open")
    
    total_rounds = len(data["rounds"])
    saved_tokens = 0
    if COST_LOG.exists():
        with open(COST_LOG) as f:
            cost = json.load(f)
            saved_tokens = cost.get("saved_tokens", 0)
    
    return {
        "goal": goal["objective"][:80],
        "status": goal["status"],
        "rounds_done": total_rounds,
        "pending_tickets": pending,
        "tokens_saved": saved_tokens,
    }

# ════════════════════════════════════════════════════════
# 10. Boss 一句话触发接口（自动识别+Goal）
# ════════════════════════════════════════════════════════

BOSS_INTENTS = {
    # 技术和产品工作
    "fix": ["修复", "修", "改bug", "bug", "500", "错误", "报错", "故障", "crash", "崩溃", "error"],
    "feature": ["开发", "新增", "做个", "加个", "实现", "构建", "搭建", "创建"],
    "optimize": ["优化", "提升", "加速", "重构", "改善", "改进"],
    "deploy": ["部署", "上线", "发布", "推送", "发布到"],
    # 吸收和学习
    "absorb": ["吸收", "学习", "引进", "研究", "试用", "评估"],
    "scan": ["扫描", "看看有什么", "检查市场", "竞品"],
    # 管理
    "report": ["报告", "总结", "汇报", "统计", "分析", "看下", "看看各个"],
    "reorganize": ["重组", "解散", "淘汰", "合并", "拆分", "换工具", "换技术栈"],
}

# 部门关键词映射
DEPT_KEYWORDS = {
    "前端": "frontend", "前端页面": "frontend", "UI": "frontend", "页面": "frontend",
    "后端": "backend", "API": "backend", "接口": "backend", "服务器": "backend",
    "基础": "infrastructure", "运维": "infrastructure", "部署": "infrastructure", "CI": "infrastructure",
    "AI": "ai", "llm": "ai", "gpt": "ai", "智能": "ai", "人工": "ai",
    "移动": "mobile", "手机": "mobile", "iOS": "mobile", "Android": "mobile", "app": "mobile",
    "设计": "design", "UI": "design", "UX": "design", "Figma": "design",
    "质量": "quality", "测试": "quality", "QA": "quality", "自动化": "quality",
    "项目": "pmo", "管理": "pmo", "进度": "pmo",
    "增长": "growth", "流量": "growth", "增长": "growth", "SEO": "growth", "运营": "growth",
    "数据": "data", "报表": "data", "分析": "data", "BI": "data",
    "支持": "tech-support", "客服": "tech-support", "售后": "tech-support", "问题": "tech-support",
    "合规": "compliance", "法务": "compliance", "合同": "compliance", "审计": "compliance",
}

def parse_boss_intent(text):
    """解析老板一句话的意图"""
    intent = None
    department = None
    
    # 匹配意图
    for intent_name, keywords in BOSS_INTENTS.items():
        for kw in keywords:
            if kw in text:
                intent = intent_name
                break
        if intent:
            break
    
    if not intent:
        # 默认：如果包含部门关键词，也触发
        for dept_kw, dept in DEPT_KEYWORDS.items():
            if dept_kw in text:
                intent = "fix"  # 默认修
                break
    
    # 匹配部门
    for dept_kw, dept in DEPT_KEYWORDS.items():
        if dept_kw in text:
            department = dept
            break
    
    return intent, department

def boss_speak(text):
    """
    老板一句话，引擎自动判断 + 触发 Goal + 执行
    
    Args:
        text: 你的话，比如"修复前端500错误"、"学习Solid.js"、"看看各部门状态"
    
    Returns:
        处理结果摘要
    """
    print(f"\n{'='*65}")
    print(f"🗣️  老板说: {text}")
    print(f"{'='*65}")
    
    # 1. 解析意图
    intent, department = parse_boss_intent(text)
    print(f"📋 解析: intent={intent}, department={department}")
    
    # 2. 根据意图选择执行路径
    
    # 如果是管理类（报告/总结）→ 不走 Goal，直接出报告
    if intent == "report":
        headquarters_report()
        monthly_kpi_report()
        return {"action": "report", "output": "总部报告已生成"}
    
    if intent == "scan":
        scan_external_tools()
        return {"action": "scan", "output": "外部扫描完成"}
    
    # 3. 需要开车门（创建 Goal）
    # 创建目标描述
    objective = f"IGP: {text}"
    
    # 检查是否已有活跃 Goal
    if has_active_goal():
        existing = goal_get_tool()
        print(f"⚠️  已有活跃 Goal: {existing['objective'][:50]}...")
        print(f"   先标记完成前面的，再继续")
        summary = boss_progress_summary()
        return {"action": "blocked", "existing_goal": existing["objective"], "summary": summary}
    
    # 4. 创建 Goal
    goal_create_tool(objective)
    
    # 5. 自动派发工单（如果有部门信息）
    ticket_id = None
    if department:
        ticket_id = create_ticket(
            source="boss_directive",
            problem=text,
            department=department,
            severity=getattr(intent, "severity", "P2"),
        )
        dispatch_ticket(ticket_id)
    
    # 6. 如果不是预定义的PK场景，提示 AI 继续处理
    # （实际运行中，AI 会看到 Goal 被创建，自动继续走）
    
    summary = boss_progress_summary()
    return {
        "action": "goal_created",
        "intent": intent,
        "department": department,
        "ticket_id": ticket_id,
        "goal": objective,
        "summary": summary,
    }

def boss_mark_complete(note=""):
    """老板说搞定了"""
    return goal_update_tool("complete", note or "任务完成")

def boss_mark_blocked(reason=""):
    """老板说卡住了"""
    return goal_update_tool("blocked", reason or "需要你决策")

# ════════════════════════════════════════════════════════
# 11. 完整推演
# ════════════════════════════════════════════════════════
def run_full_cycle(problem, department, solutions, severity="P2", source="watcher"):
    """完整IGP进化周期"""
    print(f"\n{'='*60}")
    print(f"⚡ IGP进化周期: [{department}] {problem[:50]}")
    print(f"{'='*60}")
    
    t0 = time.time()
    ticket_id = create_ticket(source, problem, department, severity)
    time.sleep(0.3)
    dispatch_ticket(ticket_id)
    
    time.sleep(0.3)
    round_id = run_pk(ticket_id, department, solutions)
    
    elapsed = time.time() - t0
    print(f"\n⏱️  周期耗时: {elapsed:.1f}秒")
    print(f"✅ 周期完成 (轮次#{round_id})")
    
    return ticket_id



# ===== 血液循环系统 v2.0 - 血型注册与识别 =====
import functools as _ft

_blood_types = {}

def register_blood_type(department, team_id, blood_type):
    _blood_types[f"{department}:{team_id}"] = blood_type
    return blood_type

@_ft.lru_cache(maxsize=256)
def _get_blood_type(team_id, department):
    cached = _blood_types.get(f"{department}:{team_id}")
    if cached:
        return cached
    data = load_evolution_data()
    for bp in data.get("best_practices", []):
        if bp.get("team") == team_id and bp.get("department") == department:
            _blood_types[f"{department}:{team_id}"] = "red_blood"
            return "red_blood"
    _blood_types[f"{department}:{team_id}"] = "white_blood"
    return "white_blood"

def _blood_regen(loser_team, department, loss_history, blood_type):
    """换血再生 — 新人默认白细胞"""
    regen_file = TEAMS_DIR / "regeneration_log.json"
    regen_data = []
    if regen_file.exists():
        with open(regen_file, encoding="utf-8") as f:
            regen_data = json.load(f)
    new_ts = suggest_new_tool_stack(department)
    regen_data.append({
        "event_id": f"REGEN-{len(regen_data)+1:04d}",
        "date": datetime.datetime.now().isoformat(),
        "department": department, "disbanded_team": loser_team,
        "blood_type": blood_type, "loss_history": loss_history,
        "new_tool_stack": new_ts,
        "replacement_creed": "新人敢冲敢闯，允许犯错但必须主动出击",
        "status": "reorganized",
    })
    with open(regen_file, "w", encoding="utf-8") as f:
        json.dump(regen_data, f, indent=2, ensure_ascii=False)
    _get_blood_type.cache_clear()
    print(f"  [OK] {blood_type}换血完成 -> 新人(白细胞)上任!")
    print(f"  [IN] 新工具栈: {new_ts}")
    print(f"  [CREED] 新人宣言：敢冲敢闯，输了就走，赢了就留")

# ════════════════════════════════════════════════════════
# 10. 演示：完整IGP推演
# ════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 70)
    print("🔷 IGP 国际集团金字塔引擎 v2.0 启动")
    print("=" * 70)
    
    # 演示 Goal 集成：模拟老板说话
    print("\n📝 演示：老板一句话触发 Goal + 引擎")
    print("-" * 50)
    
    # 场景1：老板说修复问题
    boss_speak("修复前端页面500错误，排查前端问题")
    
    # 模拟引擎跑(PK)
    run_full_cycle(
        problem="前端页面8088端口500错误",
        department="frontend",
        solutions=[
            {"team": "team1(Next.js)", "approach": "Playwright定位→修复路径", "token_cost": 0, "quality": 9},
            {"team": "team2(Vue3)", "approach": "Vue3重写适配层", "token_cost": 0, "quality": 7},
            {"team": "team3(Solid.js)", "approach": "Solid.js重写页面", "token_cost": 500, "quality": 8},
        ],
    )
    
    # PK 完成 → 标记 Goal 完成
    boss_mark_complete("前段team1胜出，最佳实践已入库")
    
    # 场景2：老板说报告
    print("\n" + "-" * 50)
    print("📝 场景2：老板说看报告")
    print("-" * 50)
    boss_speak("看看各部门状态和分析一下成本")
    
    # 场景3：外部吸收
    print("\n" + "-" * 50)
    print("📝 场景3：老板说要吸收新技术")
    print("-" * 50)
    boss_speak("看看GitHub上有什么新前端工具可以吸收")
    
    # 外部吸收扫描
    scan_external_tools()
    
    print(f"\n{'='*70}")
    print("🔷 推演完成 | Goal + IGP 已集成，等待老板指令")
    print(f"{'='*70}")


