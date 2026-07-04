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
    parser.add_argument("--notify", action="store_true", help="Write report to notification.log")
    args = parser.parse_args()

    evo = load_evolution()
    if evo is None:
        msg = "[NOTIFY] evolution_status.json not found. Has B-line been started?"
        print(msg)
        if args.notify:
            log_path = ROOT / "data" / "runs" / "notification.log"
            log_path.write_text(msg + "\n", encoding="utf-8")
        sys.exit(1)

    if args.history:
        for k, v in sorted(evo.items()):
            print(f"  {k}: {v}")
        return

    report = generate_report(evo)
    print(report)

    # Archive to reports/history/
    ts = evo.get("timestamp", datetime.now(timezone.utc).isoformat())
    hour_min = ts[11:16] if len(ts) >= 16 else ts
    safe_ts = ts[:19].replace(":", "-").replace("T", "_")
    archive_dir = ROOT / "reports" / "history"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / f"b_line_{safe_ts}.md"
    archive_path.write_text(report, encoding="utf-8")
    print(f"[ARCHIVE] Saved to {archive_path}")

    if args.notify:
        log_path = ROOT / "data" / "runs" / "notification.log"
        status = determine_status(evo)
        entry = f"[{hour_min}] [B-LINE] Report generated | ts={ts} | status={status} | pass_rate={evo.get('pass_rate','?')} | repeat_rate={evo.get('repeat_rate','?')}%\n"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"[NOTIFY] Written to {log_path}")


if __name__ == "__main__":
    main()
