#!/usr/bin/env python
"""
create-skill v0.2.0 — Skill Factory with Context Snapshot

Scans the workspace for related code files, extracts patterns
(imports, exports, function signatures), and generates a new
skill skeleton (SKILL.md + _meta.json + run.sh) with an
embedded Context Snapshot section.

Usage:
    python create_skill.py <skill-name> <description> [target-dir]

Example:
    python create_skill.py image-resizer "Image resize utility" D:/bobo/openclaw-foreign/skills/openclaw-skills
"""

import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


# ─── config ────────────────────────────────────────────────────────────
DEFAULT_TARGET = "D:/bobo/openclaw-foreign/skills/openclaw-skills"
WORKSPACE_ROOT = "D:/bobo/openclaw-foreign/workspace/gh-enterprise-baseline"
SKIP_DIRS = {"node_modules", ".git", ".next", "dist", "build", "__pycache__", ".venv", "target"}
SCAN_EXTENSIONS = {".ts", ".tsx", ".py", ".js", ".jsx", ".rs", ".go", ".java"}
MAX_FILES_SCAN = 1000
MAX_CONTEXT_FILES = 10
MAX_PATTERNS_PER_FILE = 3
CST = timezone(timedelta(hours=8))


# ─── pattern extraction ───────────────────────────────────────────────
def find_relevant_files(root: Path, keywords: list[str]) -> list[Path]:
    """Walk workspace, return files whose content or name matches keywords."""
    results: list[Path] = []
    files_scanned = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        rel_dir = Path(dirpath).relative_to(root)
        # skip deeply nested noise
        if "test" in str(rel_dir).lower() or "spec" in str(rel_dir).lower():
            continue

        for fname in filenames:
            ext = os.path.splitext(fname)[1]
            if ext not in SCAN_EXTENSIONS:
                continue

            fpath = Path(dirpath) / fname
            files_scanned += 1
            if files_scanned > MAX_FILES_SCAN:
                break

            # quick filename match
            fname_lower = fname.lower()
            name_match = any(kw.lower() in fname_lower for kw in keywords)
            if name_match:
                results.append(fpath)
                continue

            # check first 2KB for keyword match
            try:
                head = fpath.read_text(encoding="utf-8", errors="replace")[:2048]
                if any(kw.lower() in head.lower() for kw in keywords):
                    results.append(fpath)
            except Exception:
                continue

        if files_scanned > MAX_FILES_SCAN:
            break

    return results[:MAX_CONTEXT_FILES]


IMPORT_RE = re.compile(r'^import\s+(.+?)(?:\s+from\s+[\'\"](.+?)[\'\"])?\s*$', re.MULTILINE)
FROM_IMPORT_RE = re.compile(r'^from\s+[\'\"](.+?)[\'\"]\s+import\s+(.+?)$', re.MULTILINE)
EXPORT_RE = re.compile(r'export\s+(?:default\s+)?(?:(?:const|let|var|function|class|interface|type|enum|async\s+function)\s+)?(\w+)', re.MULTILINE)
FUNC_RE = re.compile(r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)', re.MULTILINE)
CLASS_RE = re.compile(r'(?:export\s+)?class\s+(\w+)', re.MULTILINE)
PY_FUNC_RE = re.compile(r'def\s+(\w+)\s*\(([^)]*)\)', re.MULTILINE)
PY_CLASS_RE = re.compile(r'class\s+(\w+)', re.MULTILINE)


def extract_patterns(fpath: Path) -> dict:
    """Extract imports, exports, function signatures from a source file."""
    try:
        content = fpath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}
    data: dict[str, list[str]] = {"imports": [], "exports": [], "functions": [], "classes": []}
    ext = fpath.suffix.lower()
    if ext in (".ts", ".tsx", ".js", ".jsx"):
        for m in IMPORT_RE.finditer(content):
            data["imports"].append(m.group(0).strip())
        for m in FROM_IMPORT_RE.finditer(content):
            data["imports"].append(m.group(0).strip())
        for m in EXPORT_RE.finditer(content):
            name = m.group(1)
            if name not in ("default", "from", "if", "for", "while"):
                data["exports"].append(name)
        for m in FUNC_RE.finditer(content):
            data["functions"].append(f"{m.group(1)}({m.group(2)[:60]})")
        for m in CLASS_RE.finditer(content):
            data["classes"].append(m.group(1))
    elif ext == ".py":
        for m in PY_FUNC_RE.finditer(content):
            data["functions"].append(f"{m.group(1)}({m.group(2)[:60]})")
        for m in PY_CLASS_RE.finditer(content):
            data["classes"].append(m.group(1))
        for line in content.splitlines():
            s = line.strip()
            if s.startswith("import ") or s.startswith("from "):
                data["imports"].append(s[:80])
    return {k: v[:MAX_PATTERNS_PER_FILE] for k, v in data.items() if v}


# ─── context snapshot generator ────────────────────────────────────────
def build_context_snapshot(keywords: list[str]) -> str:
    """Scan workspace and return a markdown context snapshot."""
    root = Path(WORKSPACE_ROOT)
    if not root.exists():
        return "_Workspace not found — no context snapshot generated._\n"

    relevant = find_relevant_files(root, keywords)

    if not relevant:
        return "_No related code files found. The workspace may be empty or keywords didn't match._\n"

    lines = ["## Context Snapshot (auto-generated)\n"]
    lines.append(f"_Scanned {WORKSPACE_ROOT}_\n")

    for fpath in relevant:
        rel = fpath.relative_to(root)
        patterns = extract_patterns(fpath)
        if not any(patterns.values()):
            continue
        lines.append(f"### `{rel}`\n")
        if patterns.get("functions"):
            lines.append("**Functions:**\n")
            for fn in patterns["functions"]:
                lines.append(f"- `{fn}`\n")
        if patterns.get("classes"):
            lines.append("**Classes:**\n")
            for cls in patterns["classes"]:
                lines.append(f"- `{cls}`\n")
        if patterns.get("exports"):
            lines.append("**Exports:**\n")
            for exp in patterns["exports"]:
                lines.append(f"- `{exp}`\n")
        if patterns.get("imports"):
            lines.append("**Imports:**\n")
            for imp in patterns["imports"]:
                lines.append(f"- `{imp}`\n")

    if not lines[1:]:
        return "_Files found but no patterns extracted._\n"

    return "".join(lines)


# ─── file generators ───────────────────────────────────────────────────
def generate_skill_md(name: str, description: str, context: str) -> str:
    ts = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
    return f"""---
name: {name}
description: >
  {description}
metadata:
  openclaw:
    requires:
      bins: []
---

# {name}

## Description
{description}

{context}
## Usage

```bash
bash "{{baseDir}}/run.sh" "<argument>"
```

## Status
- **Created**: {ts}
- **Status**: stub (skeleton only, needs implementation)
"""


def generate_meta_json(name: str, description: str) -> str:
    return json.dumps({
        "name": name,
        "version": "0.1.0",
        "entrypoint": "./run.sh",
        "status": "stub",
        "description": description,
    }, indent=2, ensure_ascii=False) + "\n"


def generate_run_sh(name: str) -> str:
    return f"""#!/bin/bash
# Auto-generated by create-skill v0.2.0
# Skill: {name}
#
# INPUT – positional argument passed via CLI

INPUT="${{1}}"
echo "========================================="
echo "  Skill: {name}"
echo "========================================="
if [ -n "$INPUT" ]; then
  echo "  Input: $INPUT"
fi
echo ""
echo "Placeholder — implement actual logic here."
exit 0
"""


def generate_run_bat(name: str) -> str:
    return f"""@echo off
REM Auto-generated by create-skill v0.2.0
REM Skill: {name}
REM
REM Windows wrapper — delegates to bash (Git Bash / WSL) or falls back to python

set INPUT=%1
echo =========================================
echo   Skill: {name}
echo =========================================
if not "%INPUT%"=="" (
  echo   Input: %INPUT%
)
echo.
echo Placeholder - implement actual logic here.
exit /b 0
"""


# ─── main ──────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: create-skill <skill-name> <description> [target-dir]", file=sys.stderr)
        sys.exit(1)

    skill_name = sys.argv[1].strip().lower().replace(" ", "-")
    description = sys.argv[2] if len(sys.argv) > 2 else ""
    target = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_TARGET

    skill_dir = Path(target) / skill_name

    # Guard: already exists → warn but succeed (idempotent)
    if skill_dir.exists():
        print(f"⚠  Skill directory already exists: {skill_dir}")
        print("   Skipping. Delete it first to regenerate.")
        # Still exit 0 so health checks pass
        sys.exit(0)

    # Build context snapshot from description keywords
    kw_raw = re.split(r'[\s,;]+', description) if description else [skill_name]
    keywords = [k for k in kw_raw if len(k) > 2]
    if not keywords:
        keywords = [skill_name]
    context = build_context_snapshot(keywords)

    # Create directory
    skill_dir.mkdir(parents=True, exist_ok=True)

    # Write files
    (skill_dir / "SKILL.md").write_text(generate_skill_md(skill_name, description, context), encoding="utf-8")
    (skill_dir / "_meta.json").write_text(generate_meta_json(skill_name, description), encoding="utf-8")
    (skill_dir / "run.sh").write_text(generate_run_sh(skill_name), encoding="utf-8")
    (skill_dir / "run.bat").write_text(generate_run_bat(skill_name), encoding="utf-8")

    # Mark run.sh executable (no-op on Windows, works on WSL/Linux)
    try:
        os.chmod(skill_dir / "run.sh", 0o755)
    except Exception:
        pass

    print("=" * 50)
    print(f"  Skill created: {skill_name}")
    print("=" * 50)
    print(f"  Directory : {skill_dir}")
    print(f"  Files     : SKILL.md, _meta.json, run.sh, run.bat")
    print(f"  Status    : stub")
    print()
    print("  Next: Implement run.sh logic → update _meta.json status to 'implemented'")
    print()
    print("--- Context Snapshot ---")
    print(context)
    sys.exit(0)


if __name__ == "__main__":
    main()
