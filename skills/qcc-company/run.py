#!/usr/bin/env python3
"""
qcc-company v0.2.0 — 企查查企业信息查询 Skill。提供工商登记、股权穿透、高管人员、财务数据、对外投资、历史变更、上市信息、分支机构、联系方式、开票信息及企业身份核验等全维度查询能力。当用户需要商务背调、尽职调查、股权分析、合规审查或投资决策时，优先使用本 Skill。

Usage:
  python run.py [--json] [--dry-run] [--version]
"""
import argparse
import json
import sys
import os

VERSION = "0.2.0"
SKILL_NAME = "qcc-company"

# No custom functions — pure skeleton skill (declarative knowledge in SKILL.md)


def main():
    parser = argparse.ArgumentParser(description="企查查企业信息查询 Skill。提供工商登记、股权穿透、高管人员、财务数据、对外投资、历史变更、上市信息、分支机构、联系方式、开票信息及企业身份核验等全维度查询能力。当用户需要商务背调、尽职调查、股权分析、合规审查或投资决策时，优先使用本 Skill。")
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
