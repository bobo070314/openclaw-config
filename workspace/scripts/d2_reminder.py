"""
d2_reminder.py — A-line D2 followup reminder.
Sends a notification to the user at 24h mark (set via cron or manual run).

Usage:
    python scripts/d2_reminder.py [--dry-run]
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

D2_THRESHOLD_HOURS = 24
TRIGGER_FILES = ["docs/A_line_D2_followup.md"]


def check_followup_due() -> bool:
    """
    Check if D2 followup is due based on git log or manual status file.
    Returns True if it's time to send D2 message.
    """
    status_path = PROJECT_ROOT / "data" / "runs" / "a_line_status.json"
    if not status_path.exists():
        return False

    status = json.loads(status_path.read_text(encoding="utf-8"))
    sent_at_iso = status.get("sent_at")
    if not sent_at_iso:
        return False

    sent_at = datetime.fromisoformat(sent_at_iso)
    now = datetime.now(timezone.utc)
    elapsed = (now - sent_at).total_seconds() / 3600
    return elapsed >= D2_THRESHOLD_HOURS


def print_reminder(dry_run: bool = False):
    """Print D2 followup reminder text."""
    if dry_run:
        print("[DRY RUN] D2 reminder would fire. Followup text:")
        print()

    path = PROJECT_ROOT / "docs" / "A_line_D2_followup.md"
    text = path.read_text(encoding="utf-8") if path.exists() else "Followup doc not found."

    print(f"🔔 A-LINE D2 REMINDER ({datetime.now(timezone.utc).isoformat()})")
    print("=" * 55)
    print(text)
    print("=" * 55)

    if not dry_run:
        # Write a flag file to indicate reminder was fired
        flag = PROJECT_ROOT / "data" / "runs" / "d2_reminder_fired.flag"
        flag.parent.mkdir(parents=True, exist_ok=True)
        flag.write_text(datetime.now(timezone.utc).isoformat())
        print(f"\n✅ Reminder flag written to {flag}")
    else:
        print("\n⏸️  Dry run — no flag written.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A-line D2 followup reminder")
    parser.add_argument("--dry-run", action="store_true", help="Print reminder without writing flag")
    args = parser.parse_args()

    if not check_followup_due():
        if args.dry_run:
            print("⏳ D2 reminder not due yet (24h threshold not reached).")
        else:
            status_path = PROJECT_ROOT / "data" / "runs" / "a_line_status.json"
            print(f"⏳ D2 reminder not due. Check data/runs/a_line_status.json for sent_at timestamp.")
            if not status_path.exists():
                print("   (status file missing — create with {\"sent_at\": \"2026-07-04T...\"})")
        sys.exit(0)

    print_reminder(dry_run=args.dry_run)
