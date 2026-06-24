#!/usr/bin/env python3.
"""log-analyzer v0.2.0 — Parse and analyze log files for errors/warnings/patterns.

Usage:
  python run.py --file app.log --level ERROR
  python run.py --file access.log --top-errors 10
  python run.py --dry-run --json --version
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

__version__ = "0.2.0"

LEVEL_PATTERNS = {
    "ERROR": re.compile(r"(ERROR|FATAL|CRITICAL|FAIL)", re.IGNORECASE),
    "WARN": re.compile(r"(WARN|WARNING|DEPRECATED)", re.IGNORECASE),
    "INFO": re.compile(r"\bINFO\b", re.IGNORECASE),
    "ALL": re.compile(r"(ERROR|FATAL|CRITICAL|FAIL|WARN|WARNING|DEPRECATED|INFO|DEBUG|TRACE)", re.IGNORECASE),
}

TIME_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}")


def analyze_log(filepath: str, level: str = "ERROR", top: int = 10):
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}

    content = path.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()

    pattern = LEVEL_PATTERNS.get(level.upper(), LEVEL_PATTERNS["ALL"])
    matches = []
    error_counter: Counter = Counter()
    level_counts: Counter = Counter()
    first_ts = None
    last_ts = None

    for i, line in enumerate(lines, 1):
        ts_match = TIME_PATTERN.search(line)
        if ts_match:
            ts = ts_match.group()
            if first_ts is None:
                first_ts = ts
            last_ts = ts

        if pattern.search(line):
            matches.append({"line": i, "content": line[:200]})
            # Extract error type
            err_match = re.search(r"(Error|Exception|FAIL|FATAL)[:\s]*(\S+)", line)
            if err_match:
                error_counter[err_match.group(0)] += 1

            # Count by level
            for lvl in ["ERROR", "WARN", "INFO", "DEBUG"]:
                if re.search(rf"\b{lvl}\b", line, re.IGNORECASE):
                    level_counts[lvl] += 1
                    break

    return {
        "file": filepath,
        "total_lines": len(lines),
        "matched_lines": len(matches),
        "level_filter": level,
        "level_distribution": dict(level_counts.most_common()),
        "top_errors": error_counter.most_common(top),
        "time_range": f"{first_ts} → {last_ts}" if first_ts else "N/A",
        "sample_matches": matches[:top],
    }


def main():
    # Handle --version/--dry-run/--json before argparse required checks
    if "--version" in sys.argv:
        print(__version__)
        return

    if "--dry-run" in sys.argv or "--json" in sys.argv:
        flags = [a for a in sys.argv[1:] if a in ("--dry-run", "--json", "--version")]
        result = {"dry_run": "--dry-run" in flags, "file": None, "level": "ERROR", "actions": ["read", "parse", "aggregate"]}
        print(json.dumps(result) if "--json" in flags else "\ud83d\udd0d Log Analyzer dry-run \u2014 ready")
        return

    parser = argparse.ArgumentParser(description="Log Analyzer v0.2.0")
    parser.add_argument("--file", required=True, help="Log file path")
    parser.add_argument("--level", choices=["ERROR", "WARN", "INFO", "ALL"], default="ERROR")
    parser.add_argument("--top-errors", type=int, default=10)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print(__version__)
        return

    if args.dry_run:
        result = {"dry_run": True, "file": args.file, "level": args.level, "actions": ["read", "parse", "aggregate"]}
        print(json.dumps(result) if args.json else "🔍 Log Analyzer dry-run — ready")
        return

    result = analyze_log(args.file, args.level, args.top_errors)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n📊 Log Analysis: {args.file}")
        print(f"   Lines: {result['total_lines']}  |  Matched: {result['matched_lines']} ({args.level})")
        if result.get("time_range"):
            print(f"   Range: {result['time_range']}")
        if result.get("level_distribution"):
            print(f"   Distribution: {result['level_distribution']}")
        if result.get("top_errors"):
            print(f"\n   Top {min(args.top_errors, len(result['top_errors']))} errors:")
            for err, count in result["top_errors"]:
                print(f"     [{count}x] {err}")


if __name__ == "__main__":
    main()
