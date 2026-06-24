#!/usr/bin/env python
"""
evaluator v0.1.0 — Eval Loop Runner
=====================================
Runs a skill via sandbox against a golden test case,
then scores the result.

Usage:
    python evaluator/run.py <skill_name> <test_case>

Example:
    python evaluator/run.py security-audit eval-suite/test_case_01.py

Output:
    Score: 100/100 (or 0/100)
"""

import argparse

# === V0.2.0 CLI STANDARD (auto-injected, do not remove) ===
VERSION = "0.2.0"
SKILL_NAME = "evaluator"
import json
import sys as _sys

def _handle_std_flags():
    """Handle --version, --json, --dry-run before main logic."""
    _args = [a for a in _sys.argv[1:] if not a.startswith("-")]
    _flags = [a for a in _sys.argv[1:] if a.startswith("-")]

    if "--version" in _flags:
        print(json.dumps({"skill": SKILL_NAME, "version": VERSION, "status": "live"}, indent=2))
        _sys.exit(0)

    if "--json" in _flags and len(_args) == 0:
        print(json.dumps({"skill": SKILL_NAME, "version": VERSION, "status": "live"}, indent=2))
        _sys.exit(0)

    if "--dry-run" in _flags:
        dry = {"skill": SKILL_NAME, "version": VERSION, "dry_run": True, "note": "Dry run — skipping real execution."}
        print(json.dumps(dry, indent=2))
        _sys.exit(0)

    # Clean flags so original argv parsing doesn't break
    _sys.argv = [_sys.argv[0]] + _args

_handle_std_flags()
# === END CLI STANDARD ===

import json
import subprocess
import sys
import os
import re
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent.parent
EVAL_DIR = ROOT / "eval-suite"
LOGS_DIR = ROOT / ".deploy" / "logs"
SANDBOX_RUNNER = ROOT / "skills" / "sandbox-executor" / "run-native.py"


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def log_event(event_type: str, details: dict):
    ensure_dir(LOGS_DIR)
    log_file = LOGS_DIR / "evaluator.jsonl"
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event_type,
        **details,
    }
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def find_test_case(name: str) -> Path:
    """Find test case by name (with or without .py extension)."""
    test_path = EVAL_DIR / name
    if test_path.exists():
        return test_path
    test_path = EVAL_DIR / f"{name}.py"
    if test_path.exists():
        return test_path
    raise FileNotFoundError(f"Test case '{name}' not found in {EVAL_DIR}")


def run_sandbox_scan(skill_name: str, target: Path, timeout: int = 60) -> dict:
    """Run a skill via sandbox-executor against a target file."""
    cmd = [
        sys.executable,
        str(SANDBOX_RUNNER),
        "--no-workspace",
        "--timeout", str(timeout),
        skill_name,
        "--target", str(target),
    ]

    print(f"[evaluator] Sandbox run: {' '.join(cmd)}", flush=True)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=timeout + 10,
            cwd=str(ROOT),
            encoding="utf-8", errors="replace",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"exit_code": 137, "stdout": "", "stderr": "Evaluator timed out"}


def evaluate_security_audit(result: dict, test_case: Path) -> dict:
    """
    Score security-audit results.
    A "GOOD" result means the audit DETECTED the vulnerability.
    """
    # Exclude sandbox-executor framing output, only look at skill output
    raw = result["stdout"] + result["stderr"]
    # Strip sandbox-executor lines
    skill_output = '\n'.join(
        line for line in raw.split('\n')
        if not line.startswith('[sandbox-executor')
    )
    combined_output = skill_output.lower()

    # Keywords that indicate vulnerability detection
    vuln_keywords = [
        "sql injection",
        "vulnerab",
        "unsafe",
        "injection",
        "string formatting",
        "f-string",
        "concatenat",
        "not parameterized",
        "use parameterized",
        "warning: high",
        "critical",
    ]

    # Also check for findings in JSON output
    findings_count = 0
    try:
        import json
        data = json.loads(skill_output)
        findings_count = len(data.get("findings", []))
    except (json.JSONDecodeError, Exception):
        pass

    detected = any(kw in combined_output for kw in vuln_keywords) or findings_count > 0

    if detected:
        return {"score": 100, "max_score": 100, "verdict": "PASS", "reason": "Vulnerability detected"}
    else:
        return {"score": 0, "max_score": 100, "verdict": "FAIL", "reason": "Vulnerability NOT detected"}


SCORERS = {
    "security-audit": evaluate_security_audit,
    # Future scorers:
    # "code-review": evaluate_code_review,
    # "performance-bench": evaluate_performance,
}


def evaluate(skill_name: str, test_case: str, timeout: int = 60) -> dict:
    """Full evaluation pipeline."""
    test_path = find_test_case(test_case)

    # Step 1: Run sandbox scan
    print(f"[evaluator] Scanning {test_path.name} with {skill_name}...", flush=True)
    scan_result = run_sandbox_scan(skill_name, test_path, timeout)
    print(f"[evaluator] Scan exit: {scan_result['exit_code']}", flush=True)

    # Step 2: Score based on skill type
    scorer = SCORERS.get(skill_name)
    if scorer:
        score = scorer(scan_result, test_path)
    else:
        # Generic scorer: if scan finds anything interesting, it passes
        has_output = len(scan_result["stdout"] + scan_result["stderr"]) > 10
        score = {
            "score": 100 if has_output else 0,
            "max_score": 100,
            "verdict": "PASS" if has_output else "FAIL",
            "reason": f"Output {len(scan_result['stdout'] + scan_result['stderr'])} chars detected" if has_output else "No output",
        }

    # Step 3: Log
    log_event("eval_complete", {
        "skill": skill_name,
        "test_case": test_path.name,
        "score": score["score"],
        "verdict": score["verdict"],
    })

    return {
        "skill": skill_name,
        "test_case": test_path.name,
        **score,
        "scan_stdout": scan_result["stdout"],
        "scan_stderr": scan_result["stderr"],
    }


def main():
    parser = argparse.ArgumentParser(description="evaluator: Eval Loop Runner")
    parser.add_argument("skill", help="Skill name to evaluate")
    parser.add_argument("test_case", help="Test case file (in eval-suite/)")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout per scan")
    args = parser.parse_args()

    print(f"╔══════════════════════════════════╗")
    print(f"║  evaluator v0.1.0 — Eval Loop   ║")
    print(f"╚══════════════════════════════════╝")
    print(f"\nSkill: {args.skill}")
    print(f"Test:  {args.test_case}")

    result = evaluate(args.skill, args.test_case, args.timeout)

    print(f"\n{'=' * 50}")
    print(f"EVALUATION RESULT")
    print(f"{'=' * 50}")
    print(f"Score: {result['score']}/{result['max_score']}")
    print(f"Verdict: {result['verdict']}")
    print(f"Reason: {result['reason']}")

    if result.get("scan_stdout"):
        print(f"\n--- Scan Output ---")
        print(result["scan_stdout"][:1000])

    sys.exit(0 if result["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
