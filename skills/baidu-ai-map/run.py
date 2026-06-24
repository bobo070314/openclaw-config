#!/usr/bin/env python3
"""
baidu-ai-map v0.2.0 — 百度地图 Agent Plan ，无需成为百度地图开发者，立即接入百度地图为 Agent 场景原生设计的地图能力，例如 AI 地点检索、AI 路线规划、地理编码与逆地理编码、天气查询、地图展示等开箱即用的工具。

Usage:
  python run.py [--json] [--dry-run] [--version]
"""
import argparse
import json
import sys
import os

VERSION = "0.2.0"
SKILL_NAME = "baidu-ai-map"

# No custom functions — pure skeleton skill (declarative knowledge in SKILL.md)


def main():
    parser = argparse.ArgumentParser(description="百度地图 Agent Plan ，无需成为百度地图开发者，立即接入百度地图为 Agent 场景原生设计的地图能力，例如 AI 地点检索、AI 路线规划、地理编码与逆地理编码、天气查询、地图展示等开箱即用的工具。")
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
