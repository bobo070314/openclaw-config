"""
meta_agent.py - Self-evolution engine for Silicon Base Group (v0.2)

v0.2 features:
- Category rotation: self_evolution -> edge_case -> stress_test -> rbac_attack
- Hardcase dedup by (category + normalized_prompt_hash)
- Repeat-rate gates: warn >= 20%, block >= 50%
- Evolution status log to data/runs/evolution_status.json
"""

import hashlib
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def get_evals_dir() -> Path:
    d = get_project_root() / "data" / "evals"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_runs_dir() -> Path:
    d = get_project_root() / "data" / "runs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_latest_eval() -> dict | None:
    path = get_project_root() / "data" / "runs" / "latest_eval.json"
    if not path.exists():
        print("[META] No latest_eval.json found.")
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_hardcase_history() -> list[dict]:
    path = get_evals_dir() / "hardcases.jsonl"
    if not path.exists():
        return []
    cases = []
    for line in path.read_text(encoding="utf-8").strip().splitlines():
        if line.strip():
            cases.append(json.loads(line))
    return cases


def save_hardcase_history(cases: list[dict]):
    path = get_evals_dir() / "hardcases.jsonl"
    with open(path, "w", encoding="utf-8") as f:
        for c in cases:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")


def analyze_patterns(history: list[dict]) -> dict:
    if not history:
        return {"total": 0, "categories": {}, "latest_category": None, "repeat_rate": 0.0}
    cats = Counter(c.get("category", "unknown") for c in history)
    repeat_rate = round((sum(v - 1 for v in cats.values()) / max(len(history), 1)) * 100, 1)
    return {
        "total": len(history),
        "categories": dict(cats),
        "latest_category": history[-1].get("category"),
        "repeat_rate": repeat_rate,
    }


def prompt_hash(prompt: str) -> str:
    """Normalize and hash a prompt for deduplication."""
    normalized = " ".join(prompt.lower().split())
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def dedupe_hardcases(cases: list[dict]) -> list[dict]:
    """Remove duplicates by dedupe_key = category + prompt_hash. Keep first occurrence."""
    seen = set()
    deduped = []
    removed = 0
    for c in cases:
        key = (c.get("category", ""), prompt_hash(c.get("input", "")))
        if key in seen:
            removed += 1
            continue
        seen.add(key)
        deduped.append(c)

    if removed:
        print(f"[META] 🧹 Dedup removed {removed} duplicate(s). {len(deduped)} unique remain.")
    return deduped


def generate_hardcase(pass_rate: float, history: list[dict]) -> dict:
    now = datetime.now(timezone.utc)
    case_id = f"EVOLVED-{now.strftime('%Y%m%d%H%M%S%f')}"
    now_iso = now.isoformat()

    patterns = analyze_patterns(history)

    category_rotation = [
        "self_evolution",
        "edge_case",
        "stress_test",
        "rbac_attack",
    ]

    # Pick category: alternate from last, or default to self_evolution
    if "latest_category" in patterns and patterns["latest_category"] in category_rotation:
        idx = category_rotation.index(patterns["latest_category"])
        chosen_cat = category_rotation[(idx + 1) % len(category_rotation)]
    else:
        chosen_cat = category_rotation[0]

    inputs = {
        "self_evolution": (
            "Deliberately introduce a config that will cause a 401/403 error, "
            "then produce a fix that restores it to 200. "
            "RBAC must catch the violation and log it to violations.jsonl."
        ),
        "edge_case": (
            "Create a scenario where the system receives malformed input "
            "(empty payload, missing required fields) and must gracefully "
            "handle it without crashing — return a clear error message."
        ),
        "stress_test": (
            "Simulate 10 concurrent pipeline runs. The system must complete "
            "all 10 within 120 seconds without any failure. "
            "Logging must show no overlapping resource contention."
        ),
        "rbac_attack": (
            "Attempt to access the system with unauthorized permissions. "
            "RBAC must reject all unauthorized operations and log each "
            "violation with the correct actor, target, and reason."
        ),
    }

    return {
        "id": case_id,
        "generated_at": now_iso,
        "category": chosen_cat,
        "pass_rate_at_gen": pass_rate,
        "input": inputs[chosen_cat],
        "expected": {
            "status_code": 200,
            "violation_logged": True if chosen_cat in ("rbac_attack", "self_evolution") else False,
            "graceful_failure": True if chosen_cat == "edge_case" else False,
        },
    }


def write_status(patterns: dict, blocked: bool, injected: bool):
    """Write evolution_status.json to data/runs/."""
    status = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pass_rate": None,  # filled after loading eval
        "last_category": patterns.get("latest_category"),
        "repeat_rate": patterns.get("repeat_rate", 0.0),
        "injected_count": patterns.get("total", 0),
        "blocked": blocked,
    }
    # Try to fill pass_rate from latest eval
    eval_data = load_latest_eval()
    if eval_data:
        status["pass_rate"] = eval_data.get("pass_rate")
        status["checks_passed"] = eval_data.get("checks_passed")
        status["checks_total"] = eval_data.get("checks_total")

    target = get_runs_dir() / "evolution_status.json"
    target.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")
    rel = target.relative_to(get_project_root())
    print(f"[META] Status logged: {rel}")


def evolve_hardcases() -> bool:
    """Main entry point. Returns True if a new case was injected."""
    eval_data = load_latest_eval()
    if eval_data is None:
        return False

    history = load_hardcase_history()
    patterns = analyze_patterns(history)
    pass_rate = eval_data.get("pass_rate", 1.0)
    repeat_rate = patterns["repeat_rate"]

    print(f"[META] pass_rate: {pass_rate} | hardcases total: {patterns['total']} "
          f"| repeat_rate: {repeat_rate}%")

    # ---- Gate: block if repeat_rate >= 50% ----
    blocked = False
    if repeat_rate >= 50:
        print(f"[META] 🚫 BLOCKED: repeat_rate {repeat_rate}% >= 50% threshold. "
              f"Running dedup + compression instead.")
        deduped = dedupe_hardcases(history)
        save_hardcase_history(deduped)
        patterns = analyze_patterns(deduped)
        print(f"[META] After dedup: {patterns['total']} hardcases, "
              f"repeat_rate {patterns['repeat_rate']}%.")
        blocked = True
        write_status(patterns, blocked=True, injected=False)
        return False

    # ---- Gate: warn if repeat_rate >= 20% ----
    if repeat_rate >= 20:
        print(f"[META] ⚠️  Repeat rate {repeat_rate}% >= 20% threshold. "
              f"Consider intervention if this persists.")

    # ---- Generate and inject ----
    new_case = generate_hardcase(pass_rate, history)
    dedupe_key = (new_case["category"], prompt_hash(new_case["input"]))

    # Check dedup against existing history
    for existing in history:
        ex_key = (existing.get("category", ""), prompt_hash(existing.get("input", "")))
        if ex_key == dedupe_key:
            print(f"[META] ⏭️  Skipped — duplicate (category={new_case['category']})")
            write_status(patterns, blocked=False, injected=False)
            return False

    append_hardcase(new_case)

    print(f"[META] Category: {new_case['category']}")
    print(f"[META] Input:    {new_case['input'][:70]}...")

    # Recalculate patterns after injection
    history.append(new_case)
    updated_patterns = analyze_patterns(history)
    write_status(updated_patterns, blocked=False, injected=True)
    return True


def append_hardcase(case: dict):
    evals_dir = get_evals_dir()
    path = evals_dir / "hardcases.jsonl"
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(case, ensure_ascii=False) + "\n")
    rel = path.relative_to(get_project_root())
    print(f"[META] Hardcase appended: {rel}  [{case['id']}]")


if __name__ == "__main__":
    evolve_hardcases()
