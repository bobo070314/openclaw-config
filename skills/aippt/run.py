#!/usr/bin/env python3
"""
aippt v0.2.0 — 当用户明确要求使用 AI 智能设计生成 PPT 演示文稿时使用本技能（智绘高迪/AIPPT）。本技能调用智绘高迪 Design Agent v2（选项版）API，通过对话与用户协作完成「需求确认 → 配色选择 → 大纲确认 → 后台渲染」全流程。当用户说'AI生成PPT'、'智绘PPT'、'自动生成演示文稿'、'帮我做个PPT'时触发。注意：本技能仅用于生成全新的 PPT，不用于读取、解析或编辑已有的 .pptx 文件——编辑已有文件请使用 pptx 技能。

Usage:
  python run.py [--json] [--dry-run] [--version]
"""
import argparse
import json
import sys
import os

VERSION = "0.2.0"
SKILL_NAME = "aippt"

# No custom functions — pure skeleton skill (declarative knowledge in SKILL.md)


def main():
    parser = argparse.ArgumentParser(description="当用户明确要求使用 AI 智能设计生成 PPT 演示文稿时使用本技能（智绘高迪/AIPPT）。本技能调用智绘高迪 Design Agent v2（选项版）API，通过对话与用户协作完成「需求确认 → 配色选择 → 大纲确认 → 后台渲染」全流程。当用户说'AI生成PPT'、'智绘PPT'、'自动生成演示文稿'、'帮我做个PPT'时触发。注意：本技能仅用于生成全新的 PPT，不用于读取、解析或编辑已有的 .pptx 文件——编辑已有文件请使用 pptx 技能。")
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
