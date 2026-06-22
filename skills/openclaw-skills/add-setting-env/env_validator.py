#!/usr/bin/env python
"""
add-setting-env v0.2.0 — Environment Variable Validator

Scans a project directory for .env.example (or .env.template),
compares required variables against actual .env, and reports
missing or mismatched variables.

Usage:
    python env_validator.py <project-dir>
"""

import os
import re
import sys
from pathlib import Path


def parse_env_vars(filepath: Path) -> dict[str, str | None]:
    """Parse KEY=VALUE or KEY= lines from an env file. Returns {KEY: VALUE or None}."""
    if not filepath.exists():
        return {}
    vars_: dict[str, str | None] = {}
    for line in filepath.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        m = re.match(r'^(\w+)\s*=\s*(.*)', s)
        if m:
            vars_[m.group(1)] = m.group(2).strip() or None
    return vars_


def find_env_files(project_dir: Path) -> list[dict]:
    """Walk project tree, find .env / .env.example / .env.template pairs."""
    results: list[dict] = []
    # Check root level
    env_example = None
    for candidate in [".env.example", ".env.template", ".env.defaults"]:
        p = project_dir / candidate
        if p.exists():
            env_example = p
            break

    env_file = project_dir / ".env"
    if not env_file.exists():
        # recursive check
        env_local = project_dir / ".env.local"
        if env_local.exists():
            env_file = env_local

    if env_example and env_file.exists():
        results.append({
            "location": str(project_dir),
            "example": env_example,
            "env": env_file,
        })
    elif env_example:
        results.append({
            "location": str(project_dir),
            "example": env_example,
            "env": None,
        })

    # Check one level deep (monorepo sub-projects)
    for child in project_dir.iterdir():
        if not child.is_dir() or child.name.startswith(".") or child.name == "node_modules":
            continue
        for candidate in [".env.example", ".env.template"]:
            ex = child / candidate
            if not ex.exists():
                continue
            env = child / ".env"
            env_local = child / ".env.local"
            results.append({
                "location": str(child),
                "example": ex,
                "env": env if env.exists() else (env_local if env_local.exists() else None),
            })
            break

    return results


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: add-setting-env <project-dir>", file=sys.stderr)
        sys.exit(1)

    project_dir = Path(sys.argv[1]).resolve()
    if not project_dir.is_dir():
        print(f"ERROR: Directory not found: {project_dir}", file=sys.stderr)
        sys.exit(1)

    env_pairs = find_env_files(project_dir)

    if not env_pairs:
        print("No .env.example or .env.template found in the project.")
        print("Nothing to validate. Create a .env.example with required variables.")
        sys.exit(0)

    print("=" * 60)
    print("  Environment Variable Validator v0.2.0")
    print("=" * 60)
    print(f"  Project: {project_dir}")
    print()

    total_missing = 0
    total_present = 0

    for pair in env_pairs:
        location = pair["location"]
        example_vars = parse_env_vars(pair["example"])
        env_vars = parse_env_vars(pair["env"]) if pair["env"] else {}

        if not example_vars:
            print(f"[{location}] .env.example is empty — nothing to validate.")
            continue

        print(f"--- {location} ---")
        missing = {}
        present = {}
        masked = {}

        for key, default_val in example_vars.items():
            if key in env_vars:
                # Mask sensitive values
                val = env_vars[key] or ""
                if any(s in key.upper() for s in ["SECRET", "KEY", "TOKEN", "PASSWORD", "PWD"]):
                    masked[key] = val[:4] + "***" if len(val) > 4 else "***"
                else:
                    masked[key] = val
                present[key] = val
            else:
                missing[key] = default_val

        if missing:
            print(f"  MISSING ({len(missing)}):")
            for k, default in missing.items():
                hint = f" (default: {default})" if default else ""
                print(f"    - {k}{hint}")
            total_missing += len(missing)

        if present:
            print(f"  PRESENT ({len(present)}):")
            for k, v in masked.items():
                print(f"    + {k}={v}")
            total_present += len(present)

        if not pair["env"]:
            print(f"  WARNING: .env file does not exist at this location!")
        print()

    # Summary
    print("=" * 60)
    print(f"  Total missing : {total_missing}")
    print(f"  Total present : {total_present}")
    print(f"  Coverage      : {_pct(total_present, total_present + total_missing)}")
    print("=" * 60)

    # Non-zero exit if any missing
    if total_missing > 0:
        print()
        print("To fix: add the missing variables to your .env file.")
        print("Copy from .env.example and fill in the values.")
        sys.exit(1)
    else:
        print("All required environment variables are set.")
        sys.exit(0)


def _pct(part: int, total: int) -> str:
    if total == 0:
        return "N/A"
    return f"{part / total * 100:.0f}%"


if __name__ == "__main__":
    main()
