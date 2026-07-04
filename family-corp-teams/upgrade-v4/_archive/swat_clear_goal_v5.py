#!/usr/bin/env python3
"""SWAT FINAL v2 — 找到并清除Goal"""
import json

fp = r"D:\\bobo\\openclaw-foreign\\state\agents\main\\sessions\\sessions.json"
data = json.load(open(fp, encoding="utf-8"))

main = data.get("agent:main:main", {})
# 打印所有的一级key
print("Top-level keys:", list(main.keys()))
# 找goal
goal = main.get("goal")
if goal:
    print("Goal found:")
    print(json.dumps(goal, ensure_ascii=False, indent=2))
    # 删除它
    del main["goal"]
    print("\nGoal deleted!")
    
    # 写回
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print("File saved!")
else:
    print("No top-level goal. Searching deeper...")
    # 找goal嵌套在哪里
    for k, v in main.items():
        if isinstance(v, dict) and "goal" in v:
            print(f"goal nested in {k}: {json.dumps(v['goal'])[:200]}")
        if isinstance(v, list):
            for item in v:
                if isinstance(item, dict) and "goal" in item:
                    print(f"goal in list {k}: {json.dumps(item['goal'])[:200]}")
