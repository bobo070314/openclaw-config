"""
auto_fixer_demo.py — 10-second demo script for A-line customer followup.
Shows: input a fail_reason → auto_fixer categorizes it → outputs repair template name.

Colors: green=success, blue=info, red=error, cyan=headers.

Usage:
    python scripts/auto_fixer_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path("scripts").resolve()))
from auto_fixer import analyze_failures, select_strategy, apply_repair

# ANSI color codes
GREEN = "\033[92m"
BLUE = "\033[94m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Simulate eval failure scenarios
test_failures = [
    "missing file: configs/agent_chain.yaml",
    "invalid config: bad configuration value",
    "rbac: permission denied for user coder",
]

print(f"{CYAN}{'=' * 52}{RESET}")
print(f"{BOLD}{CYAN}  auto_fixer demo — input \u2192 categorize \u2192 repair{RESET}")
print(f"{CYAN}{'=' * 52}{RESET}")

for fail_reason in test_failures:
    eval_data = {
        "pass_rate": 0.0,
        "checks": [{
            "name": "demo_check",
            "status": "fail",
            "fail_reason": fail_reason
        }]
    }
    analysis = analyze_failures(eval_data)
    plan = select_strategy(analysis)
    result_path = apply_repair(plan["strategy"])

    category = analysis["failures"][0]["category"]
    strategy = plan["strategy"]
    confidence = plan["confidence"]

    # Color by category
    if category == "FileMissing":
        cat_color = YELLOW
    elif category == "ConfigError":
        cat_color = BLUE
    elif category == "RBACViolation":
        cat_color = RED
    else:
        cat_color = RESET

    print(f"\n  {BOLD}{CYAN}\u2500\u2500 Input{RESET}")
    print(f"     {BLUE}fail_reason:{RESET} {fail_reason}")
    print(f"  {BOLD}{CYAN}\u2500\u2500 Result{RESET}")
    print(f"     {GREEN}category:{RESET}   {cat_color}{category}{RESET}")
    print(f"     {GREEN}strategy:{RESET}   {cat_color}{strategy}{RESET}")
    print(f"     {GREEN}confidence:{RESET} {cat_color}{confidence}{RESET}")
    print(f"     {GREEN}applied to:{RESET} {result_path}")

print(f"\n{CYAN}{'=' * 52}{RESET}")
print(f"  {GREEN}\u2705 10-second demo complete.{RESET}")
print(f"{CYAN}{'=' * 52}{RESET}")
