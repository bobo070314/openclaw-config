#!/usr/bin/env python3
"""
b_line_24h_report.py — Generate B-line 24h observation summary report.
Designed to be run at observation end (2026-07-05 10:04 UTC).
Outputs structured report + Go/No-Go recommendation.

Usage:
    python scripts/b_line_24h_report.py
"""

import json, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def report():
    print(f"{'='*55}")
    print(f"  B-LINE 24H OBSERVATION REPORT")
    print(f"  Generated: {datetime.now(timezone.utc).isoformat()}")
    print(f"{'='*55}")

    # ── 1. Evolution status ──
    evo = load_json(ROOT / "data" / "runs" / "evolution_status.json")
    if evo:
        print(f"\n  📊 EVOLUTION STATUS")
        print(f"     pass_rate:       {evo.get('pass_rate', '?')}")
        print(f"     repeat_rate:     {evo.get('repeat_rate', '?')}%")
        print(f"     blocked:         {evo.get('blocked', '?')}")
        print(f"     injected_count:  {evo.get('injected_count', '?')}")
        print(f"     checks:          {evo.get('checks_passed', '?')}/{evo.get('checks_total', '?')}")
        print(f"     last_category:   {evo.get('last_category', '?')}")
        print(f"     last_update:     {evo.get('timestamp', '?')}")
    else:
        print(f"\n  ❌ EVOLUTION STATUS: NO DATA")

    # ── 2. Hardcases count ──
    hc = ROOT / "data" / "evals" / "hardcases.jsonl"
    if hc.exists():
        lines = hc.read_text(encoding="utf-8").strip().split("\n")
        print(f"\n  📋 HARD CASES")
        print(f"     total entries:   {len(lines)}")
        categories = set()
        for line in lines:
            try:
                d = json.loads(line)
                categories.add(d.get("category", "?"))
            except json.JSONDecodeError:
                pass
        print(f"     categories:      {', '.join(sorted(categories))}")
    else:
        print(f"\n  ❌ HARD CASES: FILE MISSING")

    # ── 3. Code readiness ──
    print(f"\n  🛠️  CODE READINESS")
    af = ROOT / "scripts" / "auto_fixer.py"
    print(f"     auto_fixer.py:    {'✅' if af.exists() else '❌'}")

    # ── 4. Docs ──
    required = [
        "docs/RFC-001-meta-autofix.md", "docs/auto_fixer_usage.md",
        "docs/v1.8.0_prefab_validation.md", "docs/v1.8.0_go_nogo_checklist.md",
        "docs/v1.8.0_launch_runbook.md", "docs/v1.8.0_release_announcement.md",
    ]
    missing = [d for d in required if not (ROOT / d).exists()]
    print(f"     docs:             {'✅ ALL' if not missing else f'❌ MISSING: {missing}'}")

    # ── 5. Recommendation ──
    print(f"\n  {'='*55}")
    if evo and evo.get("pass_rate", 0) >= 0.99 and evo.get("blocked") is False:
        if evo.get("repeat_rate", 100) < 50:
            decision = "🟢 GO"
            note = "All gates pass. Ready for v1.8.0 launch."
        else:
            decision = "🔴 NO-GO"
            note = f"Repeat rate too high: {evo.get('repeat_rate')}%"
    else:
        decision = "🔴 NO-GO"
        note = "One or more gates failed."

    if evo is None:
        decision = "⏳ PENDING"
        note = "Insufficient B-line data."

    print(f"     RECOMMENDATION:   {decision}")
    print(f"     NOTE:             {note}")
    print(f"     SEE:              docs/v1.8.0_go_nogo_checklist.md")
    print(f"  {'='*55}")


if __name__ == "__main__":
    report()
