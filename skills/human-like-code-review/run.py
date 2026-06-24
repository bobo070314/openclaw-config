#!/usr/bin/env python3
"""
human-like-code-review v0.2.0 — 类人代码审查 - AI模拟人类审查风格，关注逻辑、可读性和架构而非格式

Usage:
  python run.py [--json] [--dry-run] [--version]
"""
import argparse
import json
import sys
import os

VERSION = "0.2.0"
SKILL_NAME = "human-like-code-review"

# No custom functions — pure skeleton skill (declarative knowledge in SKILL.md)


def main():
    parser = argparse.ArgumentParser(description="类人代码审查 - AI模拟人类审查风格，关注逻辑、可读性和架构而非格式")
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
