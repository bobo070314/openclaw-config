#!/usr/bin/env python3
"""血液循环淘汰机制升级 — 替换igp_engine.py中的淘汰函数"""
import re

path = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\igp_engine.py"
with open(path, encoding="utf-8") as f:
    code = f.read()

# 1. 替换 suggest_new_tool_stack
old_alternatives = '''    alternatives = {
        "frontend": "Solid.js / Qwik / Astro",
        "backend": "Bun / Elysia / PocketBase",
        "infrastructure": "Nomad / Coolify / Coolify",'''

new_alternatives = '''    # 取代旧的硬编码alternatives
    alternatives = _get_dynamic_tool_stack(department)'''

code = code.replace(old_alternatives, new_alternatives)

# 2. 在文件末尾注入新的三血模型函数和identify_blood_type
injection = '''

# ===== 血液循环淘汰机制 v2.0（2026-07-01）=====
# 三血模型：红细胞(老将)/白细胞(新兵)/血小板(修复型)

# Team血型注册表 — 记录每个Team的"血液类型"
_blood_types = {}  # {"department:team": "red_blood" | "white_blood" | "platelet"}

def register_blood_type(department, team_id, blood_type):
    """注册Team的血型。红细胞=老将，白细胞=新兵，血小板=修复型"""
    key = f"{department}:{team_id}"
    _blood_types[key] = blood_type
    return blood_type

def identify_blood_type(team_id, department):
    """判断血型。无注册默认为白细胞（新兵），鼓励冲劲"""
    key = f"{department}:{team_id}"
    bt = _blood_types.get(key)
    if bt:
        return bt
    # 检查是否在最佳实践中有记录（有历史的算老将）
    data = load_evolution_data()
    for bp in data.get("best_practices", []):
        if bp["team"] == team_id and bp["department"] == department:
            # 有历史贡献 → 红细胞
            _blood_types[key] = "red_blood"
            return "red_blood"
    # 新人 → 白细胞（敢冲敢闯，但犯错两次走人）
    _blood_types[key] = "white_blood"
    return "white_blood"

def check_elimination_v2(loser_team, department):
    """血液循环淘汰 v2.0
    
    三血模型：
    - 红细胞（老将）：连续3次垫底→淘汰（有经验值得多一次机会）
    - 白细胞（新兵）：连续2次垫底→淘汰（新人敢冲撞两次墙就走）
    - 血小板（修复型）：1次致命失误→直接淘汰（专治烂摊子的，修不好就滚）
    """
    data = load_evolution_data()
    losses = []
    for r in data.get("eliminated_approaches", []):
        if r.get("team") == loser_team and r.get("department") == department:
            losses.append(r)
    
    team_type = identify_blood_type(loser_team, department)
    dept_label = ALL_DEPARTMENTS.get(department, {}).get("label", department)
    
    print(f"  🩸 {loser_team}@{dept_label} 血型={team_type} 本轮评分={losses[-1].get('score', 0) if losses else '?'}")
    
    # 血小板模式：一次致命失误直接滚
    if team_type == "platelet":
        if losses and losses[-1].get("score", 5) <= 2:
            print(f"  🔥 血小板→一次致命失误直接走人")
            trigger_regeneration_v2(loser_team, department, losses, team_type)
            return True
        return False
    
    # 白细胞模式：连续2次垫底走人
    if team_type == "white_blood":
        if len(losses) >= 2:
            print(f"  🔥 白细胞→新人撞两次墙，走人")
            trigger_regeneration_v2(loser_team, department, losses, team_type)
            return True
        # 第一次垫底：给警告
        if len(losses) >= 1:
            print(f"  📢 白细胞警告：已输1次，再输1次走人！下次必须赢回来")
        return False
    
    # 红细胞模式（老将）：连续3次垫底才淘汰
    if team_type == "red_blood":
        if len(losses) >= 3:
            print(f"  🔥 红细胞→老将连续3次垫底，该退了")
            trigger_regeneration_v2(loser_team, department, losses, team_type)
            return True
        # 警告
        if len(losses) >= 1:
            print(f"  📢 红细胞警告：已垫底{len(losses)}次，还剩{3 - len(losses)}次机会")
        return False
    
    return False

def trigger_regeneration_v2(loser_team, department, loss_history, blood_type):
    """团队解散→重组流程 v2 — 换上新人（白细胞）"""
    from pathlib import Path
    TEAMS_DIR = Path(r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams")
    
    regen_file = TEAMS_DIR / "regeneration_log.json"
    regen_data = []
    if regen_file.exists():
        with open(regen_file, encoding="utf-8") as f:
            regen_data = json.load(f)
    
    new_tool_stack = _get_dynamic_tool_stack(department)
    
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
    
    # 新人直接注册为白细胞（敢闯型）
    register_blood_type(department, loser_team, "white_blood")
    
    print(f"  ✅ {blood_type}换血完成 → 新人(白细胞)上任!")
    print(f"  📥 新工具栈: {new_tool_stack}")
    print(f"  🗣️  新人宣言：敢冲敢闯，输了就走，赢了就留")

def _get_dynamic_tool_stack(department):
    """动态推荐新工具栈 — 从观察池或GitHub趋势"""
    from datetime import datetime
    
    # 从观察池取，没有就用静态fallback
    pool_path = Path(r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\new_tools_pool.json")
    if pool_path.exists():
        try:
            pool = json.load(open(pool_path, encoding="utf-8"))
            candidates = pool.get("candidates", [])
            if candidates:
                # 取最新的3个候选
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

# 替换旧函数（保持向后兼容）
check_elimination = check_elimination_v2
trigger_regeneration = trigger_regeneration_v2
# 保持suggest_new_tool_stack兼容接口
suggest_new_tool_stack = _get_dynamic_tool_stack
'''

code += injection

# 验证
try:
    compile(code, path, "exec")
    print("[OK] 编译通过")
except SyntaxError as e:
    print(f"[FAIL] 编译失败: {e}")
    # 尝试找到具体问题
    for i, line in enumerate(code.splitlines()):
        if "SyntaxError" in str(e) and str(e).split("line")[-1].strip().startswith(str(i+1)):
            print(f"  问题行 {i+1}: {line[:100]}")
    sys.exit(1)

with open(path, "w", encoding="utf-8") as f:
    f.write(code)
print("[OK] igp_engine.py 血液循环机制升级完成!")
