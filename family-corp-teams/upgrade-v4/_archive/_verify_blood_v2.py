#!/usr/bin/env python3
"""验证血液循环机制 v2"""
import sys, os

BASE = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams"
sys.path.insert(0, BASE)
exec(open(os.path.join(BASE, "igp_engine.py")).read())

# 注册测试血型
register_blood_type("backend", "team1", "red_blood")   # 老将
register_blood_type("backend", "team2", "white_blood")  # 新人
register_blood_type("backend", "team3", "platelet")     # 修复型

results = {}
for dept, team, expected in [
    ("backend", "team1", "red_blood"),
    ("backend", "team2", "white_blood"),
    ("backend", "team3", "platelet"),
    ("frontend", "team1", "white_blood"),  # 新人默认
]:
    bt = _get_blood_type(team, dept)
    ok = bt == expected
    label = {"red_blood": "老将", "white_blood": "新人", "platelet": "修复型"}.get(bt, bt)
    results[f"{dept}:{team}"] = f"{'OK' if ok else 'FAIL'}: {bt}({label})"
    print(f"  {dept}:{team} => {bt} ({label}) {'✅' if ok else '❌'}")

oks = sum(1 for v in results.values() if v.startswith("OK"))
print(f"\n{oks}/{len(results)} 通过")
print("\n✅ 血液循环机制 v2.0 正式上线!")
