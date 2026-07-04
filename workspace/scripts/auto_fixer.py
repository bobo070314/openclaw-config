"""
auto_fixer.py — Meta-Agent Auto-Fix Engine (v1.8.0)

DRAFT — Pre-written logic functions for RFC-001.
Do NOT integrate into orchestrator until v1.8.0 go/no-go decision.

Functions in this file are unit-testable independently.

Usage:
    python scripts/auto_fixer.py           # run P0 analysis
    python scripts/auto_fixer.py -h          # show this help

Supported fail_reason patterns (regex):
  FileMissing  — (file|missing|no\\s+such)
  RBACViolation— (rbac|permission|access|denied|forbidden|unauthorized)
  ConfigError  — (config|invalid|bad|syntax|parse)

Template locations:
  S1 (file)    — S1_TEMPLATES in scripts/auto_fixer.py
  S2 (config)  — S2_TEMPLATES in scripts/auto_fixer.py
  S3 (rbac)    — S3_TEMPLATES in scripts/auto_fixer.py
"""

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ── CLI help ──
def _print_help():
    print(__doc__.strip())
    sys.exit(0)


# ── Pre-compiled regex patterns for fuzzy fail_reason matching ──
_RE_FILE_MISSING = re.compile(r"(file|missing|no\s+such)", re.IGNORECASE)
_RE_CONFIG_ERR  = re.compile(r"(config|invalid|bad|syntax|parse)", re.IGNORECASE)
_RE_RBAC        = re.compile(r"(rbac|permission|access|denied|forbidden|unauthorized)", re.IGNORECASE)


# ──────────────────────────────────────────────────────
# Section 1: Failure Analysis (regex-based fuzzy matching)
# ──────────────────────────────────────────────────────


def load_eval(path: str | Path = None) -> dict | None:
    """Load latest_eval.json and return dict, or None if missing/unreadable."""
    if path is None:
        path = PROJECT_ROOT / "data" / "runs" / "latest_eval.json"
    path = Path(path)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def analyze_failures(eval_data: dict | None = None) -> dict:
    """
    Parse latest_eval.json checks and extract failure details.
    Uses regex for fuzzy matching on fail_reason to handle real-world variants.

    Category patterns:
      - FileMissing:     (file|missing|no\\s+such)
      - ConfigError:     (config|invalid|bad|syntax|parse)
      - RBACViolation:   (rbac|permission|access|denied|forbidden|unauthorized)

    Matching priority: FileMissing > RBACViolation > ConfigError > Unknown

    Returns:
        {
            "total_checks": int,
            "failed_checks": int,
            "failures": [
                {"check_name": str, "fail_reason": str, "category": str}
            ],
            "pass_rate": float,
            "analysis_timestamp": str (ISO-8601)
        }
    """
    if eval_data is None:
        eval_data = load_eval()

    # Handle missing / empty / unreadable eval data
    if eval_data is None:
        return {
            "total_checks": 0, "failed_checks": 0, "failures": [],
            "pass_rate": 1.0,
            "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
        }

    checks = eval_data.get("checks")
    if not checks:
        return {
            "total_checks": 0, "failed_checks": 0, "failures": [],
            "pass_rate": eval_data.get("pass_rate", 1.0),
            "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
        }

    pass_rate = eval_data.get("pass_rate", 1.0)

    failures = []
    for check in checks:
        if check.get("status") != "fail":
            continue

        name = check.get("name", "unknown_check")
        fail_reason = check.get("fail_reason", "No fail_reason provided")

        # Priority: FileMissing > RBACViolation > ConfigError > Unknown
        if _RE_FILE_MISSING.search(fail_reason):
            category = "FileMissing"
        elif _RE_RBAC.search(fail_reason):
            category = "RBACViolation"
        elif _RE_CONFIG_ERR.search(fail_reason):
            category = "ConfigError"
        else:
            category = "Unknown"

        failures.append({
            "check_name": name,
            "fail_reason": fail_reason,
            "category": category,
        })

    return {
        "total_checks": len(checks),
        "failed_checks": len(failures),
        "failures": failures,
        "pass_rate": pass_rate,
        "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ──────────────────────────────────────────────────────
# Section 2: Strategy Selection
# ──────────────────────────────────────────────────────


def select_strategy(analysis: dict) -> dict:
    """
    Based on failure analysis, select the best repair strategy.
    Returns:
        {"strategy": "S1"|"S2"|"S3"|"NONE", "confidence": float, ...}
    """
    failures = analysis.get("failures", [])
    if not failures:
        return {
            "strategy": "NONE", "confidence": 1.0, "target_files": [],
            "reason": "No failures detected. No repair needed.",
            "selected_at": datetime.now(timezone.utc).isoformat(),
        }

    cats = Counter(f["category"] for f in failures)
    most_common_cat = cats.most_common(1)[0][0]

    strategy_map = {
        "FileMissing": "S1", "ConfigError": "S2",
        "RBACViolation": "S3", "Unknown": "NONE",
    }
    strategy = strategy_map.get(most_common_cat, "NONE")

    total_fails = len(failures)
    top_count = cats.most_common(1)[0][1]
    confidence = round(top_count / max(total_fails, 1), 2)

    target_files = []
    for f in failures:
        check_path = PROJECT_ROOT / "configs" / f"{f['check_name']}.yaml"
        if check_path.exists():
            target_files.append(str(check_path))
    if not target_files:
        if strategy == "S1":
            target_files = [str(PROJECT_ROOT / "configs")]
        elif strategy in ("S2", "S3"):
            target_files = [str(PROJECT_ROOT / "configs" / "agent_chain.yaml")]

    return {
        "strategy": strategy,
        "confidence": confidence,
        "target_files": list(set(target_files)),
        "reason": f"Most common failure category: {most_common_cat} ({cats[most_common_cat]}/{total_fails})",
        "selected_at": datetime.now(timezone.utc).isoformat(),
    }


# ──────────────────────────────────────────────────────
# Section 3: Repair Strategy Templates (S1 / S2 / S3)
# ──────────────────────────────────────────────────────


S1_TEMPLATES = {
    "agent_chain.yaml": """# Agent Chain Configuration (auto-generated by auto_fixer S1)
pipeline:
  name: "silicon-base-delivery"
  version: "1.0.1"
  stages:
    - name: init
      script: "scripts/init.ps1"
      timeout_seconds: 30
      required: true
    - name: validate
      script: "scripts/orchestrator.py"
      timeout_seconds: 60
      required: true
  rbac:
    enabled: true
    violation_log: "data/runs/violations.jsonl"
""",
    "README.deliver.md": """# OpenClaw Delivery Package (auto-generated by auto_fixer S1)

## Quick Start
1. Run `scripts/init.ps1`
2. Run `scripts/run_all.ps1`

## Verification
Check `data/runs/latest_eval.json` for `pass_rate: 1.0`.
""",
}

S2_TEMPLATES = {
    "agent_chain.yaml": """# Agent Chain Configuration (auto-fixed by auto_fixer S2 — ConfigError)
# Fix applied: invalid_key replaced with known-good default
pipeline:
  name: "silicon-base-delivery"
  version: "1.0.1"
  stages:
    - name: init
      script: "scripts/init.ps1"
      timeout_seconds: 30
      required: true
    - name: validate
      script: "scripts/orchestrator.py"
      timeout_seconds: 60
      required: true
  rbac:
    enabled: true
    violation_log: "data/runs/violations.jsonl"
""",
}

S3_TEMPLATES = {
    "agent_chain.yaml": """# Agent Chain Configuration (auto-fixed by auto_fixer S3 — RBACViolation)
# Fix applied: restored default rbac permissions with explicit roles
pipeline:
  name: "silicon-base-delivery"
  version: "1.0.1"
  stages:
    - name: init
      script: "scripts/init.ps1"
      timeout_seconds: 30
      required: true
    - name: validate
      script: "scripts/orchestrator.py"
      timeout_seconds: 60
      required: true
  rbac:
    enabled: true
    violation_log: "data/runs/violations.jsonl"
    default_roles:
      - name: coder
        permissions:
          - read:configs
          - write:scripts
          - run:eval
""",
}


def apply_repair(strategy: str, target_name: str = "agent_chain.yaml") -> str | None:
    """
    Apply a repair template based on strategy (S1/S2/S3).
    Returns output file path on success, None if template not found.
    """
    template_map = {"S1": S1_TEMPLATES, "S2": S2_TEMPLATES, "S3": S3_TEMPLATES}
    templates = template_map.get(strategy)
    if templates is None:
        return None

    content = templates.get(target_name)
    if content is None:
        return None

    if target_name.endswith(".yaml"):
        output = PROJECT_ROOT / "configs" / target_name
    else:
        output = PROJECT_ROOT / target_name

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    return str(output)


# ──────────────────────────────────────────────────────
# Section 4: Rollback Decision
# ──────────────────────────────────────────────────────


def should_rollback(pre_repair_pass_rate: float, post_repair_pass_rate: float) -> dict:
    """
    Rule: rollback if post_repair < pre_repair (repair made things worse).
    """
    if post_repair_pass_rate >= pre_repair_pass_rate:
        return {
            "rollback": False, "pre_rate": pre_repair_pass_rate,
            "post_rate": post_repair_pass_rate,
            "reason": "Repair improved or maintained pass_rate. No rollback needed.",
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }

    return {
        "rollback": True, "pre_rate": pre_repair_pass_rate,
        "post_rate": post_repair_pass_rate,
        "reason": (f"Repair degraded pass_rate: {post_repair_pass_rate:.2f} < {pre_repair_pass_rate:.2f}. "
                   f"Rolling back to pre-repair state."),
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


# ──────────────────────────────────────────────────────
# Section 5: Audit Logging
# ──────────────────────────────────────────────────────


def log_fix_attempt(plan: dict, result: dict):
    """Append a fix attempt record to violations.jsonl for audit trail.
    Each line is prefixed with [TIMESTAMP] [LEVEL] for easy grep.

    Levels:
      INFO  — analysis / planning
      WARN  — strategy selected with low confidence
      ERROR — fix failed or rollback triggered
    """
    violations_path = PROJECT_ROOT / "data" / "runs" / "violations.jsonl"
    violations_path.parent.mkdir(parents=True, exist_ok=True)

    result_str = result.get("result", "unknown")
    level = "INFO"
    if result_str in ("failed", "rollback"):
        level = "ERROR"
    elif result_str == "analyzed_only":
        level = "INFO"
    elif plan.get("confidence", 1.0) < 0.8:
        level = "WARN"

    now = datetime.now(timezone.utc).isoformat()

    record = {
        "timestamp": now,
        "level": level,
        "action_type": "AUTO_REPAIR",
        "strategy": plan.get("strategy", "NONE"),
        "target_files": plan.get("target_files", []),
        "result": result_str,
        "detail": result.get("detail", ""),
    }

    # Prefix for grep-friendly log
    prefix = f"[{now}] [{level}] "

    with open(violations_path, "a", encoding="utf-8") as f:
        f.write(prefix + json.dumps(record, ensure_ascii=False) + "\n")


# ──────────────────────────────────────────────────────
# Section 6: Main Pipeline (P0 — analysis only, no execution)
# ──────────────────────────────────────────────────────


def run_fix_pipeline() -> dict:
    """P0: analysis only, no execution."""
    eval_data = load_eval()
    if eval_data is None:
        return {"status": "SKIP", "reason": "No eval data available."}

    analysis = analyze_failures(eval_data)
    plan = select_strategy(analysis)

    log_fix_attempt(plan, {"result": "analyzed_only", "detail": "P0: analysis only, no execution."})

    return {"status": "ANALYZED", "analysis": analysis, "plan": plan}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="auto_fixer.py — Meta-Agent Auto-Fix Engine")
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        _print_help()

    result = run_fix_pipeline()
    print(json.dumps(result, indent=2, ensure_ascii=False))
