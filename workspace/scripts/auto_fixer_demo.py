"""
auto_fixer_demo.py — 10-second demo script for A-line customer followup.
Shows: input a fail_reason → auto_fixer categorizes it → outputs repair template name.

Usage:
    python demos/auto_fixer_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path("scripts").resolve()))
from auto_fixer import analyze_failures, select_strategy, apply_repair

# Simulate eval failure scenarios
test_failures = [
    "missing file: configs/agent_chain.yaml",
    "invalid config: bad configuration value",
    "rbac: permission denied for user coder",
]

print("=" * 52)
print("  auto_fixer demo — input → categorize → repair")
print("=" * 52)

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

    print(f"\n  ── Input ──")
    print(f"     fail_reason: {fail_reason}")
    print(f"  ── Result ──")
    print(f"     category:   {category}")
    print(f"     strategy:   {strategy}")
    print(f"     confidence: {confidence}")
    print(f"     applied to: {result_path}")

print(f"\n{'=' * 52}")
print("  ✅ 10-second demo complete.")
print(f"{'=' * 52}")
