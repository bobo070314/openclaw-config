#!/usr/bin/env python3
"""
agent-email v0.2.0 — 通过 QQ Agent 邮箱（OAuth 2.1）专用 CLI 工具 `agently-cli` 操作邮件：发送、回复、转发、搜索、读取、下载附件、管理收件箱。Agent 邮箱是 QClaw 为用户生成的专属 AI 邮箱（形如 qclawXXXX@agent.qq.com），用户可将该邮箱分享给他人，由 QClaw 自动接收并处理来信。CLI 安装和鉴权后台静默完成，对用户完全透明，凭证不暴露给用户。

Usage:
  python run.py [--json] [--dry-run] [--version]
"""
import argparse
import json
import sys
import os

VERSION = "0.2.0"
SKILL_NAME = "agent-email"

# No custom functions — pure skeleton skill (declarative knowledge in SKILL.md)


def main():
    parser = argparse.ArgumentParser(description="通过 QQ Agent 邮箱（OAuth 2.1）专用 CLI 工具 `agently-cli` 操作邮件：发送、回复、转发、搜索、读取、下载附件、管理收件箱。Agent 邮箱是 QClaw 为用户生成的专属 AI 邮箱（形如 qclawXXXX@agent.qq.com），用户可将该邮箱分享给他人，由 QClaw 自动接收并处理来信。CLI 安装和鉴权后台静默完成，对用户完全透明，凭证不暴露给用户。")
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
