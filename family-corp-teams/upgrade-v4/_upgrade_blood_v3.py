#!/usr/bin/env python3
"""修复血液循环 — 把函数定义移到文件末尾"""
import re

path = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\igp_engine.py"
with open(path, encoding="utf-8") as f:
    code = f.read()

# 1. 从原文件中删除末尾重复注入的代码（>=最后一个文件的末尾部分）
# 找到最后添加的"血液循环系统"部分
last_func_start = code.find("\n# ===== 血液循环系统 v2.0")
if last_func_start > 0:
    code = code[:last_func_start]
    print("[OK] 去掉了末尾重复注入")

# 2. 把 check_elimination 恢复为调用独立函数
old_check = """def check_elimination(loser_team, department):
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
    
    return False"""

# 用简单的旧版淘汰函数替换
new_check = """def check_elimination(loser_team, department):
    \"\"\"血液循环淘汰 v2.0 — 委托到独立模块\"\"\"
    return _blood_eliminate(loser_team, department)

def _blood_eliminate(loser_team, department):
    \"\"\"血液循环淘汰核心逻辑\"\"\"
    data = load_evolution_data()
    losses = []
    for r in data.get(\"eliminated_approaches\", []):
        if r.get(\"team\") == loser_team and r.get(\"department\") == department:
            losses.append(r)
    
    team_type = _get_blood_type(loser_team, department)
    dept_label = ALL_DEPARTMENTS.get(department, {}).get(\"label\", department)
    
    print(f\"  [BLOOD] {loser_team}@{dept_label} 血型={team_type} 本轮评分={losses[-1].get('score', 0) if losses else '?'}\")
    
    if team_type == \"platelet\":
        if losses and losses[-1].get(\"score\", 5) <= 2:
            print(f\"  [ELIM] 血小板\\u2192一次致命失误直接走人\")
            _blood_regen(loser_team, department, losses, team_type)
            return True
        return False
    
    if team_type == \"white_blood\":
        if len(losses) >= 2:
            print(f\"  [ELIM] 白细胞\\u2192新人撞两次墙，走人\")
            _blood_regen(loser_team, department, losses, team_type)
            return True
        if losses:
            print(f\"  [WARN] 白细胞警告：已输1次，再输1次走人！下次必须赢回来\")
        return False
    
    if team_type == \"red_blood\":
        if len(losses) >= 3:
            print(f\"  [ELIM] 红细胞\\u2192老将连续{len(losses)}次垫底，该退了\")
            _blood_regen(loser_team, department, losses, team_type)
            return True
        if losses:
            print(f\"  [WARN] 红细胞警告：已垫底{len(losses)}次，还剩{3 - len(losses)}次机会\")
        return False
    return False
"""

code = code.replace(old_check, new_check)

# 3. 在文件最末尾注入血型函数
code += """

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
    \"\"\"换血再生 — 新人默认白细胞\"\"\"
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
print("[OK] 写入成功")
