#!/usr/bin/env python3
"""
reasoning-framework v0.2.0 — 三层推理框架：分解→执行→验证。封装 Sequential Thinking MCP 供复杂任务使用。依赖 MCP server `sequential-think`。

Usage:
  python run.py [--json] [--dry-run] [--version]
"""
import argparse
import json
import sys
import os

VERSION = "0.2.0"
SKILL_NAME = "reasoning-framework"

# No custom functions — pure skeleton skill (declarative knowledge in SKILL.md)


def main():
    parser = argparse.ArgumentParser(description="三层推理框架：分解→执行→验证。封装 Sequential Thinking MCP 供复杂任务使用。依赖 MCP server `sequential-think`。")
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
