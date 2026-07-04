"""
monitor_daemon.py - Unattended observation daemon for B-Line.

Runs a 30-minute reporting loop reading evolution_status.json.
Outputs Runbook-templated reports to stdout (redirect to log for persistence).

Usage:
    python scripts/monitor_daemon.py > logs/monitor.log 2>&1
    # Stop with: Ctrl+C
"""

import json
import time
import sys
from datetime import datetime, timezone
from pathlib import Path


STATUS_FILE = Path("data/runs/evolution_status.json")
REPORT_INTERVAL = 1800  # 30 minutes


def load_status() -> dict | None:
    if not STATUS_FILE.exists():
        return None
    try:
        return json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def check_anomaly(status: dict) -> str | None:
    """Return alert level if anomaly detected, else None."""
    repeat_rate = status.get("repeat_rate", 0.0)
    blocked = status.get("blocked", False)

    if blocked:
        return "BLOCK"
    if isinstance(repeat_rate, (int, float)) and repeat_rate >= 50:
        return "BLOCK"
    if isinstance(repeat_rate, (int, float)) and repeat_rate >= 20:
        return "WARN"
    return None


def evaluate_watchdog(status: dict) -> str:
    """Return a short assessment note."""
    if status is None:
        return "NO_DATA"
    now = datetime.now(timezone.utc)
    last_ts = status.get("timestamp", "")
    if last_ts:
        try:
            last_dt = datetime.fromisoformat(last_ts)
            age_min = (now - last_dt).total_seconds() / 60
            if age_min > 120:
                return f"STALE (last update {age_min:.0f} min ago)"
        except ValueError:
            pass
    return "OK"


def report(cycle: int):
    """Emit one Runbook-templated report to stdout."""
    status = load_status()
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"[{timestamp}] B-LINE REPORT  cycle={cycle}")

    if status is None:
        print("  ERROR: evolution_status.json not found or unreadable")
        print("-" * 30)
        return

    pass_rate = status.get("pass_rate", "?")
    repeat_rate = f"{status.get('repeat_rate', '?')}%"
    injected = status.get("injected_count", "?")
    blocked = status.get("blocked", "?")
    anomaly = check_anomaly(status)
    watchdog = evaluate_watchdog(status)

    print(f"  pass_rate:    {pass_rate}")
    print(f"  repeat_rate:  {repeat_rate}  {resolve_glyph(anomaly)}")
    print(f"  injected:     {injected}")
    print(f"  blocked:      {blocked}")
    print(f"  watchdog:     {watchdog}")

    if anomaly == "BLOCK":
        print(f"  🚫 ALERT: repeat_rate >= 50% or block active. Immediate intervention needed.")
    elif anomaly == "WARN":
        print(f"  ⚠️  WARN: repeat_rate >= 20%. Monitor closely.")

    print("-" * 30)
    sys.stdout.flush()


def resolve_glyph(anomaly: str | None) -> str:
    if anomaly == "BLOCK":
        return "🚫"
    if anomaly == "WARN":
        return "⚠️"
    return "✅"


def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] monitor_daemon STARTED")
    print(f"  Reporting every {REPORT_INTERVAL}s ({REPORT_INTERVAL//60} min)")
    print("=" * 30)
    sys.stdout.flush()

    cycle = 0
    try:
        while True:
            cycle += 1
            report(cycle)
            time.sleep(REPORT_INTERVAL)
    except KeyboardInterrupt:
        print(f"\n[{datetime.now(timezone.utc).isoformat()}] monitor_daemon STOPPED (Ctrl+C)")
        print(f"  Total cycles: {cycle}")
        sys.exit(0)


if __name__ == "__main__":
    main()
