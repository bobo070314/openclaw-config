#!/usr/bin/env python3
"""
wechat-topic-outline-planner v0.2.0 — 公众号选题与大纲策划技能。用于把一个粗点子、资料包、语音底稿或采访纪要，转成 2-3 个高价值选题角度、1 个推荐方向、1 套主大纲和 1 套备选大纲。适用于写作前的方案阶段，必须先确认结构，再交给写稿技能。

Usage:
  python run.py [--json] [--dry-run] [--version]
"""
import argparse
import json
import sys
import os

VERSION = "0.2.0"
SKILL_NAME = "wechat-topic-outline-planner"

# No custom functions — pure skeleton skill (declarative knowledge in SKILL.md)


def main():
    parser = argparse.ArgumentParser(description="公众号选题与大纲策划技能。用于把一个粗点子、资料包、语音底稿或采访纪要，转成 2-3 个高价值选题角度、1 个推荐方向、1 套主大纲和 1 套备选大纲。适用于写作前的方案阶段，必须先确认结构，再交给写稿技能。")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--dry-run", action="store_true", help="Preview mode")
    parser.add_argument("--version", action="store_true", help="Show version")
    args = parser.parse_args()

    if args.version:
        print(json.dumps({"skill": SKILL_NAME, "version": VERSION, "status": "live"}, indent=2))
        return 0

    info = {"skill": SKILL_NAME, "version": VERSION, "status": "live"}

    if args.dry_run:
        info["dry_run"] = True
        info["note"] = "Dry run — skeleton skill, no side effects."
        print(json.dumps(info, indent=2))
        return 0

    info["note"] = "Skeleton skill — functionality defined in SKILL.md"

    print(json.dumps(info, indent=2) if args.json else json.dumps(info, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
