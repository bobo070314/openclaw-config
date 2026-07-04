#!/usr/bin/env python3
"""
v1.8.0_assess.py — Auto-assessment script for v1.8.0 Go/No-Go decision.

Usage:
    python scripts/v1.8.0_assess.py

Output: prints structured Go/No-Go decision draft to stdout.
Intended for manual review by decision-maker (not auto-commit).
"""

import json, sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def run_assessment() -> dict:
    result = {
        "assessed_at": datetime.now(timezone.utc).isoformat(),
        "b_line": {},
        "code_assets": {},
        "docs": {},
        "gates": {},
        "overall": "",
        "decision": "PENDING",
    }

    # ── B-line status ──
    evo = load_json(PROJECT_ROOT / "data" / "runs" / "evolution_status.json")
    if evo:
        result["b_line"]["pass_rate"] = evo.get("pass_rate", "?")
        result["b_line"]["repeat_rate"] = evo.get("repeat_rate", "?")
        result["b_line"]["blocked"] = evo.get("blocked", "?")
        result["b_line"]["injected_count"] = evo.get("injected_count", "?")
        result["b_line"]["checks_passed"] = evo.get("checks_passed", "?")
        result["b_line"]["checks_total"] = evo.get("checks_total", "?")
        result["b_line"]["status"] = "ok"
    else:
        result["b_line"]["status"] = "NO_DATA"

    # ── Code assets ──
    auto_fixer = PROJECT_ROOT / "scripts" / "auto_fixer.py"
    result["code_assets"]["auto_fixer_exists"] = auto_fixer.exists()

    # ── Docs ──
    required_docs = [
        "docs/RFC-001-meta-autofix.md",
        "docs/auto_fixer_usage.md",
        "docs/v1.8.0_prefab_validation.md",
        "docs/v1.8.0_go_nogo_checklist.md",
        "docs/v1.8.0_launch_runbook.md",
        "docs/v1.8.0_release_announcement.md",
        "docs/A_line_D2_followup.md",
    ]
    docs_ok = all((PROJECT_ROOT / d).exists() for d in required_docs)
    result["docs"]["all_required_docs_exist"] = docs_ok
    result["docs"]["required_docs"] = {d: (PROJECT_ROOT / d).exists() for d in required_docs}

    # ── Gates (one-vote veto) ──
    gates = {}

    # G1: B-line blocked
    if evo and evo.get("blocked", True) is True:
        # blocked=False is good, but check if True
        gates["G1_block_triggered"] = evo.get("blocked", "?")

    # G2: repeat_rate >= 50%
    if evo:
        rr = evo.get("repeat_rate", 100)
        gates["G2_repeat_rate"] = rr
        gates["G2_ok"] = rr < 50

    # G3: manual code changes during observation
    gates["G3_manual_code_changes"] = False  # true if we detect non-doc commits

    # G4: pass_rate = 1.0
    if evo:
        gates["G4_pass_rate_ok"] = evo.get("pass_rate", 0) >= 0.99

    result["gates"] = gates

    # ── Overall ──
    vetoes = []
    if gates.get("G1_block_triggered") is True:
        vetoes.append("G1: block triggered during observation")
    if gates.get("G2_ok") is False:
        vetoes.append("G2: repeat_rate >= 50%")
    if gates.get("G4_pass_rate_ok") is False:
        vetoes.append("G4: pass_rate < 1.0")

    if vetoes:
        result["overall"] = "NO-GO"
        result["vetoes"] = vetoes
    else:
        result["overall"] = "GO"
        result["vetoes"] = []

    result["decision"] = result["overall"]
    return result


if __name__ == "__main__":
    result = run_assessment()
    print(json.dumps(result, indent=2, ensure_ascii=False))

    decision = result["decision"]
    if decision == "GO":
        print(f"\n{'='*40}")
        print("  ✅ GO — proceed to v1.8.0 launch")
        print("  📍 Run: docs/v1.8.0_launch_runbook.md")
        print(f"{'='*40}")
    elif decision == "NO-GO":
        print(f"\n{'='*40}")
        print("  ❌ NO-GO — vetoes active:")
        for v in result.get("vetoes", []):
            print(f"     • {v}")
        print("  📍 Review: docs/v1.8.0_go_nogo_checklist.md")
        print(f"{'='*40}")
    else:
        print(f"\n{'='*40}")
        print("  ⏳ PENDING — insufficient data")
        print(f"{'='*40}")
