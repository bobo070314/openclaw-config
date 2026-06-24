#!/usr/bin/env python3
"""
meituan-travel v0.2.0 — 基于美团酒旅供给，处理旅游出行需求，包括提供酒店、机火、门票、度假等商品的查询交易能力，以及定制化旅行攻略能力，打通从“灵感启发”到“一键下单”的全链路。

Usage:
  python run.py [--json] [--dry-run] [--version]
"""
import argparse
import json
import sys
import os

VERSION = "0.2.0"
SKILL_NAME = "meituan-travel"

# No custom functions — pure skeleton skill (declarative knowledge in SKILL.md)


def main():
    parser = argparse.ArgumentParser(description="基于美团酒旅供给，处理旅游出行需求，包括提供酒店、机火、门票、度假等商品的查询交易能力，以及定制化旅行攻略能力，打通从“灵感启发”到“一键下单”的全链路。")
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
