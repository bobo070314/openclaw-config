#!/usr/bin/env python3
"""
report_b_line.py — Auto-generate B-line health report as Markdown.

Usage:
    python scripts/report_b_line.py              # print to stdout
    python scripts/report_b_line.py --history     # list all evolution_status.json entries
"""

import argparse, json, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EMOJI_MAP = {
    "ok": "🟢",
    "warn": "🟡",
    "block": "🔴",
}


def load_evolution() -> dict | None:
    path = ROOT / "data" / "runs" / "evolution_status.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def determine_status(evo: dict) -> str:
    if evo.get("blocked", False):
        return "block"
    rr = evo.get("repeat_rate", 0)
    if rr >= 50:
        return "block"
    if rr >= 20:
        return "warn"
    return "ok"


def generate_report(evo: dict) -> str:
    is_blocked = evo.get("blocked", False)
    rr = evo.get("repeat_rate", 0)
    pr = evo.get("pass_rate", "?")
    ic = evo.get("injected_count", "?")
    ts = evo.get("timestamp", "?")
    cp = evo.get("checks_passed", "?")
    ct = evo.get("checks_total", "?")
    lc = evo.get("last_category", "?")

    status = determine_status(evo)
    emoji = EMOJI_MAP.get(status, "🟢")

    if status == "block":
        status_line = "⚠️ BLOCKED — 异常触发，需要人工干预"
    elif status == "warn":
        status_line = "⚠️ 告警 — repeat_rate ≥ 20%，建议关注"
    else:
        status_line = "✅ 稳态运行，无需干预"

    report = f"""## B-Line 续报

- **时间**: {ts}
- **pass_rate**: {pr}
- **repeat_rate**: {rr}%
- **blocked**: {str(is_blocked)}
- **injected_count**: {ic}
- **checks**: {cp}/{ct}
- **last_category**: {lc}

## 状态

{emoji} {status_line}

## 指标趋势

| 时段 | pass_rate | repeat_rate | blocked | injected_count |
|---|---|---|---|---|
| {ts} | {pr} | {rr}% | {str(is_blocked)} | {ic} |

## 下轮续报

``` 
下一续报: 30分钟后
{status_line}
```
"""
    return report


def main():
    parser = argparse.ArgumentParser(description="B-line health report generator")
    parser.add_argument("--history", action="store_true", help="Show all historical evolution entries")
    args = parser.parse_args()

    evo = load_evolution()
    if evo is None:
        print("❌ evolution_status.json not found. Has B-line been started?")
        sys.exit(1)

    if args.history:
        # Show all history if available
        for k, v in sorted(evo.items()):
            print(f"  {k}: {v}")
    else:
        print(generate_report(evo))


if __name__ == "__main__":
    main()
