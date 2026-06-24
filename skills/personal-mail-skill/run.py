#!/usr/bin/env python3
"""
personal-mail-skill v0.2.0 — 个人邮箱二级路由层。仅在 email-skill 把任务转发到本 skill 后被调用——典型场景是『发给别人 / 需要附件 / 抄送 / 收件箱搜索 / 下载附件』等完整收发需求。本 skill 通过执行路由脚本确定性地决定路由到 agent-email 或 imap-smtp-email，然后立即用 read 工具读取目标 SKILL.md 执行邮件操作。

Usage:
  python run.py [--json] [--dry-run] [--version]
"""
import argparse
import json
import sys
import os

VERSION = "0.2.0"
SKILL_NAME = "personal-mail-skill"

# No custom functions — pure skeleton skill (declarative knowledge in SKILL.md)


def main():
    parser = argparse.ArgumentParser(description="个人邮箱二级路由层。仅在 email-skill 把任务转发到本 skill 后被调用——典型场景是『发给别人 / 需要附件 / 抄送 / 收件箱搜索 / 下载附件』等完整收发需求。本 skill 通过执行路由脚本确定性地决定路由到 agent-email 或 imap-smtp-email，然后立即用 read 工具读取目标 SKILL.md 执行邮件操作。")
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
