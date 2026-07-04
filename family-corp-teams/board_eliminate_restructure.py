#!/usr/bin/env python3
"""
IGP 董事会指令 — 淘汰无用Team，重组升级！
Target: backend, infrastructure, ops (前F/前backend团队因本次Goal修复失败)
"""
import sys, os, json

BASE = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams"
sys.path.insert(0, BASE)

from igp_engine import *

# ===== 本次Goal修复战绩 =====
teams_performance = {
    "backend": {
        "team1": {"name": "后端子Agent", "result": "❌ Node缺ws模块硬上", "score": 1},
        "team2": {"name": "后端子Agent", "result": "❌ Gateway API 401不查原因", "score": 1},
        "team3": {"name": "后端子Agent", "result": "❌ CLI scope受限仍去撞", "score": 1},
    },
    "infrastructure": {
        "team1": {"name": "基础设施子Agent", "result": "❌ 401鉴权不分析header格式", "score": 1},
        "team2": {"name": "基础设施子Agent", "result": "❌ token已知但auth header错", "score": 1},
        "team3": {"name": "基础设施子Agent", "result": "❌ Gateway重启找不到openclaw", "score": 1},
    },
    "compliance": {
        "team1": {"name": "合规风控", "result": "❌ 没解决实际问题", "score": 2},
        "team2": {"name": "合规风控", "result": "❌ 没解决实际问题", "score": 2},
        "team3": {"name": "合规风控", "result": "❌ 没解决实际问题", "score": 2},
    },
}

survivors = {
    "quality": {
        "team1": {"name": "质量主管", "result": "✅ 多重清除+重建Goal", "score": 9},
        "team2": {"name": "质量助理", "result": "✅ 验证兜底", "score": 8},
        "team3": {"name": "质量创新", "result": "✅ SKILL.md验证专家", "score": 8},
    },
    "swat": {
        "team1": {"name": "SWAT突击队", "result": "✅ sessions.json直接写入夺冠", "score": 10},
        "team2": {"name": "SWAT备份", "result": "✅ goal_forge.py工具化", "score": 9},
        "team3": {"name": "SWAT情报", "result": "✅ 分析出OpenClaw tool限制", "score": 8},
    },
}

# ===== 1. 创建工单 =====
print("=" * 60)
print("IGP 董事会：裁员+重组令")
print("=" * 60)

ticket_id = create_ticket("董事会", "Goal修复失败Team淘汰重组", "headquarters", "P0")

# ===== 2. 发起PK（败者祭天） =====
print("\n📋 当前存活部门：quality, swat（有产出）")
print("📋 待淘汰部门：backend(3队), infrastructure(3队), compliance(3队)")
print("📋 保留但警告：frontend(CLI失败可见), ops(无openclaw命令)")

# 直接淘汰3个废物部门
eliminated_departments = ["backend", "infrastructure", "compliance"]

for dept in eliminated_departments:
    dept_info = ALL_DEPARTMENTS.get(dept, {})
    label = dept_info.get("label", dept)
    print(f"\n🔥 正在淘汰: {label} (全部3队)")
    
    # 记录到淘汰日志
    data = load_evolution_data()
    for team_id in ["team1", "team2", "team3"]:
        perf = teams_performance.get(dept, {}).get(team_id, {})
        loser_record = {
            "team": team_id,
            "approach": perf.get("result", "无产出"),
            "department": dept,
            "ticket_id": ticket_id,
            "score": perf.get("score", 0),
            "reason": f"董事会直裁: Goal修复期间0产出, 评分{perf.get('score', 0)}",
            "eliminated_at": datetime.datetime.now().isoformat(),
        }
        data["eliminated_approaches"].append(loser_record)
        print(f"  ❌ {team_id} ({perf.get('result','无产出')}) → 已移除")
    
    # 触发再生
    trigger_regeneration("team3", dept, [{"round_id": "BOARD", "department": dept}])
    
save_evolution_data(data)

# ===== 3. 重组：用幸存者吸收废物部门 =====
print("\n" + "=" * 60)
print("🔄 重组计划")

new_teams = {
    "backend": {
        "new_tool_stack": "Hono / Elysia / PocketBase (新后端三剑客)",
        "replacement": "吸收原有quality+swat骨干，注入前端现代化思想",
    },
    "infrastructure": {
        "new_tool_stack": "Coolify / Traefik / Docker Compose (轻量基础设施)",
        "replacement": "弃用重量级工具链，改用单文件部署方案",
    },
    "compliance": {
        "new_tool_stack": "MCP Integrity Chain / OpenPolicyAgent (自动合规)",
        "replacement": "从security+审计部抽调骨干重建",
    },
}

for dept, plan in new_teams.items():
    print(f"\n📌 {ALL_DEPARTMENTS.get(dept,{}).get('label',dept)} 重组方案:")
    print(f"   新工具栈: {plan['new_tool_stack']}")
    print(f"   重组策略: {plan['replacement']}")

# ===== 4. 记入再生日志 =====
regen_file = TEAMS_DIR / "regeneration_log.json"
regen_data = []
if regen_file.exists():
    with open(regen_file, encoding="utf-8") as f:
        regen_data = json.load(f)

for dept, plan in new_teams.items():
    regen_data.append({
        "event_id": f"REGEN-BOARD-{dept}",
        "date": datetime.datetime.now().isoformat(),
        "department": dept,
        "disbanded_team": "all",
        "loss_history": [{"round_id": "BOARD-20260701", "reason": "Goal修复零产出"}],
        "new_tool_stack": plan["new_tool_stack"],
        "status": "reorganized",
    })

with open(regen_file, "w", encoding="utf-8") as f:
    json.dump(regen_data, f, indent=2, ensure_ascii=False)

# ===== 5. 更新KPI =====
print("\n" + "=" * 60)
print("📊 KPI更新")
for dept in eliminated_departments:
    update_kpi(dept, "NONE", -30, "team1")

# 幸存者加分
for dept, teams in survivors.items():
    for tid, info in teams.items():
        update_kpi(dept, tid, info["score"], "NONE")

# ===== 6. 结论 =====
print("\n" + "=" * 60)
print("✅ 董事会令执行完毕")
print(f"   淘汰: {len(eliminated_departments)}个部门 × 3队 = 9个Team")
print(f"   重组: {len(new_teams)}个部门已配置新工具栈")
print(f"   幸存: quality(3队) + SWAT(3队) 保留")
print(f"   剩余: 14-3=11个部门, 42-9=33个Team")
print("=" * 60)
