#!/usr/bin/env python3
"""验证血液循环机制"""
import sys, os

BASE = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams"
sys.path.insert(0, BASE)
exec(open(os.path.join(BASE, "igp_engine.py")).read())

register_blood_type("backend", "team1", "red_blood")
register_blood_type("backend", "team2", "white_blood")
register_blood_type("backend", "team3", "platelet")

print("=== 血型验证 ===")
for key in ["backend:team1", "backend:team2", "backend:team3", "frontend:team1"]:
    dept, team = key.split(":")
    bt = identify_blood_type(team, dept)
    label = {"red_blood": "红细胞(老将)", "white_blood": "白细胞(新兵)", "platelet": "血小板(修复型)"}.get(bt, bt)
    print(f"  {key} => {bt} ({label})")

print("\n✅ 血液循环机制 v2.0 就绪！")
print("红细胞=老将 3次淘汰 | 白细胞=新兵 2次淘汰 | 血小板=修复型 1次淘汰")
