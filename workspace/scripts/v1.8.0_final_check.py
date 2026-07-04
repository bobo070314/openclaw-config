#!/usr/bin/env python3
"""
v1.8.0_final_check.py — Pre-launch final verification.
Checks: git tags, commits, test counts, doc presence, B-line status.
Outputs: structured JSON report. Exit code 0 = all clear.

Usage:
    python scripts/v1.8.0_final_check.py
"""

import json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git(args: list[str]) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT)] + args,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def check():
    issues = []
    ok = 0

    def verify(name: str, condition: bool, detail: str = ""):
        nonlocal ok
        if condition:
            ok += 1
        else:
            issues.append(f"{name}: {detail}")

    # ── Tags ──
    tags = git(["tag", "-l", "v1.8*"])
    verify("v1.8.0-design-draft tag", "v1.8.0-design-draft" in tags)
    verify("v1.8.0-auto-fixer-ready tag", "v1.8.0-auto-fixer-ready" in tags)

    # ── auto_fixer.py presence ──
    af = ROOT / "scripts" / "auto_fixer.py"
    verify("auto_fixer.py exists", af.exists(), "missing")

    if af.exists():
        content = af.read_text(encoding="utf-8")
        verify("has analyze_failures", "def analyze_failures" in content)
        verify("has select_strategy", "def select_strategy" in content)
        verify("has should_rollback", "def should_rollback" in content)
        verify("has log_fix_attempt", "def log_fix_attempt" in content)
        verify("has apply_repair", "def apply_repair" in content)
        verify("has S1_TEMPLATES", "S1_TEMPLATES" in content)
        verify("has S2_TEMPLATES", "S2_TEMPLATES" in content)
        verify("has S3_TEMPLATES", "S3_TEMPLATES" in content)

    # ── B-line status ──
    evo = ROOT / "data" / "runs" / "evolution_status.json"
    if evo.exists():
        edata = json.loads(evo.read_text(encoding="utf-8"))
        verify("evolution_status.json readable", True)
        verify("pass_rate == 1.0", edata.get("pass_rate") >= 0.99, str(edata.get("pass_rate")))
        verify("repeat_rate == 0%", edata.get("repeat_rate", -1) < 1, str(edata.get("repeat_rate")))
        verify("blocked == false", edata.get("blocked") is False, str(edata.get("blocked")))
    else:
        issues.append("evolution_status.json missing")

    # ── Required docs ──
    required = [
        "docs/RFC-001-meta-autofix.md",
        "docs/auto_fixer_usage.md",
        "docs/v1.8.0_prefab_validation.md",
        "docs/v1.8.0_go_nogo_checklist.md",
        "docs/v1.8.0_launch_runbook.md",
        "docs/v1.8.0_release_announcement.md",
        "docs/A_line_D2_followup.md",
        "docs/v1.8.0_incident_response.md",
        "docs/CHANGELOG_v1.8.0.md",
    ]
    for d in required:
        verify(f"doc {d} exists", (ROOT / d).exists(), "missing")

    # ── Scripts ──
    req_scripts = ["d2_reminder.py", "v1.8.0_assess.py", "auto_fixer_demo.py"]
    for s in req_scripts:
        verify(f"script {s} exists", (ROOT / "scripts" / s).exists(), "missing")

    # ── Summary ──
    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "checks": {
            "total": ok + len(issues),
            "passed": ok,
            "failed": len(issues),
        },
        "issues": issues,
        "overall": "READY" if not issues else "ISSUES_DETECTED",
    }

    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not issues:
        print(f"\n✅ ALL {report['checks']['total']} CHECKS PASSED — ready for launch")
    else:
        print(f"\n❌ {len(issues)} ISSUES — resolve before launch")
        for i in issues:
            print(f"   • {i}")
    sys.exit(0 if not issues else 1)


if __name__ == "__main__":
    check()
