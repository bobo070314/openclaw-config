"""
全自动进化编排引擎
链路：看门狗发现问题→自动创建工单→3个团队自动出方案→3天后自动对比→最佳方案反哺→最差淘汰
"""
import os
import json
import datetime
import subprocess
from pathlib import Path

BASE_DIR = Path(r"D:\bobo\openclaw-foreign\workspace")
TEAMS_DIR = BASE_DIR / "family-corp-teams"
TASKS_DIR = BASE_DIR / "family-corp-tasks"
ASSIGN_DIR = TASKS_DIR / "assignments"
MEMORY_DIR = BASE_DIR / "memory"

EVOLUTION_LOG = TEAMS_DIR / "evolution_log.json"
COST_LOG = TEAMS_DIR / "cost_log.json"
TICKET_COUNTER = TEAMS_DIR / "ticket_counter.json"

# ============================================================
# 1. 自动创建工单（从看门狗触发）
# ============================================================
def detect_and_create_ticket(watcher_name, problem_desc, department, severity="P2"):
    """
    看门狗扫描到异常 → 自动创建工单
    返回 ticket_id
    """
    # 读取计数器
    counter = {"next_id": 1}
    if TICKET_COUNTER.exists():
        with open(TICKET_COUNTER) as f:
            counter = json.load(f)
    
    ticket_id = f"EVO-{counter['next_id']:04d}"
    counter["next_id"] += 1
    with open(TICKET_COUNTER, "w") as f:
        json.dump(counter, f, indent=2)
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    ticket = {
        "ticket_id": ticket_id,
        "source": watcher_name,
        "problem": problem_desc,
        "department": department,
        "severity": severity,
        "created": now,
        "status": "open",
        "teams_dispatched": False,
        "three_day_review": None,
    }
    
    # 写入看门狗工作流文件
    tickets_file = TEAMS_DIR / "pending_tickets.json"
    tickets = []
    if tickets_file.exists():
        with open(tickets_file) as f:
            tickets = json.load(f)
    tickets.append(ticket)
    with open(tickets_file, "w") as f:
        json.dump(tickets, f, indent=2, ensure_ascii=False)
    
    print(f"🎫 [{ticket_id}] 新工单: [{department}] {problem_desc[:50]}...")
    return ticket_id

# ============================================================
# 2. 自动派发到3个团队（盲盒机制）
# ============================================================
def dispatch_to_teams(ticket_id, department):
    """
    工单自动派发到对应部门的3个团队
    每个团队收到一个"盲盒"——只知道问题，不知道其他团队的方案
    """
    tickets_file = TEAMS_DIR / "pending_tickets.json"
    with open(tickets_file) as f:
        tickets = json.load(f)
    
    ticket_found = None
    for t in tickets:
        if t["ticket_id"] == ticket_id:
            ticket_found = t
            break
    
    if not ticket_found:
        print(f"❌ 工单 {ticket_id} 未找到")
        return
    
    # 检查该部门是否有对应的团队目录
    dept_dir = TEAMS_DIR / department
    if not dept_dir.exists():
        print(f"⚠️ 部门 {department} 无团队目录，创建通用工单")
        return
    
    # 生成3个团队的工单文件
    teams = ["team1", "team2", "team3"]
    team_names = {
        "team1": "先锋/主流方案",
        "team2": "国产/替代方案",
        "team3": "极速/创新方案",
    }
    
    for team_id in teams:
        team_file = dept_dir / f"{team_id}.md"
        if not team_file.exists():
            print(f"  ⚠️ {team_id} 不存在, 跳过")
            continue
        
        # 在团队目录下创建任务文件（盲盒）
        task_file = dept_dir / f"task_{ticket_id}.json"
        blind_box = {
            "ticket_id": ticket_id,
            "problem": ticket_found["problem"],
            "your_team": team_id,
            "other_teams": "未知（盲盒机制）",
            "deadline": (
                datetime.datetime.now() + datetime.timedelta(days=3)
            ).isoformat(),
            "status": "pending",
            "submitted": False,
        }
        with open(task_file, "w") as f:
            json.dump(blind_box, f, indent=2, ensure_ascii=False)
        
        print(f"  📦 {department}/{team_id} 已收到盲盒工单")
    
    # 更新工单状态
    ticket_found["teams_dispatched"] = True
    ticket_found["dispatched_at"] = datetime.datetime.now().isoformat()
    with open(tickets_file, "w") as f:
        json.dump(tickets, f, indent=2, ensure_ascii=False)
    
    return True

# ============================================================
# 3. 团队提交方案
# ============================================================
def submit_team_solution(ticket_id, department, team_id, approach, cost_tokens=0, quality_score=5):
    """
    团队提交方案
    触发进化引擎记录
    """
    dept_dir = TEAMS_DIR / department
    task_file = dept_dir / f"task_{ticket_id}.json"
    
    if not task_file.exists():
        print(f"❌ 任务文件 {task_file} 不存在")
        return
    
    with open(task_file) as f:
        task = json.load(f)
    
    task["submitted"] = True
    task["approach"] = approach
    task["cost_tokens"] = cost_tokens
    task["quality_score"] = quality_score
    task["submitted_at"] = datetime.datetime.now().isoformat()
    
    with open(task_file, "w") as f:
        json.dump(task, f, indent=2, ensure_ascii=False)
    
    # 记录token消耗
    record_cost(ticket_id, department, team_id, cost_tokens)
    
    print(f"  ✅ {department}/{team_id} 方案已提交 (token: {cost_tokens}, 质量: {quality_score}/10)")
    return True

# ============================================================
# 4. 三天回溯自动对比
# ============================================================
def auto_review_ticket(ticket_id, department):
    """
    3天后自动对比3个团队方案
    选最佳、淘汰最差
    """
    dept_dir = TEAMS_DIR / department
    if not dept_dir.exists():
        return
    
    # 读取3个团队的任务文件
    solutions = []
    team_map = {"team1": "先锋/主流", "team2": "国产/替代", "team3": "极速/创新"}
    
    for team_id in ["team1", "team2", "team3"]:
        task_file = dept_dir / f"task_{ticket_id}.json"
        if task_file.exists():
            with open(task_file) as f:
                task = json.load(f)
            if task.get("submitted"):
                solutions.append({
                    "team": team_id,
                    "name": team_map.get(team_id, team_id),
                    "approach": task.get("approach", ""),
                    "cost_tokens": task.get("cost_tokens", 0),
                    "quality_score": task.get("quality_score", 0),
                })
    
    if len(solutions) < 2:
        print(f"⏳ 工单 {ticket_id}: 只有 {len(solutions)} 个方案提交，等待...")
        return
    
    # 选最佳：综合评分 = quality_score - cost_tokens/1000
    winner = max(solutions, key=lambda s: s["quality_score"] - s["cost_tokens"]/1000)
    loser = min(solutions, key=lambda s: s["quality_score"] - s["cost_tokens"]/1000)
    
    # 记录到进化日志
    data = load_evolution_data()
    round_entry = {
        "round_id": len(data["rounds"]) + 1,
        "ticket_id": ticket_id,
        "department": department,
        "submitted": datetime.datetime.now().isoformat(),
        "solutions": solutions,
        "winner": winner["team"],
        "loser": loser["team"],
        "comments": f"最优: {winner['name']} | 淘汰: {loser['name']}",
        "promoted_to_skill": True if winner["cost_tokens"] == 0 else False,
    }
    data["rounds"].append(round_entry)
    
    # 最佳方案入最佳实践库
    data["best_practices"].append({
        "origin": ticket_id,
        "problem": "",
        "approach": winner["approach"],
        "department": department,
        "created": datetime.datetime.now().isoformat(),
        "token_free": winner["cost_tokens"] == 0,
    })
    
    # 最差方案淘汰
    data["eliminated_approaches"].append({
        "team": loser["team"],
        "problem": "",
        "ticket_id": ticket_id,
        "reason": f"回溯对比得分最低",
        "eliminated_at": datetime.datetime.now().isoformat(),
    })
    
    save_evolution_data(data)
    
    # 清理任务文件
    for team_id in ["team1", "team2", "team3"]:
        task_file = dept_dir / f"task_{ticket_id}.json"
        if task_file.exists():
            os.remove(task_file)
    
    # 更新工单状态
    tickets_file = TEAMS_DIR / "pending_tickets.json"
    with open(tickets_file) as f:
        tickets = json.load(f)
    for t in tickets:
        if t["ticket_id"] == ticket_id:
            t["status"] = "resolved"
            t["three_day_review"] = {
                "winner": winner["team"],
                "loser": loser["team"],
                "completed": datetime.datetime.now().isoformat(),
            }
    with open(tickets_file, "w") as f:
        json.dump(tickets, f, indent=2, ensure_ascii=False)
    
    print(f"🏆 第{round_entry['round_id']}轮回溯完成: [{department}]")
    print(f"   最优: {winner['name']} (score={winner['quality_score']}, token={winner['cost_tokens']})")
    print(f"   淘汰: {loser['name']}")
    
    return True

# ============================================================
# 5. Token成本记录器
# ============================================================
def record_cost(ticket_id, department, team_id, tokens):
    """记录每一笔 token 消耗"""
    data = {"total_tokens": 0, "records": []}
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
    # 计算节约率
    data["saved_tokens"] = data.get("saved_tokens", 0) + (tokens * 3)  # 假设本地解决可省3倍
    data["savings_rate"] = round(
        data["saved_tokens"] / (data["total_tokens"] + data["saved_tokens"]) * 100, 1
    ) if data["total_tokens"] + data["saved_tokens"] > 0 else 0
    
    with open(COST_LOG, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return data["total_tokens"]

# ============================================================
# 6. 辅助函数
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
# 7. 全链路模拟推演
# ============================================================
def full_simulation():
    print("="*70)
    print("全自动进化闭环 - 完整推演")
    print("="*70)
    print()
    
    # Step 1: 看门狗发现异常
    print("🟢 [看门狗] 扫描到异常: caipiao1前端8088端口返回500")
    ticket_id = detect_and_create_ticket(
        watcher_name="caipiao1_watcher",
        problem_desc="caipiao1后端8088端口返回500，前端8502无法加载数据",
        department="frontend",
        severity="P1",
    )
    print()
    
    # Step 2: 派发到3个团队
    print("🟢 [派发] 工单到前端工程部3个团队")
    dispatch_to_teams(ticket_id, "frontend")
    print()
    
    # Step 3: 3个团队各自提交方案
    print("🟢 [团队] 3个团队开始解决...")
    print()
    
    # 方案1：先锋战队 - 纯本地
    submit_team_solution(
        ticket_id, "frontend", "team1",
        approach="用Playwright定位路由问题，发现是Python路径错误，已修复run_server.ps1",
        cost_tokens=0,
        quality_score=9,
    )
    
    # 方案2：优雅战队 - 也纯本地
    submit_team_solution(
        ticket_id, "frontend", "team2",
        approach="Vue3替代方案看了一遍，发现问题在配置不匹配，提供兼容脚本",
        cost_tokens=0,
        quality_score=7,
    )
    
    # 方案3：极速战队 - 本地+少量远程
    submit_team_solution(
        ticket_id, "frontend", "team3",
        approach="Hono快速重写了一个临时前端，但需要参考旧代码结构所以查了GitHub文档",
        cost_tokens=500,
        quality_score=8,
    )
    print()
    
    # Step 4: 回溯对比
    print("🟢 [回溯] 3天后自动对比...")
    print()
    auto_review_ticket(ticket_id, "frontend")
    print()
    
    # Step 5: 成本统计
    print("🟢 [成本] 当前token消耗统计")
    with open(COST_LOG) as f:
        cost_data = json.load(f)
    print(f"   已消耗token: {cost_data['total_tokens']}")
    print(f"   本地节约: {cost_data['saved_tokens']} token")
    print(f"   节约率: {cost_data['savings_rate']}%")
    print()
    
    print("="*70)
    print("✅ 全自动进化闭环推演完成")
    print("="*70)

if __name__ == "__main__":
    full_simulation()
