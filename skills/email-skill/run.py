#!/usr/bin/env python3
"""
email-skill v0.2.0 — 邮件统一入口（纯路由层），自身不执行任何脚本与接口，识别用户意图后用 read 工具读取下游 skill 的 SKILL.md 路由到下游。【路由决策必读】两步决策：L0 用户是否显式指定邮箱通道？L1 若未指定，是发给自己/结果留存还是发给别人/完整收发？L0 显式：'Agent/AI 邮箱'→读取 agent-email/SKILL.md；'用我的 QQ/163/Gmail/Outlook'→读取 imap-smtp-email/SKILL.md；'发到我邮箱/推到我邮箱/保存到邮箱'→读取 public-skill/SKILL.md。L0 未指定 → L1：发给自己/结果留存→读取 public-skill/SKILL.md；发给别人/完整收发→读取 personal-mail-skill/SKILL.md。绝不在 read 工具读取 SKILL.md 之前向用户追问账号选择，由系统拦截层统一处理。

Usage:
  python run.py [--json] [--dry-run] [--version]
"""
import argparse
import json
import sys
import os

VERSION = "0.2.0"
SKILL_NAME = "email-skill"

# No custom functions — pure skeleton skill (declarative knowledge in SKILL.md)


def main():
    parser = argparse.ArgumentParser(description="邮件统一入口（纯路由层），自身不执行任何脚本与接口，识别用户意图后用 read 工具读取下游 skill 的 SKILL.md 路由到下游。【路由决策必读】两步决策：L0 用户是否显式指定邮箱通道？L1 若未指定，是发给自己/结果留存还是发给别人/完整收发？L0 显式：'Agent/AI 邮箱'→读取 agent-email/SKILL.md；'用我的 QQ/163/Gmail/Outlook'→读取 imap-smtp-email/SKILL.md；'发到我邮箱/推到我邮箱/保存到邮箱'→读取 public-skill/SKILL.md。L0 未指定 → L1：发给自己/结果留存→读取 public-skill/SKILL.md；发给别人/完整收发→读取 personal-mail-skill/SKILL.md。绝不在 read 工具读取 SKILL.md 之前向用户追问账号选择，由系统拦截层统一处理。")
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
