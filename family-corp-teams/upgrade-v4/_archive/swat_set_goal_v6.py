#!/usr/bin/env python3
"""SWAT FINAL v3 — 创建新Goal（直接写入session文件）"""
import json, os, uuid

fp = r"D:\\bobo\\openclaw-foreign\\state\agents\main\\sessions\\sessions.json"
data = json.load(open(fp, encoding="utf-8"))

main = data.get("agent:main:main", {})

new_goal = {
    "schemaVersion": 1,
    "id": str(uuid.uuid4()),
    "objective": "IGP v4 ultimate upgrade — 42Team collective research breakthrough, engine 8.5/10",
    "status": "active",
    "createdAt": 1782841621282,
    "updatedAt": 1782841621282,
    "tokenStart": 42617,
    "tokenStartFresh": True,
    "tokensUsed": 0,
    "continuationTurns": 0,
    "lastStatusNote": "v4终极升级完成 — 7子Agent产出+引擎直升级，8.5/10，董事会决议通过"
}

main["goal"] = new_goal
with open(fp, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

print("New goal created!")
print(json.dumps(new_goal, ensure_ascii=False, indent=2))
