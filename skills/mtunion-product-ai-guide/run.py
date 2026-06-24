#!/usr/bin/env python3
"""
mtunion-product-ai-guide v0.2.0 — 美团优惠下单助手。当你想吃饭、找餐厅、买团购券、喝咖啡、喝奶茶、找饮品、吃快餐、吃火锅、吃烧烤、吃日料、吃川菜、吃自助餐、找下午茶、附近有什么好吃的好喝的，只需告诉我想吃什么喝什么或在哪附近找，我会自动帮你领券、搜索商品、展示图文列表，选好后直接帮你下单。我也可以单独帮你领优惠券、领券、领红包、领神券、领专属红包、薅羊毛、领优惠、美团省钱，为你推荐各类爆品会场。全程在对话中完成，无需切换应用。

Usage:
  python run.py [--json] [--dry-run] [--version]
"""
import argparse
import json
import sys
import os

VERSION = "0.2.0"
SKILL_NAME = "mtunion-product-ai-guide"

# No custom functions — pure skeleton skill (declarative knowledge in SKILL.md)


def main():
    parser = argparse.ArgumentParser(description="美团优惠下单助手。当你想吃饭、找餐厅、买团购券、喝咖啡、喝奶茶、找饮品、吃快餐、吃火锅、吃烧烤、吃日料、吃川菜、吃自助餐、找下午茶、附近有什么好吃的好喝的，只需告诉我想吃什么喝什么或在哪附近找，我会自动帮你领券、搜索商品、展示图文列表，选好后直接帮你下单。我也可以单独帮你领优惠券、领券、领红包、领神券、领专属红包、薅羊毛、领优惠、美团省钱，为你推荐各类爆品会场。全程在对话中完成，无需切换应用。")
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
