#!/usr/bin/env python
"""
db-migrations v0.2.0 — Prisma Migration Runner (Cross-Platform)

Validates project structure, checks DATABASE_URL, runs
`npx prisma migrate deploy`, and logs results.

Usage:
    python db_migrate.py <project-dir>
"""

import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

CST = timezone(timedelta(hours=8))
LOG_FILE = Path("D:/bobo/skill-test.log")


def log(msg: str) -> None:
    ts = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [DB-MIGRATIONS-PRISMA] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def main() -> None:
    if len(sys.argv) < 2:
        log("Warning: No project directory provided. Skipping.")
        print("Usage: db-migrations <project-dir>")
        sys.exit(0)

    project_dir = Path(sys.argv[1]).resolve()

    print("=" * 50)
    print("  DB Migration Skill (Prisma Mode)")
    print("=" * 50)
    log(f"Starting Prisma Migration for: {project_dir}")

    # Validation
    if not project_dir.is_dir():
        log(f"Warning: Not a valid directory. Skipping.")
        print(f"Warning: {project_dir} is not a valid directory.")
        sys.exit(0)

    pkg_json = project_dir / "package.json"
    schema_prisma = project_dir / "prisma" / "schema.prisma"

    if not pkg_json.exists() or not schema_prisma.exists():
        log("Warning: Not a Prisma project (missing package.json or prisma/schema.prisma).")
        print("Warning: Not a Prisma project. Skipping.")
        sys.exit(0)

    # Environment check
    db_url = os.environ.get("DATABASE_URL", "")
    if not db_url:
        log("Warning: DATABASE_URL is not set. Skipping migration.")
        print("Warning: DATABASE_URL not set. Skipping.")
        sys.exit(0)

    # Mask password for display
    masked = re.sub(r"://.*?:.*?@", "://***:***@", db_url) if "@" in db_url else db_url[:20] + "..."
    log(f"DATABASE_URL: {masked}")

    # Run migration
    log("Running: npx prisma migrate deploy")
    print("Applying Prisma migrations...")

    try:
        result = subprocess.run(
            ["npx", "prisma", "migrate", "deploy"],
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=120,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
    except subprocess.TimeoutExpired:
        log("Error: Migration timed out (120s)")
        sys.exit(1)
    except FileNotFoundError:
        log("Error: npx not found. Is Node.js installed?")
        sys.exit(1)

    # Output
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    if stdout:
        print(stdout[-3000:])
    if stderr:
        print(stderr[-2000:], file=sys.stderr)

    # Log results
    if result.returncode == 0:
        log("Prisma migrations applied successfully.")
        print("Success: Database schema is up to date.")
    else:
        log(f"Prisma migration failed. Exit code: {result.returncode}")
        print("Migration failed. Check logs for details.")

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
