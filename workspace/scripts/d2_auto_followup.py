#!/usr/bin/env python3
"""
d2_auto_followup.py — Match customer reply and select appropriate followup.

Triggers:
  - "interested" / "demo" / "看看" / "有空" → Scenario A: arrange 15min demo
  - "什么" / "怎么用" / "复杂" / "了解" → Scenario B: pitch pain points
  - "忙" / "之后" / "再说" / "考虑" → Scenario C: defer to D2
  - Anything else (or no reply) → Scenario C (defer)

Usage:
    python scripts/d2_auto_followup.py --reply "<customer message>" [--dry-run]
"""

import argparse, sys, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


SCENARIOS = {
    "A": {
        "keywords": ["interested", "demo", "看看", "有空", "有兴趣", "行", "好"],
        "response": (
            "好的，那这周安排 15 分钟演示。\n"
            "您什么时候方便？我直接给您跑一遍整个流程。"
        ),
    },
    "B": {
        "keywords": ["什么", "怎么用", "复杂", "了解", "详细", "具体", "说明"],
        "response": (
            "一句话说就是：配置错了/文件丢了/权限乱了 → 系统自动修，修不上自动回滚。\n"
            "您可以直接跑 `python scripts/auto_fixer_demo.py` 看效果，不到 10 秒。"
        ),
    },
    "C": {
        "keywords": ["忙", "之后", "再说", "考虑", "没时间", "再看看", "不需要", "没兴趣", "不用了", "不必"],
        "response": (
            "没事，资料先放着。您忙完了随时说。\n"
            "这版系统的自动修复能力已经过 50 项测试全面验证。\n"
            "如果您或团队之后想试试效果，跑两行命令：\n"
            "  python scripts/auto_fixer_demo.py\n"
            "\n"
            "如果之后有团队在做相关的事，帮我们搭个线就好。"
        ),
    },
}


def classify(reply: str) -> tuple[str, list[str]]:
    """Classify reply into scenario, return (scenario_letter, matched_keywords_list)."""
    reply_lower = reply.lower()
    for scenario, config in SCENARIOS.items():
        matched_keywords = []
        for kw in config["keywords"]:
            if kw.lower() in reply_lower:
                matched_keywords.append(kw)
        if matched_keywords:
            return scenario, matched_keywords

    return "C", []


def followup(reply: str, dry_run: bool = False) -> dict:
    scenario, matched_kws = classify(reply)
    response_text = SCENARIOS[scenario]["response"]
    matched_at = datetime.now(timezone.utc).isoformat()
    primary_kw = matched_kws[0] if matched_kws else "no_match"

    result = {
        "matched_at": matched_at,
        "customer_reply": reply,
        "scenario": f"Scenario {scenario}",
        "matched_keyword": primary_kw,
        "keywords_matched": matched_kws,
        "response_text": response_text,
    }

    if dry_run:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"\n⏸️  Dry run — response above is draft only.")
    else:
        # Log to centralized jsonl
        log_path = ROOT / "data" / "runs" / "d2_followup_log.jsonl"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")

        # Archive individual reply with timestamp
        archive_dir = ROOT / "logs" / "d2_replies"
        archive_dir.mkdir(parents=True, exist_ok=True)
        safe_s = "".join(c if c.isalnum() or c in "-_" else "_" for c in reply[:40])
        archive_path = archive_dir / f"{safe_s}_{matched_at[:19].replace(':', '-')}.json"
        archive_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

        print(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"\n✅ Followup logged to {log_path}")
        print(f"✅ Reply archived to {archive_path}")

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A-line D2 auto followup")
    parser.add_argument("--reply", required=True, help="Customer reply text")
    parser.add_argument("--dry-run", action="store_true", help="Print only, no logging")
    args = parser.parse_args()

    followup(args.reply, dry_run=args.dry_run)
