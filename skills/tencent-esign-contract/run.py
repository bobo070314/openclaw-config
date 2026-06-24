#!/usr/bin/env python3
"""
tencent-esign-contract v0.2.0 — 腾讯电子签合同AI助手，支持合同起草、审查、对比、法条法规检索。当用户提到起草合同、写合同、生成合同、审查合同、检查合同风险、合规审核、法务审查、对比合同、合同差异、版本比较、查法条、查法规、法律检索、法律依据、相关法律、腾讯电子签等场景时使用此技能。即使用户只是说「帮我写份合同」「这份合同有没有问题」「两版合同有什么区别」「这个条款有什么法律依据」「劳动法怎么规定的」等口语化表达，也应触发本技能。

Usage:
  python run.py [--json] [--dry-run] [--version]
"""
import argparse
import json
import sys
import os

VERSION = "0.2.0"
SKILL_NAME = "tencent-esign-contract"

# No custom functions — pure skeleton skill (declarative knowledge in SKILL.md)


def main():
    parser = argparse.ArgumentParser(description="腾讯电子签合同AI助手，支持合同起草、审查、对比、法条法规检索。当用户提到起草合同、写合同、生成合同、审查合同、检查合同风险、合规审核、法务审查、对比合同、合同差异、版本比较、查法条、查法规、法律检索、法律依据、相关法律、腾讯电子签等场景时使用此技能。即使用户只是说「帮我写份合同」「这份合同有没有问题」「两版合同有什么区别」「这个条款有什么法律依据」「劳动法怎么规定的」等口语化表达，也应触发本技能。")
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
