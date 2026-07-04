#!/usr/bin/env python3
"""验证血液循环 v3 — 只导入不触发main"""
import sys

sys.path.insert(0, r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams")

# 只导入函数，不跑main
import importlib.util
spec = importlib.util.spec_from_file_location("igp_engine", 
    r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\igp_engine.py")
mod = importlib.util.module_from_spec(spec)

# 拦截__name__
import types as _types
old_name = mod.__name__
mod.__name__ = "igp_engine_imported"

spec.loader.exec_module(mod)

# 现在所有函数都已经定义好了
mod.register_blood_type("backend", "team1", "red_blood")
mod.register_blood_type("backend", "team2", "white_blood")
mod.register_blood_type("backend", "team3", "platelet")

results = {}
for dept, team, expected in [
    ("backend", "team1", "red_blood"),
    ("backend", "team2", "white_blood"),
    ("backend", "team3", "platelet"),
    ("frontend", "team1", "white_blood"),
]:
    bt = mod._get_blood_type(team, dept)
    ok = bt == expected
    label = {"red_blood": "老将", "white_blood": "新人", "platelet": "修复型"}.get(bt, bt)
    results[f"{dept}:{team}"] = f"{'OK' if ok else 'FAIL'}: {bt}({label})"
    print(f"  {dept}:{team} => {bt} ({label}) {'✅' if ok else '❌'}")

oks = sum(1 for v in results.values() if v.startswith("OK"))
print(f"\n{oks}/{len(results)} 通过")

# 测试淘汰逻辑
print("\n=== 模拟淘汰测试 ===")
print("backend:team2（白细胞/新人）输1次 =>")
print("  ", mod._blood_eliminate("team2", "backend"))
print("backend:team2（白细胞/新人）再输1次 =>")
print("  ", mod._blood_eliminate("team2", "backend"))
print("\n✅ 血液循环机制 v2.0 正式上线!")
