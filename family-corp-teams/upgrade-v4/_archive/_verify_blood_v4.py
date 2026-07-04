#!/usr/bin/env python3
"""验证血液循环 v4 — 直接exec，但加个标记不跑main"""
import sys

sys.path.insert(0, r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams")

# 设置标记阻止__main__执行
import __main__
__main__.__igp_imported_as_module = True

exec(open(r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\igp_engine.py", encoding="utf-8").read())

register_blood_type("backend", "team1", "red_blood")
register_blood_type("backend", "team2", "white_blood")
register_blood_type("backend", "team3", "platelet")

results = {}
for dept, team, expected in [
    ("backend", "team1", "red_blood"),
    ("backend", "team2", "white_blood"),
    ("backend", "team3", "platelet"),
    ("frontend", "team1", "white_blood"),
]:
    bt = _get_blood_type(team, dept)
    ok = bt == expected
    label = {"red_blood": "老将", "white_blood": "新人", "platelet": "修复型"}.get(bt, bt)
    print(f"  {dept}:{team} => {bt} ({label}) {'OK' if ok else 'FAIL'}")
    results[f"{dept}:{team}"] = ok

oks = sum(1 for v in results.values() if v)
print(f"\n{oks}/{len(results)} 通过")

# 模拟淘汰
print("\n=== 模拟淘汰 ===")
print("新人 team2 输1次 =>", _blood_eliminate("team2", "backend"))
print("新人 team2 再输1次 =>", _blood_eliminate("team2", "backend"))

print("\n=== 血液循环机制 v2.0 就绪 ===")
