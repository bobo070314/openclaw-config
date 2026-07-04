#!/usr/bin/env python3
"""精确替换igp_engine.py中的淘汰函数 v2.0"""
import re, sys

path = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\igp_engine.py"
with open(path, encoding="utf-8") as f:
    code = f.read()

# 1. 替换 check_elimination 函数
old_ce_start = "def check_elimination(loser_team, department):"
old_ce_end = "# ════════════════════════════════════════════════════════\n# 4. 淘汰与再生"

idx_start = code.find(old_ce_start)
idx_end = code.find(old_ce_end)
if idx_start < 0 or idx_end < 0:
    print(f"[FAIL] 找不到check_elimination函数边界")
    sys.exit(1)

new_check_elim = """def check_elimination(loser_team, department):
    \"\"\"血液循环淘汰机制 v2.0
    
    三血模型：
    - 红细胞（老将）：连续3次垫底→淘汰（有经验值得多一次机会）
    - 白细胞（新兵）：连续2次垫底→淘汰（新人敢冲撞两次墙就走）
    - 血小板（修复型）：1次致命失误→直接淘汰（专治烂摊子的，修不好就滚）
    \"\"\"
    data = load_evolution_data()
    losses = []
    for r in data.get("eliminated_approaches", []):
        if r.get("team") == loser_team and r.get("department") == department:
            losses.append(r)
    
    team_type = identify_blood_type(loser_team, department)
    dept_label = ALL_DEPARTMENTS.get(department, {}).get("label", department)
    
    print(f"  [BLOOD] {loser_team}@{dept_label} 血型={team_type} 本轮评分={losses[-1].get('score', 0) if losses else '?'}")
    
    # ⚡ 血小板模式：一次致命失误直接滚
    if team_type == "platelet":
        if losses and losses[-1].get("score", 5) <= 2:
            print(f"  [ELIM] 血小板→一次致命失误直接走人")
            trigger_regeneration(loser_team, department, losses, team_type)
            return True
        return False
    
    # ⚡ 白细胞模式：连续2次垫底走人
    if team_type == "white_blood":
        if len(losses) >= 2:
            print(f"  [ELIM] 白细胞→新人撞两次墙，走人")
            trigger_regeneration(loser_team, department, losses, team_type)
            return True
        if losses:
            print(f"  [WARN] 白细胞警告：已输1次，再输1次走人！下次必须赢回来")
        return False
    
    # ⚡ 红细胞模式（老将）：连续3次垫底才淘汰
    if team_type == "red_blood":
        if len(losses) >= 3:
            print(f"  [ELIM] 红细胞→老将连续{len(losses)}次垫底，该退了")
            trigger_regeneration(loser_team, department, losses, team_type)
            return True
        if losses:
            print(f"  [WARN] 红细胞警告：已垫底{len(losses)}次，还剩{3 - len(losses)}次机会")
        return False
    
    return False
"""

code = code[:idx_start] + new_check_elim + code[idx_end:]

# 2. 替换 trigger_regeneration
old_tr_start = "def trigger_regeneration(loser_team, department, loss_history):"
old_tr_end = "def suggest_new_tool_stack(department):"
idx_tr_start = code.find(old_tr_start)
idx_tr_end = code.find(old_tr_end)
if idx_tr_start < 0 or idx_tr_end < 0:
    print(f"[FAIL] 找不到trigger_regeneration边界")
    sys.exit(1)

new_trigger = """def trigger_regeneration(loser_team, department, loss_history, blood_type="white_blood"):
    \"\"\"团队解散→重组流程 — 换上新血（默认白细胞 敢冲敢闯）\"\"\"
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
    
    print(f"   [OK] {blood_type}换血完成 \\u2192 新人(白细胞)上任!")
    print(f"   [IN] 新工具栈: {new_tool_stack}")
    print(f"   [CREED] 新人宣言：敢冲敢闯，输了就走，赢了就留")
"""

code = code[:idx_tr_start] + new_trigger + code[idx_tr_end:]

# 3. 替换 suggest_new_tool_stack
old_sns_start = "def suggest_new_tool_stack(department):"
idx_sns_start = code.find(old_sns_start)
idx_sep_next = code.find("\n\n", idx_sns_start + 50)
if idx_sns_start < 0:
    print(f"[FAIL] 找不到suggest_new_tool_stack")
    sys.exit(1)

new_suggest = """def suggest_new_tool_stack(department):
    \"\"\"动态推荐新工具栈 — 从观察池优先，无则fallback\"\"\"
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
"""

code = code[:idx_sns_start] + new_suggest + code[idx_sep_next:]

# 4. 注入血型识别函数
code += """

# ===== 血液循环系统 v2.0 — 血型注册与识别 =====
import functools

_blood_types = {}  # "department:team" -> "red_blood" | "white_blood" | "platelet"

def register_blood_type(department, team_id, blood_type):
    \"\"\"注册团队血型。红=老将 白=新兵 血=修复型\"\"\"
    _blood_types[f"{department}:{team_id}"] = blood_type
    return blood_type

@functools.lru_cache(maxsize=256)
def identify_blood_type(team_id, department):
    \"\"\"识别血型。无注册默认为白细胞（鼓励主动出击）\"\"\"
    cached = _blood_types.get(f"{department}:{team_id}")
    if cached:
        return cached
    # 查询历史贡献：有最佳实践记录算红细胞
    data = load_evolution_data()
    for bp in data.get("best_practices", []):
        if bp.get("team") == team_id and bp.get("department") == department:
            _blood_types[f"{department}:{team_id}"] = "red_blood"
            return "red_blood"
    # 默认白细胞：新人敢冲敢闯，允许犯错但不会无限容忍
    _blood_types[f"{department}:{team_id}"] = "white_blood"
    return "white_blood"
"""

try:
    compile(code, path, "exec")
    print("[OK] 编译通过")
except SyntaxError as e:
    print(f"[FAIL] 编译失败 line {e.lineno}: {e.msg}")
    lines = code.splitlines()
    for i in range(max(0, e.lineno-3), min(len(lines), e.lineno+2)):
        print(f"  {i+1}: {lines[i][:120]}")
    sys.exit(1)

with open(path, "w", encoding="utf-8") as f:
    f.write(code)
print("[OK] igp_engine.py 血液循环机制升级完成")
