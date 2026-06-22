#!/usr/bin/env python
"""
frontend-code-review v0.2.0 — ESLint-Powered Frontend Code Review

Runs ESLint, parses JSON output, enriches with symbol cross-references
from code-navigator, and produces a human-readable audit report with
fix suggestions.

Two modes:
  --file <path>   Quick single-file review
  --src <dir>     Deep scan of entire source directory

Usage:
    python code_review.py --file src/components/Login.tsx
    python code_review.py --src src/ --format json|text|markdown
"""

import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path


CST = timezone(timedelta(hours=8))

# ═══════════════════════════════════════════════════════════════════════
# Configuration Scanner
# ═══════════════════════════════════════════════════════════════════════

def scan_project_config(project_dir: Path) -> dict:
    """Extract project configuration context."""
    config = {
        "eslint_configs": [],
        "dependencies": {},
        "framework": "unknown",
        "typescript": False,
        "react_version": None,
    }

    # Find eslint configs
    for candidate in [".eslintrc.js", ".eslintrc.cjs", ".eslintrc.json", ".eslintrc.yaml",
                       ".eslintrc.yml", "eslint.config.js", "eslint.config.mjs", "eslint.config.cjs"]:
        p = project_dir / candidate
        if p.exists():
            config["eslint_configs"].append(candidate)
            try:
                content = p.read_text(encoding="utf-8", errors="replace")
                config["eslint_rules_summary"] = _summarize_eslint_rules(content)
            except Exception:
                pass

    # Parse package.json
    pkg = project_dir / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            all_deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            relevant = ["eslint", "prettier", "typescript", "react", "next", "@typescript-eslint",
                        "eslint-plugin-react", "eslint-plugin-react-hooks", "eslint-config-next"]
            for key in relevant:
                if key in all_deps:
                    config["dependencies"][key] = all_deps[key]
            if "react" in all_deps:
                config["framework"] = "react"
                config["react_version"] = all_deps["react"].lstrip("^~")
            if "next" in all_deps:
                config["framework"] = "next.js"
            if "typescript" in all_deps:
                config["typescript"] = True
        except Exception:
            pass

    return config


def _summarize_eslint_rules(content: str) -> str:
    """Extract key rule patterns from eslint config."""
    rules = re.findall(r"['\"](\S+?)['\"]\s*:\s*['\"](error|warn|off)['\"]", content)
    if not rules:
        rules = re.findall(r"['\"](\S+?)['\"]\s*:\s*\[.*?['\"](error|warn|off)", content)
    if not rules:
        return "custom rules (unable to parse)"
    error_count = sum(1 for _, s in rules if s == "error")
    warn_count = sum(1 for _, s in rules if s == "warn")
    return f"{len(rules)} rules ({error_count} error, {warn_count} warn)"


# ═══════════════════════════════════════════════════════════════════════
# ESLint Runner
# ═══════════════════════════════════════════════════════════════════════

def run_eslint(target: Path, project_dir: Path, quiet: bool = False) -> list[dict]:
    """Execute ESLint and return parsed JSON results."""
    cmd = ["npx", "eslint", "--format=json"]

    if not target.is_dir():
        cmd.append(str(target))
    else:
        # Scan src with TS/TSX extensions
        cmd.extend([
            str(target),
            "--ext", ".ts,.tsx,.js,.jsx",
        ])

    try:
        result = subprocess.run(
            cmd,
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=120,
            env={**os.environ, "PYTHONIOENCODING": "utf-8", "CI": "true"},
        )
    except subprocess.TimeoutExpired:
        return [{"_error": "ESLint timed out (120s)"}]
    except FileNotFoundError:
        return [{"_error": "ESLint not found. Run: npm install eslint --save-dev"}]

    # ESLint sometimes writes to stderr even on success (warnings)
    output = result.stdout.strip()
    if not output:
        # Try stderr for non-JSON output
        if result.stderr.strip():
            return [{"_error": f"ESLint error: {result.stderr[:500]}"}]
        return []

    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return [{"_error": f"ESLint returned non-JSON output: {output[:500]}"}]

    return data


# ═══════════════════════════════════════════════════════════════════════
# Symbol Cross-Reference (code-navigator integration)
# ═══════════════════════════════════════════════════════════════════════

# Inline symbol extractor (lightweight, no subprocess call to code-navigator)
FUNC_DEF_RE = re.compile(
    r'(?:export\s+(?:default\s+)?)?(?:async\s+)?function\s+(\w+)', re.MULTILINE)
ARROW_DEF_RE = re.compile(
    r'(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(', re.MULTILINE)
TS_CLASS_DEF_RE = re.compile(
    r'(?:export\s+(?:default\s+)?)?class\s+(\w+)', re.MULTILINE)


def find_symbol_definition(project_dir: Path, symbol_name: str) -> dict | None:
    """Quick symbol lookup across project source files."""
    src_dir = project_dir / "src"
    if not src_dir.is_dir():
        src_dir = project_dir

    pattern = re.compile(re.escape(symbol_name))
    for dirpath, dirnames, filenames in os.walk(src_dir):
        dirnames[:] = [d for d in dirnames if d not in {"node_modules", ".git", ".next", "dist", "build"}]
        for fname in filenames:
            if not fname.endswith((".ts", ".tsx", ".js", ".jsx")):
                continue
            fpath = Path(dirpath) / fname
            try:
                content = fpath.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if not pattern.search(content):
                continue
            lines = content.splitlines()
            for i, line in enumerate(lines, 1):
                ts_match = FUNC_DEF_RE.search(line) or ARROW_DEF_RE.search(line) or TS_CLASS_DEF_RE.search(line)
                if ts_match and ts_match.group(1) == symbol_name:
                    return {
                        "file": str(fpath.relative_to(project_dir)),
                        "line": i,
                        "snippet": line.strip()[:120],
                    }
        # Limit walk depth
        if len(list(Path(dirpath).parents)) > 8:
            break
    return None


# ═══════════════════════════════════════════════════════════════════════
# Fix Suggestions
# ═══════════════════════════════════════════════════════════════════════

SUGGESTION_MAP = {
    "no-unused-vars": "Remove unused variable or prefix with '_' to indicate intentional unused.",
    "@typescript-eslint/no-unused-vars": "Remove unused variable or prefix with '_'.",
    "no-console": "Replace console.log with a proper logging library or remove before production.",
    "react-hooks/exhaustive-deps": "Add missing dependencies to the dependency array, or wrap in useCallback/useMemo.",
    "react/prop-types": "Add PropTypes validation or use TypeScript interface instead.",
    "@typescript-eslint/no-explicit-any": "Replace 'any' with a proper type or interface.",
    "import/no-unresolved": "Check the import path — the module may not exist or needs to be installed.",
    "prefer-const": "Use 'const' instead of 'let' when the variable is never reassigned.",
    "no-undef": "Variable is not defined — check for typos or add a proper import.",
    "@typescript-eslint/no-non-null-assertion": "Use optional chaining (?.) or a null check instead of '!'.",
    "no-empty": "Add a comment explaining why the block is empty, or remove it.",
    "no-unused-expressions": "Assign the expression to a variable or refactor to use it.",
}


def get_suggestion(rule_id: str, message: str, symbol: str = "") -> str:
    """Get a context-aware fix suggestion."""
    base = SUGGESTION_MAP.get(rule_id, "")
    if not base:
        base = f"Review this ESLint rule violation: {message}"

    if symbol:
        base = f"[{symbol}] {base}"

    return base


# ═══════════════════════════════════════════════════════════════════════
# Report Formatter
# ═══════════════════════════════════════════════════════════════════════

SEVERITY_ICONS = {2: "🔴", 1: "🟡", 0: "⚪"}
SEVERITY_LABELS = {2: "ERROR", 1: "WARNING", 0: "OFF"}


def _render_text(report: dict) -> str:
    """Render a human-readable text report."""
    lines = []
    lines.append("=" * 80)
    lines.append(f"  📋 Frontend Code Review Report")
    lines.append(f"  {datetime.now(CST).strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 80)

    # Project context
    ctx = report.get("project_context", {})
    if ctx:
        lines.append("")
        lines.append("--- Project Context ---")
        lines.append(f"  Framework     : {ctx.get('framework', 'unknown')}")
        if ctx.get("react_version"):
            lines.append(f"  React         : v{ctx['react_version']}")
        if ctx.get("typescript"):
            lines.append(f"  TypeScript    : yes")
        deps = ctx.get("dependencies", {})
        if deps.get("eslint"):
            lines.append(f"  ESLint        : {deps['eslint']}")
        if deps.get("prettier"):
            lines.append(f"  Prettier      : {deps['prettier']}")
        eslint_cfg = ctx.get("eslint_configs", [])
        if eslint_cfg:
            lines.append(f"  Config        : {', '.join(eslint_cfg)}")
        if ctx.get("eslint_rules_summary"):
            lines.append(f"  Rules         : {ctx['eslint_rules_summary']}")

    # Summary
    summary = report.get("summary", {})
    lines.append("")
    lines.append("--- Summary ---")
    lines.append(f"  Files scanned : {summary.get('files_scanned', 0)}")
    lines.append(f"  Files with issues : {summary.get('files_with_issues', 0)}")
    lines.append(f"  Errors        : {summary.get('errors', 0)}")
    lines.append(f"  Warnings      : {summary.get('warnings', 0)}")
    lines.append(f"  Total issues  : {summary.get('total_issues', 0)}")

    # Score
    score = summary.get("score", "N/A")
    score_color = "🟢" if isinstance(score, (int, float)) and score >= 90 else ("🟡" if isinstance(score, (int, float)) and score >= 70 else "🔴")
    lines.append(f"  Score         : {score_color} {score}/100")

    # Issues detail
    issues = report.get("issues", [])
    if issues:
        lines.append("")
        lines.append("--- Issues Detail ---")
        current_file = None
        for issue in issues:
            fpath = issue.get("filePath", "")
            if fpath != current_file:
                current_file = fpath
                lines.append("")
                lines.append(f"  📄 {fpath}")

            severity = issue.get("severity", 2)
            icon = SEVERITY_ICONS.get(severity, "❓")
            label = SEVERITY_LABELS.get(severity, "??")

            msg = issue.get("message", "")
            rule = issue.get("ruleId", "?")
            line_no = issue.get("line", "?")
            col = issue.get("column", "?")

            lines.append(f"     {icon} L{line_no}:{col} [{rule}] {msg}")

            # Symbol cross-reference
            symbol_ref = issue.get("symbol_ref")
            if symbol_ref:
                lines.append(f"         → Defined at: {symbol_ref['file']}:{symbol_ref['line']}")
                lines.append(f"            {symbol_ref['snippet']}")

            # Fix suggestion
            suggestion = issue.get("suggestion", "")
            if suggestion:
                lines.append(f"         💡 Fix: {suggestion}")

    # Affected symbols
    affected = report.get("affected_symbols", [])
    if affected:
        lines.append("")
        lines.append("--- Affected Symbols ---")
        for sym in affected[:15]:
            lines.append(f"  • {sym['name']} ({sym['kind']}) — {sym['file']}:{sym['line']}")

    lines.append("")
    lines.append("=" * 80)
    return "\n".join(lines)


def _render_json(report: dict) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False)


def _render_markdown(report: dict) -> str:
    """Render a markdown report (for PR comments)."""
    lines = []
    ctx = report.get("project_context", {})
    summary = report.get("summary", {})

    lines.append("# 📋 Frontend Code Review")
    lines.append("")
    lines.append(f"**Framework:** {ctx.get('framework', 'unknown')} | "
                 f"**ESLint:** {ctx.get('dependencies', {}).get('eslint', 'N/A')} | "
                 f"**Date:** {datetime.now(CST).strftime('%Y-%m-%d')}")
    lines.append("")

    score = summary.get("score", "N/A")
    score_emoji = "✅" if isinstance(score, (int, float)) and score >= 90 else ("⚠️" if isinstance(score, (int, float)) and score >= 70 else "❌")
    lines.append(f"## Score: {score_emoji} {score}/100")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Files scanned | {summary.get('files_scanned', 0)} |")
    lines.append(f"| Files with issues | {summary.get('files_with_issues', 0)} |")
    lines.append(f"| Errors | {summary.get('errors', 0)} |")
    lines.append(f"| Warnings | {summary.get('warnings', 0)} |")
    lines.append("")

    issues = report.get("issues", [])
    if issues:
        lines.append("## Issues")
        lines.append("")
        lines.append("| File | Line | Rule | Message | Fix |")
        lines.append("|------|------|------|---------|-----|")
        for issue in issues:
            fpath = Path(issue.get("filePath", "")).name
            line_no = issue.get("line", "?")
            rule = issue.get("ruleId", "?")
            msg = issue.get("message", "")[:80]
            suggestion = issue.get("suggestion", "")[:60]
            icon = "🔴" if issue.get("severity") == 2 else "🟡"
            lines.append(f"| {fpath} | {line_no} | `{rule}` | {icon} {msg} | {suggestion} |")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════
# Scoring
# ═══════════════════════════════════════════════════════════════════════

def calculate_score(errors: int, warnings: int, files_with_issues: int) -> int:
    """Calculate a 0-100 quality score."""
    if errors + warnings == 0:
        return 100
    penalty = (errors * 5) + (warnings * 1) + (files_with_issues * 2)
    return max(0, 100 - penalty)


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Frontend Code Review")
    parser.add_argument("--file", help="Single file to review")
    parser.add_argument("--src", help="Source directory to scan")
    parser.add_argument("--format", default="text", choices=["text", "json", "markdown"])
    parser.add_argument("--project-dir", help="Project root (for config detection)", default=None)
    args = parser.parse_args()

    if not args.file and not args.src:
        print("ERROR: Specify --file or --src", file=sys.stderr)
        sys.exit(1)

    target = Path(args.file or args.src).resolve()
    project_dir = Path(args.project_dir or target.parent if args.file else target).resolve()

    if not target.exists():
        print(f"ERROR: Target not found: {target}", file=sys.stderr)
        sys.exit(1)

    # Scan project config
    project_context = scan_project_config(project_dir)

    # Run ESLint
    eslint_data = run_eslint(target, project_dir)

    # Build report
    report: dict = {
        "project_context": project_context,
        "target": str(target),
        "mode": "file" if args.file else "src",
        "timestamp": datetime.now(CST).isoformat(),
        "issues": [],
        "affected_symbols": [],
        "summary": {"files_scanned": 0, "files_with_issues": 0, "errors": 0, "warnings": 0, "total_issues": 0, "score": 100},
        "eslint_raw": None,
    }

    # Handle ESLint errors
    if len(eslint_data) == 1 and "_error" in eslint_data[0]:
        print(f"ERROR: {eslint_data[0]['_error']}", file=sys.stderr)
        print("Continuing with limited analysis (no ESLint)...")
        report["summary"]["score"] = "N/A (ESLint unavailable)"
    else:
        for file_result in eslint_data:
            file_path = file_result.get("filePath", "unknown")
            messages = file_result.get("messages", [])
            error_count = file_result.get("errorCount", 0)
            warning_count = file_result.get("warningCount", 0)

            report["summary"]["files_scanned"] += 1
            if messages:
                report["summary"]["files_with_issues"] += 1
            report["summary"]["errors"] += error_count
            report["summary"]["warnings"] += warning_count
            report["summary"]["total_issues"] += error_count + warning_count

            for msg in messages:
                rule_id = msg.get("ruleId", "")
                message = msg.get("message", "")
                symbol = ""

                # Extract symbol name from message (e.g., "'handleSubmit' is defined but never used")
                sym_match = re.search(r"'(\w+)'", message)
                if sym_match:
                    symbol = sym_match.group(1)

                issue = {
                    "filePath": file_path,
                    "line": msg.get("line", "?"),
                    "column": msg.get("column", "?"),
                    "severity": msg.get("severity", 2),
                    "ruleId": rule_id,
                    "message": message,
                    "suggestion": get_suggestion(rule_id, message, symbol),
                    "symbol_ref": None,
                }

                # Symbol cross-reference
                if symbol:
                    def_loc = find_symbol_definition(project_dir, symbol)
                    if def_loc:
                        issue["symbol_ref"] = def_loc
                        report["affected_symbols"].append({
                            "name": symbol,
                            "kind": "function",
                            "file": def_loc["file"],
                            "line": def_loc["line"],
                        })

                report["issues"].append(issue)

    # Calculate score
    if isinstance(report["summary"]["score"], int):
        report["summary"]["score"] = calculate_score(
            report["summary"]["errors"],
            report["summary"]["warnings"],
            report["summary"]["files_with_issues"],
        )

    # Output
    formatters = {
        "text": _render_text,
        "json": _render_json,
        "markdown": _render_markdown,
    }
    output = formatters[args.format](report)
    print(output)

    # Exit with status based on errors
    if report["summary"]["errors"] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
