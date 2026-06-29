#!/usr/bin/env python
"""
self-coder v0.1.0 — AI Self-Modification Engine
=================================================
Reads a skill's SKILL.md + run.py, generates an optimized
draft in workspace/drafts/<skill>/run.py WITHOUT overwriting
the original file.

Usage:
    python self-coder/run.py <skill_name> [--api-key KEY]

Output:
    workspace/drafts/<skill>/run.py  (draft, never overwrites original)
"""

import argparse

# === V0.2.0 CLI STANDARD (auto-injected, do not remove) ===
VERSION = "0.2.0"
SKILL_NAME = "self-coder"
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
SKILLS_DIR = ROOT / "skills"
DRAFTS_DIR = ROOT / "workspace" / "drafts"
LOGS_DIR = ROOT / ".deploy" / "logs"

# DeepSeek API config
API_URL = "https://api.deepseek.com/chat/completions"
DEFAULT_MODEL = "deepseek-chat"


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def log_event(event_type: str, details: dict):
    ensure_dir(LOGS_DIR)
    log_file = LOGS_DIR / "selfcoder.jsonl"
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event_type,
        **details,
    }
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_skill(skill_name: str) -> dict:
    """Read SKILL.md and run.py for a given skill."""
    skill_dir = SKILLS_DIR / skill_name
    if not skill_dir.exists():
        raise FileNotFoundError(f"Skill '{skill_name}' not found at {skill_dir}")

    skill_md = skill_dir / "SKILL.md"
    run_py = skill_dir / "run.py"

    return {
        "skill_name": skill_name,
        "skill_md": skill_md.read_text(encoding="utf-8") if skill_md.exists() else "(no SKILL.md)",
        "run_py": run_py.read_text(encoding="utf-8") if run_py.exists() else "(no run.py)",
        "run_py_path": str(run_py),
    }


def build_prompt(skill_data: dict) -> str:
    """Build the LLM prompt for code optimization."""
    return f"""You are an expert Python code optimizer. Your task is to improve the following skill's run.py.

## Skill Description (SKILL.md)
{skill_data['skill_md']}

## Current Code (run.py)
```python
{skill_data['run_py']}
```

## Optimization Goals
1. Performance: Improve speed, reduce memory usage
2. Readability: Better variable names, add docstrings
3. Robustness: Better error handling, edge cases
4. Maintainability: Follow PEP 8, Type hints

## Output Format
Return ONLY the complete improved run.py code in a Python code block.
Do NOT include explanations. Do NOT remove existing functionality.
Output format:
```python
# Improved run.py for {skill_data['skill_name']}
... (complete code) ...
```
"""


def call_llm(prompt: str, api_key: str, model: str = DEFAULT_MODEL) -> str:
    """Call DeepSeek API to generate improved code."""
    import urllib.request
    import urllib.error

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a Python code optimizer. Return only the improved code in a Python code block. No explanations."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 4096,
    }).encode("utf-8")

    req = urllib.request.Request(API_URL, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    })

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            return content
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"API error {e.code}: {error_body}")


def extract_code(llm_response: str) -> str:
    """Extract Python code from LLM response."""
    # Try to find ```python ... ``` block
    match = re.search(r"```python\s*\n(.*?)```", llm_response, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Fallback: ``` ... ``` block
    match = re.search(r"```\s*\n(.*?)```", llm_response, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Fallback: entire response
    return llm_response.strip()


def save_draft(skill_name: str, code: str) -> Path:
    """Save improved code to workspace/drafts/<skill>/run.py"""
    draft_dir = DRAFTS_DIR / skill_name
    ensure_dir(draft_dir)
    draft_path = draft_dir / "run.py"
    draft_path.write_text(code, encoding="utf-8")
    return draft_path


def run_code_navigator(skill_name: str) -> dict:
    """Run code-navigator on the skill to get structure info."""
    navigator_path = SKILLS_DIR / "code-navigator" / "run.py"
    if not navigator_path.exists():
        return {"available": False, "reason": "code-navigator not installed"}

    try:
        result = subprocess.run(
            [sys.executable, str(navigator_path), "analyze", skill_name],
            capture_output=True, text=True, timeout=30,
            cwd=str(ROOT),
        )
        return {
            "available": True,
            "exit_code": result.returncode,
            "stdout": result.stdout[:2000],
            "stderr": result.stderr[:500],
        }
    except Exception as e:
        return {"available": True, "error": str(e)}


def optimize_with_rules(code: str, skill_name: str = "") -> str:
    """Apply optimization rules to Python code. Returns improved code."""
    lines = code.split('\n')
    new_lines = list(lines)
    changes = []

    # Rule 1: Add shebang if missing
    if lines and not lines[0].startswith('#!'):
        new_lines.insert(0, '#!/usr/bin/env python')
        changes.append("Added shebang")

    # Rule 2: Add docstring if missing (after shebang, before imports)
    has_docstring = any(True for line in lines[1:5] if line.strip().startswith('"""'))
    if not has_docstring and skill_name:
        idx = 1 if new_lines[0].startswith('#!') else 0
        new_lines[idx:idx] = [
            f'"""{skill_name} - Auto-optimized by self-coder"""',
            ''
        ]
        changes.append("Added docstring")

    result = '\n'.join(new_lines)

    # Rule 3: Add encoding to subprocess.run that lacks it
    if 'subprocess.run(' in result and 'encoding=' not in result:
        result = result.replace(
            'subprocess.run(\n',
            'subprocess.run(\n                encoding="utf-8", errors="replace",'
        )
        if 'subprocess.run(\n' in code and 'encoding=' not in code:
            changes.append("Added encoding=utf-8 to subprocess.run")

    # Rule 4: Fix datetime.UTC deprecation
    if 'datetime.UTC' in result:
        result = result.replace(
            'from datetime import datetime',
            'from datetime import datetime, timezone'
        )
        result = result.replace('datetime.UTC', 'timezone.utc')
        changes.append("Replaced datetime.UTC with timezone.utc")

    # Add changes log as comment
    if changes:
        comment = "# self-coder optimizations: " + ", ".join(changes)
        result = comment + '\n' + result

    return result


def main():
    parser = argparse.ArgumentParser(description="self-coder: AI Self-Modification Engine")
    parser.add_argument("skill", help="Skill name to optimize")
    parser.add_argument("--api-key", help="DeepSeek API key (or set # DISABLED (DEEPSEEK_API)_KEY env)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model to use")
    parser.add_argument("--dry-run", action="store_true", help="Show prompt but don't call API")
    parser.add_argument("--rules", action="store_true", help="Use rule engine instead of LLM (no API key needed)")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("# DISABLED (DEEPSEEK_API)_KEY")
    use_rules = args.rules
    if not api_key and not args.dry_run and not use_rules:
        print("[ERROR] API key required. Set # DISABLED (DEEPSEEK_API)_KEY env or pass --api-key", file=sys.stderr)
        sys.exit(1)

    print(f"╔══════════════════════════════════════════════════╗")
    print(f"║  self-coder v0.1.0 — AI Self-Modification Engine ║")
    print(f"╚══════════════════════════════════════════════════╝")
    print(f"\nTarget skill: {args.skill}")

    # ── Rules mode: no API needed ──
    if use_rules:
        print(f"\n  [rules] Applying optimization rules...")
        skill_data = read_skill(args.skill)
        improved = optimize_with_rules(skill_data['run_py'], args.skill)
        draft_path = save_draft(args.skill, improved)
        orig_lines = skill_data['run_py'].count('\n')
        impr_lines = improved.count('\n')
        print(f"  Original: {orig_lines} lines")
        print(f"  Improved: {impr_lines} lines ({impr_lines - orig_lines:+d})")
        print(f"  Draft saved to: {draft_path}")
        print(f"  Original UNTOUCHED: {skill_data['run_py_path']}")
        log_event("rules_optimized", {
            "skill": args.skill,
            "draft_path": str(draft_path),
            "original_lines": orig_lines,
            "improved_lines": impr_lines,
        })
        print(f"\n[DONE] Rules-based optimization for '{args.skill}'")
        return

    # ── LLM mode ──
    # Step 1: Read skill source
    print(f"\n[1/5] Reading skill '{args.skill}'...")
    skill_data = read_skill(args.skill)
    print(f"  SKILL.md: {len(skill_data['skill_md'])} chars")
    print(f"  run.py:   {len(skill_data['run_py'])} chars")

    # Step 2: Run code-navigator for structure analysis
    print(f"\n[2/5] Running code-navigator...")
    nav_result = run_code_navigator(args.skill)
    if nav_result["available"]:
        if nav_result.get("error"):
            print(f"  Code-navigator error: {nav_result['error']}")
        else:
            print(f"  Code-navigator exit: {nav_result['exit_code']}")
            if nav_result["stdout"]:
                print(f"  Structure analysis available ({len(nav_result['stdout'])} chars)")
    else:
        print(f"  Code-navigator not available, proceeding without structure analysis")

    # Step 3: Build prompt
    print(f"\n[3/5] Building optimization prompt...")
    prompt = build_prompt(skill_data)
    print(f"  Prompt size: {len(prompt)} chars")

    if args.dry_run:
        draft_path = DRAFTS_DIR / args.skill / "prompt.txt"
        ensure_dir(draft_path.parent)
        draft_path.write_text(prompt, encoding="utf-8")
        print(f"  Prompt saved to: {draft_path}")
        print(f"\n[DONE] Dry-run complete. No API call made.")
        return

    # Step 4: Call LLM
    print(f"\n[4/5] Calling LLM ({args.model})...")
    try:
        llm_response = call_llm(prompt, api_key, args.model)
        print(f"  Response: {len(llm_response)} chars")
    except RuntimeError as e:
        print(f"  API call failed: {e}", file=sys.stderr)
        log_event("api_error", {"skill": args.skill, "error": str(e)})
        sys.exit(1)

    # Step 5: Extract code and save draft
    print(f"\n[5/5] Extracting code and saving draft...")
    improved_code = extract_code(llm_response)
    draft_path = save_draft(args.skill, improved_code)

    print(f"  Draft saved to: {draft_path}")
    print(f"  Draft size: {len(improved_code)} chars")
    print(f"  Original file UNTOUCHED: {skill_data['run_py_path']}")

    # Diff stats
    original_lines = skill_data['run_py'].count('\n')
    improved_lines = improved_code.count('\n')
    print(f"\n  Original: {original_lines} lines")
    print(f"  Improved: {improved_lines} lines")
    print(f"  Delta: {improved_lines - original_lines:+d} lines")

    log_event("draft_generated", {
        "skill": args.skill,
        "draft_path": str(draft_path),
        "original_lines": original_lines,
        "improved_lines": improved_lines,
    })

    print(f"\n{'=' * 50}")
    print(f"DRAFT PREVIEW (first 40 lines):")
    print(f"{'=' * 50}")
    for line in improved_code.split('\n')[:40]:
        print(line)
    if improved_lines > 40:
        print(f"... ({improved_lines - 40} more lines)")

    print(f"\n[DONE] self-coder completed for '{args.skill}'")


if __name__ == "__main__":
    main()
