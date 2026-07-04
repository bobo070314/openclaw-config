#!/usr/bin/env python3
"""SWAT FINAL — 直接修改sessions.json清Goal"""
import json, os

fp = r"D:\\bobo\\openclaw-foreign\\state\agents\main\\sessions\\sessions.json"
data = json.load(open(fp, encoding="utf-8"))

current_id = "180247f2-8462-4674-b396-c82e35571ddf"

def find_key(obj, target, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            if target in p or target in k:
                return p, v
            r = find_key(v, target, p)
            if r:
                return r
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            r = find_key(v, target, f"{path}[{i}]")
            if r:
                return r
    return None

# 先用一层遍历找session
session_entry = None
if isinstance(data, list):
    for s in data:
        if s.get("id") == current_id or s.get("sessionId") == current_id:
            session_entry = s
            break
elif isinstance(data, dict):
    session_entry = data.get(current_id)
    if not session_entry:
        session_entry = data.get("sessions", {}).get(current_id)

if session_entry:
    print("Found session entry, type:", type(session_entry).__name__)
    # 逐层检查goal
    def find_goal_keys(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                p = f"{path}.{k}" if path else k
                if "goal" in k.lower():
                    print(f"GOAL FOUND at {p}: {json.dumps(v, ensure_ascii=False)[:200]}")
                find_goal_keys(v, p)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                find_goal_keys(v, f"{path}[{i}]")
    find_goal_keys(session_entry)
else:
    # 搜索全部
    print("Searching all entries for goal...")
    if isinstance(data, list):
        for s in data:
            s_str = json.dumps(s)
            if '"goal"' in s_str or '"goals"' in s_str or "'goal'" in s_str:
                sid = s.get("id", s.get("sessionId", "?"))
                print(f"\nSession {sid} has goal:")
                # 打印前500字符
                print(json.dumps(s, ensure_ascii=False)[:500])
    elif isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                v_str = json.dumps(v)
                if '"goal"' in v_str or '"goals"' in v_str:
                    print(f"Key {k} has goal (first 500 chars):")
                    print(v_str[:500])
