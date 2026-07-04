#!/usr/bin/env python3
"""IGP v4 终极演示入口"""
import sys, os, json

V4_DIR = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\upgrade-v4"
sys.path.insert(0, V4_DIR)

# 直接exec文件（保留__file__上下文）
exec(compile(open(os.path.join(V4_DIR, "v4_unified_engine.py"), encoding="utf-8").read(), 
             os.path.join(V4_DIR, "v4_unified_engine.py"), "exec"))

engine = V4UnifiedEngine()
result = engine.ultimate_demo()
print("\n" + result)

report = engine.generate_ultimate_report()
report_path = os.path.join(V4_DIR, "_v4_ultimate_report.json")
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print("\nReport: " + report_path)
print("Score: " + str(report["total_score"]) + "/10")
