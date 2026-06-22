#!/usr/bin/env python
"""
code-navigator v0.2.0 — Symbolic Code Navigation

Deep search across TypeScript/JavaScript/Python source tree.
Finds function definitions, class declarations, interface types,
export symbols, import dependencies — with file:line references.

Usage:
    python code_navigator.py <project-dir> <symbol> [--type func|class|interface|export|import|all] [--fuzzy]

Examples:
    python code_navigator.py D:/project createRun
    python code_navigator.py D:/project AgentBackend --type class
    python code_navigator.py D:/project "handle|on" --fuzzy --type func
"""

import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


CST = timezone(timedelta(hours=8))
SKIP_DIRS = {"node_modules", ".git", ".next", "dist", "build", "__pycache__", ".venv", "target", "coverage", ".turbo"}
SCAN_EXTENSIONS = {".ts", ".tsx", ".py", ".js", ".jsx", ".mjs", ".cjs", ".mts", ".cts"}


# ─── Pattern Matchers ──────────────────────────────────────────────────
# TS/JS matchers
TS_FUNC = re.compile(r'(?:export\s+(?:default\s+)?)?(?:async\s+)?function\s+(\w+)\s*(<[^>]*>)?\s*\(([^)]*)\)(?:\s*:\s*(\S+(?:\s*<[^>]*>)?(?:\s*\[\])?))?', re.MULTILINE)
TS_ARROW = re.compile(r'(?:export\s+(?:const|let|var)\s+)?(\w+)\s*(?:<[^>]*>)?\s*=\s*(?:async\s+)?\(([^)]*)\)(?:\s*:\s*(\S+(?:\s*<[^>]*>)?))?\s*=>', re.MULTILINE)
TS_CONST_FUNC = re.compile(r'(?:export\s+)?(?:const|let|var)\s+(\w+)\s*(?:<[^>]*>)?\s*:\s*(?:\(\s*(?:(?:\{[^}]*\}|[^)])+)\)\s*=>\s*\S+|(?:React\.)?FC|Function)', re.MULTILINE)
TS_CLASS = re.compile(r'(?:export\s+(?:default\s+)?)?(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([^{]+))?', re.MULTILINE)
TS_INTERFACE = re.compile(r'(?:export\s+(?:default\s+)?)?interface\s+(\w+)(?:\s+extends\s+([^{]+))?', re.MULTILINE)
TS_TYPE = re.compile(r'(?:export\s+)?type\s+(\w+)(?:\s*<[^>]*>)?\s*=\s*', re.MULTILINE)
TS_ENUM = re.compile(r'(?:export\s+(?:default\s+)?)?enum\s+(\w+)', re.MULTILINE)
TS_IMPORT = re.compile(r'^import\s+(.+?)(?:\s+from\s+[\'\"](.+?)[\'\"])?\s*;?\s*$', re.MULTILINE)
TS_FROM_IMPORT = re.compile(r'^(?:import\s+)?type\s+\{?\s*([^}]+)\s*\}?\s+from\s+[\'\"](.+?)[\'\"]\s*;?$', re.MULTILINE)
TS_EXPORT_NAMED = re.compile(r'export\s+\{\s*([^}]+)\s*\}', re.MULTILINE)
TS_EXPORT_DEFAULT = re.compile(r'export\s+default\s+(?:function|class|const|let|var)?\s*(\w*)', re.MULTILINE)

# Python matchers
PY_FUNC = re.compile(r'(?:async\s+)?def\s+(\w+)\s*\(([^)]*)\)(?:\s*->\s*(\S+))?', re.MULTILINE)
PY_CLASS = re.compile(r'class\s+(\w+)(?:\s*\(\s*([^)]*)\s*\))?', re.MULTILINE)
PY_IMPORT = re.compile(r'^(?:from\s+(\S+)\s+)?import\s+(.+)$', re.MULTILINE)


# ─── Symbol Extraction ─────────────────────────────────────────────────
def extract_symbols(filepath: Path) -> list[dict]:
    """Extract all symbols from a single file."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    lines = content.splitlines()
    ext = filepath.suffix.lower()
    matches: list[dict] = []

    if ext in (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".mts", ".cts"):
        _match(matches, filepath, lines, content, TS_FUNC, "function", group_idx=1)
        _match(matches, filepath, lines, content, TS_ARROW, "function", group_idx=1)
        _match(matches, filepath, lines, content, TS_CONST_FUNC, "function", group_idx=1)
        _match(matches, filepath, lines, content, TS_CLASS, "class", group_idx=1)
        _match(matches, filepath, lines, content, TS_INTERFACE, "interface", group_idx=1)
        _match(matches, filepath, lines, content, TS_TYPE, "type", group_idx=1)
        _match(matches, filepath, lines, content, TS_ENUM, "enum", group_idx=1)
        _match(matches, filepath, lines, content, TS_IMPORT, "import", group_idx=0)
        _match(matches, filepath, lines, content, TS_FROM_IMPORT, "import", group_idx=0)
        _match(matches, filepath, lines, content, TS_EXPORT_NAMED, "export", group_idx=0)
        _match(matches, filepath, lines, content, TS_EXPORT_DEFAULT, "export", group_idx=0)

    elif ext == ".py":
        _match(matches, filepath, lines, content, PY_FUNC, "function", group_idx=1)
        _match(matches, filepath, lines, content, PY_CLASS, "class", group_idx=1)
        _match(matches, filepath, lines, content, PY_IMPORT, "import", group_idx=0)

    return matches


def _match(matches: list, filepath: Path, lines: list[str], content: str, pattern: re.Pattern, kind: str, group_idx: int):
    for m in pattern.finditer(content):
        line_no = content[:m.start()].count("\n") + 1
        snippet = lines[line_no - 1].strip()[:160]
        if group_idx == 0:
            name = m.group(0).strip()[:120]
        else:
            name = m.group(group_idx) or ""
        if not name:
            continue
        matches.append({
            "kind": kind,
            "name": name,
            "file": str(filepath),
            "line": line_no,
            "snippet": snippet,
        })


# ─── Walk & Search ─────────────────────────────────────────────────────
def walk_and_search(root: Path, symbol: str, kind_filter: str | None, fuzzy: bool) -> list[dict]:
    """Recursively scan source tree, extract symbols, filter by query."""
    results: list[dict] = []
    files_scanned = 0
    MAX_FILES = 2000

    pattern = re.compile(re.escape(symbol), re.IGNORECASE) if symbol else None

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            ext = os.path.splitext(fname)[1]
            if ext not in SCAN_EXTENSIONS:
                continue
            files_scanned += 1
            if files_scanned > MAX_FILES:
                break

            fpath = Path(dirpath) / fname

            # Quick pre-filter on file content (first 4KB) for large files
            if pattern and files_scanned > 100:
                try:
                    head = fpath.read_text(encoding="utf-8", errors="replace")[:4096]
                    if not pattern.search(head):
                        continue
                except Exception:
                    continue

            symbols = extract_symbols(fpath)
            for s in symbols:
                if kind_filter and s["kind"] != kind_filter:
                    continue
                if symbol:
                    if fuzzy:
                        if not pattern or not pattern.search(s["name"]):
                            continue
                    else:
                        if s["name"].lower() != symbol.lower():
                            continue
                results.append(s)

        if files_scanned > MAX_FILES:
            break

    return results


# ─── Output ─────────────────────────────────────────────────────────────
def print_json(results: list[dict]) -> None:
    print(json.dumps(results, indent=2, ensure_ascii=False))


def print_table(results: list[dict]) -> None:
    ts = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 80)
    print(f"  Code Navigator v0.2.0  |  {ts}")
    print("=" * 80)

    # Summary by kind
    counts: dict[str, int] = {}
    for r in results:
        counts[r["kind"]] = counts.get(r["kind"], 0) + 1
    summary = ", ".join(f"{v} {k}{'s' if v > 1 else ''}" for k, v in sorted(counts.items()))
    print(f"  Found: {len(results)} symbols ({summary})")
    print()

    # Group by file
    from collections import defaultdict
    grouped: dict[str, list] = defaultdict(list)
    for r in results:
        grouped[r["file"]].append(r)

    for fpath, symbols in grouped.items():
        rel = Path(fpath).name
        print(f"  📄 {fpath}")
        for s in symbols:
            icon = {"function": "🔧", "class": "🏛️", "interface": "📐", "type": "🏷️", "enum": "📦", "import": "📥", "export": "📤"}.get(s["kind"], "❓")
            print(f"     {icon} L{s['line']:>4} [{s['kind']}] {s['name']}")
            if any(c for c in s["snippet"] if c.islower() if c.lower() != s["name"][0].lower()):
                preview = s["snippet"][:100]
                print(f"            {preview}")
        print()

    # Summary
    print("=" * 80)
    print(f"  Total: {len(results)} matches across {len(grouped)} files")
    print("=" * 80)


# ─── Main ───────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: code-navigator <project-dir> [symbol] [--type func|class|interface|export|import|all] [--fuzzy] [--json]", file=sys.stderr)
        sys.exit(1)

    project_dir = Path(sys.argv[1]).resolve()
    symbol = ""
    kind_filter = None
    fuzzy = False
    output_json = False

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--type" and i + 1 < len(sys.argv):
            kind_filter = sys.argv[i + 1]
            if kind_filter == "all":
                kind_filter = None
            i += 2
        elif arg == "--fuzzy":
            fuzzy = True
            i += 1
        elif arg == "--json":
            output_json = True
            i += 1
        elif not arg.startswith("--"):
            symbol = arg
            i += 1
        else:
            i += 1

    if not project_dir.is_dir():
        print(f"ERROR: Directory not found: {project_dir}", file=sys.stderr)
        sys.exit(1)

    results = walk_and_search(project_dir, symbol, kind_filter, fuzzy)

    if output_json:
        print_json(results)
    else:
        print_table(results)

    sys.exit(0 if results else 1)


if __name__ == "__main__":
    main()
