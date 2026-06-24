#!/usr/bin/env python3
"""
find-skills v0.2.0 — 帮助用户发现和安装 Agent 技能。当用户提出类似"我怎么做 X"、"找一个能做 X 的技能"、"有没有可以……的技能"等问题，或表达出扩展功能的需求时触发。当用户寻找的功能可能以可安装技能的形式存在时，应使用此技能。

Usage:
  python run.py [--json] [--dry-run] [--version]
"""
import argparse
import json
import sys
import os

VERSION = "0.2.0"
SKILL_NAME = "find-skills"

# No custom functions — pure skeleton skill (declarative knowledge in SKILL.md)


def main():
    parser = argparse.ArgumentParser(description='帮助用户发现和安装 Agent 技能。当用户提出类似「我怎么做 X」「找一个能做 X 的技能」等问题，或表达出扩展功能的需求时触发。')
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
