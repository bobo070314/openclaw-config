#!/usr/bin/env python3
"""
v1.8.0_rollback_drill.py — Simulate auto_fixer failure and test rollback path.

This is a DRY-RUN script. It prints what would happen without modifying files.

Usage:
    python scripts/v1.8.0_rollback_drill.py [--apply]  # --apply to actually run
"""

import argparse, subprocess, json, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git(*args: str) -> str:
    r = subprocess.run(
        ["git", "-C", str(ROOT)] + list(args),
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return r.stdout.strip()


def drill(apply: bool = False) -> dict:
    steps = []
    ok = True

    # Step 1: Check current state
    head = git("rev-parse", "--short", "HEAD")
    tag = git("describe", "--tags", "--exact-match", "HEAD")
    steps.append({"step": "Current HEAD", "ref": head, "tag": tag or "no tag"})

    # Step 2: Check v1.8.0-auto-fixer-ready tag exists
    tags = git("tag", "-l", "v1.8.0-auto-fixer-ready")
    if "v1.8.0-auto-fixer-ready" not in tags:
        steps.append({"step": "Rollback source", "status": "FAIL: tag v1.8.0-auto-fixer-ready not found"})
        ok = False
    else:
        steps.append({"step": "Rollback source", "status": "available", "tag": "v1.8.0-auto-fixer-ready"})

    # Step 3: Check v1.7.2-bline-monitor-daemon tag exists
    tags = git("tag", "-l", "v1.7.2-bline-monitor-daemon")
    if "v1.7.2-bline-monitor-daemon" not in tags:
        steps.append({"step": "Rollback target", "status": "FAIL: tag v1.7.2-bline-monitor-daemon not found"})
        ok = False
    else:
        steps.append({"step": "Rollback target", "status": "available", "tag": "v1.7.2-bline-monitor-daemon"})

    # Step 4: Report current b-line status as baseline
    evo = ROOT / "data" / "runs" / "evolution_status.json"
    if evo.exists():
        edata = json.loads(evo.read_text(encoding="utf-8"))
        steps.append({
            "step": "B-line baseline",
            "pass_rate": edata.get("pass_rate"),
            "repeat_rate": edata.get("repeat_rate"),
            "blocked": edata.get("blocked"),
        })

    # Step 5: Commands that would be run
    cmds = []
    if ok:
        cmds.append("git revert HEAD --no-edit")
        cmds.append("git tag v1.8.0-rollback-drill")
        cmds.append("git checkout v1.7.2-bline-monitor-daemon")
        cmds.append("python scripts/orchestrator.py  # verify pass_rate >= 1.0")
        cmds.append("git checkout main  # restore to latest")

    if apply:
        for cmd in cmds[:2]:
            subprocess.run(cmd, shell=True, cwd=ROOT)
        steps.append({"step": "APPLIED: git revert + tag"})
        steps.append({"step": "WARNING: git checkout v1.7.2 would change working tree"})
    else:
        steps.append({"step": "Simulated commands (dry-run)", "commands": cmds})

    result = {
        "drill_time": datetime.now(timezone.utc).isoformat(),
        "mode": "APPLY" if apply else "DRY-RUN",
        "overall_ok": ok,
        "steps": steps,
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="v1.8.0 rollback drill")
    parser.add_argument("--apply", action="store_true", help="Actually run rollback")
    args = parser.parse_args()

    drill(apply=args.apply)
