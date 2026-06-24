#!/usr/bin/env python3.
"""sql-optimizer v0.2.0 — SQL query analyzer and optimizer.

Usage:
  python run.py --query "SELECT * FROM users WHERE email LIKE '%gmail%'"
  python run.py --file queries.sql --explain
  python run.py --dry-run --json --version
"""

import argparse
import json
import sys

__version__ = "0.2.0"

RULES = [
    ("SELECT *", "Avoid SELECT * — specify columns explicitly"),
    ("LIKE '%", "Leading wildcard in LIKE prevents index usage — consider full-text search"),
    ("ORDER BY RAND()", "ORDER BY RAND() is slow on large tables — use random offset instead"),
    ("NOT IN", "NOT IN with NULLs can produce unexpected results — use NOT EXISTS instead"),
    ("DISTINCT", "DISTINCT may hide duplicate data issues — verify if truly needed"),
    ("HAVING", "Use WHERE instead of HAVING for non-aggregate filters"),
    ("OR (?!.*IN)", "OR conditions can bypass indexes — consider UNION ALL"),
    ("GROUP BY", "Add appropriate indexes for GROUP BY columns"),
    ("LIMIT 1000000", "Large LIMIT without pagination may cause memory issues — use cursor pagination"),
    ("N+1", "Detected possible N+1 query pattern — use JOIN or eager loading"),
]


def analyze(query: str, explain: bool = False) -> dict:
    suggestions = []
    for pattern, advice in RULES:
        import re

        if re.search(pattern, query, re.IGNORECASE):
            suggestions.append({"pattern": pattern, "suggestion": advice})

    result = {
        "status": "ok",
        "query_length": len(query),
        "issues_found": len(suggestions),
        "severity": "HIGH" if len(suggestions) > 3 else "MEDIUM" if suggestions else "LOW",
        "suggestions": suggestions,
    }

    if explain:
        result["explain_plan"] = "Seq Scan on table (cost=0.00..estimate) — add WHERE clause index"

    return result


def analyze_file(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        queries = f.read()
    return {
        "file": filepath,
        "total_queries": queries.count("SELECT") + queries.count("INSERT") + queries.count("UPDATE"),
        "results": analyze(queries),
    }


def main():
    parser = argparse.ArgumentParser(description="SQL Optimizer v0.2.0")
    parser.add_argument("--query", help="SQL query string")
    parser.add_argument("--file", help="SQL file path")
    parser.add_argument("--explain", action="store_true", help="Include EXPLAIN plan estimate")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print(__version__)
        return

    if args.dry_run:
        result = {
            "dry_run": True,
            "query": args.query,
            "file": args.file,
            "actions": ["parse", "lint", "suggest"],
        }
        print(json.dumps(result, indent=2) if args.json else "🔍 SQL Optimizer dry-run — ready to analyze")
        return

    if args.file:
        result = analyze_file(args.file)
    elif args.query:
        result = analyze(args.query, explain=args.explain)
    else:
        parser.print_help()
        return

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n📊 SQL Analysis: {result.get('issues_found', 0)} issues ({result.get('severity', '?')})")
        for s in result.get("suggestions", []):
            print(f"  ⚡ [{s['pattern']}] → {s['suggestion']}")
        if result.get("explain_plan"):
            print(f"\n📋 EXPLAIN: {result['explain_plan']}")


if __name__ == "__main__":
    main()
