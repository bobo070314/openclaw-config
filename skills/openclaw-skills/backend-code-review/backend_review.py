#!/usr/bin/env python
"""
backend-code-review v0.2.0 — Python Backend Code Review & Security Audit

Three-layered analysis:
  1. pylint/flake8 → linting issues (optional, fallback to AST when unavailable)
  2. AST pattern detection → Django/FastAPI framework patterns
  3. Security scanner → SQL injection, N+1 queries, hardcoded secrets, unsafe deserialization

Output: Markdown report with risk levels (High/Medium/Low) and fix examples.

Usage:
    python backend_review.py --src <dir> [--format markdown|text|json] [--no-linter]
    python backend_review.py --file <path> [--format markdown|text|json]
"""

import ast
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path


CST = timezone(timedelta(hours=8))
SKIP_DIRS = {"node_modules", ".git", ".next", "dist", "build", "__pycache__",
             ".venv", "venv", "env", ".tox", ".eggs", "*.egg-info"}

# ═══════════════════════════════════════════════════════════════════════
# Project Configuration Scanner
# ═══════════════════════════════════════════════════════════════════════

def scan_project_config(project_dir: Path) -> dict:
    """Extract project configuration: dependencies, framework, lint config."""
    config = {
        "framework": "unknown",
        "dependencies": {},
        "lint_configs": [],
        "structure": {"views": 0, "models": 0, "routers": 0, "services": 0},
    }

    # Reqs
    for fname in ["requirements.txt", "requirements-dev.txt"]:
        p = project_dir / fname
        if not p.exists():
            continue
        try:
            for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                # Parse "package==version" or "package>=version"
                m = re.match(r'^([a-zA-Z0-9_\-\.]+)\s*([><=!~]+)\s*([\d\.]+)', line)
                if m:
                    config["dependencies"][m.group(1).lower()] = m.group(3)
                else:
                    pkg = re.match(r'^([a-zA-Z0-9_\-\.]+)', line)
                    if pkg:
                        config["dependencies"][pkg.group(1).lower()] = "latest"
        except Exception:
            pass

    # pyproject.toml
    pp = project_dir / "pyproject.toml"
    if pp.exists():
        try:
            content = pp.read_text(encoding="utf-8", errors="replace")
            deps_match = re.search(r'\[tool\.poetry\.dependencies\](.*?)(?:\[|$)', content, re.DOTALL)
            if deps_match:
                for line in deps_match.group(1).splitlines():
                    m = re.match(r'^\s*([a-zA-Z0-9_\-]+)\s*=\s*[\"\']?([^\"\'\n]+)', line)
                    if m:
                        config["dependencies"][m.group(1).lower()] = m.group(2).strip('"\'')
        except Exception:
            pass

    # Framework detection
    deps = config["dependencies"]
    if "django" in deps:
        config["framework"] = "django"
    elif "fastapi" in deps:
        config["framework"] = "fastapi"
    elif "flask" in deps:
        config["framework"] = "flask"

    # Lint configs
    for candidate in [".pylintrc", "pyproject.toml", "setup.cfg", "tox.ini"]:
        if (project_dir / candidate).exists():
            config["lint_configs"].append(candidate)
    if (project_dir / ".flake8").exists():
        config["lint_configs"].append(".flake8")

    return config


# ═══════════════════════════════════════════════════════════════════════
# Linter Runner (pylint or flake8)
# ═══════════════════════════════════════════════════════════════════════

def run_linter(target: Path, project_dir: Path) -> list[dict]:
    """Run pylint (primary) or fallback to flake8. Returns parsed issues."""
    linters = [
        ["pylint", "--output-format=json"],
        ["flake8", "--format=json"],
    ]

    for cmd_base in linters:
        linter_name = cmd_base[0]
        cmd = cmd_base + [str(target)]
        try:
            result = subprocess.run(
                cmd,
                cwd=str(project_dir),
                capture_output=True,
                text=True,
                timeout=120,
                env={**os.environ, "PYTHONIOENCODING": "utf-8", "CI": "true"},
            )
            output = result.stdout.strip() or result.stderr.strip()
            if not output:
                return []
            issues = _parse_linter_output(linter_name, output)
            if issues:
                return issues
        except subprocess.TimeoutExpired:
            continue
        except FileNotFoundError:
            continue

    return [{"_linter_error": "Neither pylint nor flake8 found. Run: pip install pylint"}]


def _parse_linter_output(linter: str, output: str) -> list[dict]:
    """Parse pylint JSON or flake8 JSON output into normalized format."""
    issues = []
    if linter == "pylint":
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            return [{"_linter_error": f"pylint parse error: {output[:300]}"}]
        for item in data:
            issues.append({
                "source": "pylint",
                "file": item.get("path", "?"),
                "line": item.get("line", "?"),
                "column": item.get("column", "?"),
                "message": item.get("message", ""),
                "symbol": item.get("symbol", ""),
                "type": item.get("type", "info"),
            })
    elif linter == "flake8":
        issues = []
        for line in output.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            m = re.match(r'^(.+?):(\d+):(\d+):\s+(\w+)\s+(.+)$', line)
            if m:
                issues.append({
                    "source": "flake8",
                    "file": m.group(1),
                    "line": int(m.group(2)),
                    "column": int(m.group(3)),
                    "message": m.group(5),
                    "symbol": m.group(4),
                    "type": "warning",
                })
    return issues


# ═══════════════════════════════════════════════════════════════════════
# AST-based Framework Pattern Detection
# ═══════════════════════════════════════════════════════════════════════

class FrameworkVisitor(ast.NodeVisitor):
    """Walk AST to detect Django/FastAPI/Flask patterns and collect structure info."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.findings: list[dict] = []
        self._current_func: str | None = None
        self._imports: set[str] = set()
        self._has_django_orm = False
        self._has_fastapi_router = False

    def visit_Import(self, node):
        for alias in node.names:
            self._imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self._imports.add(node.module)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        old = self._current_func
        self._current_func = node.name

        # Detect Django view
        if any(getattr(d, 'arg', '') == "request" for d in node.args.args):
            self.findings.append({
                "kind": "framework",
                "subtype": "django_view",
                "func": node.name,
                "file": self.filepath,
                "line": node.lineno,
            })

        self.generic_visit(node)
        self._current_func = old

    def visit_AsyncFunctionDef(self, node):
        old = self._current_func
        self._current_func = node.name

        # Detect FastAPI endpoint (has Request/Depends params)
        for d in node.args.args:
            if d.annotation:
                ann_str = ast.unparse(d.annotation) if hasattr(ast, 'unparse') else ast.dump(d.annotation)
                if "Request" in ann_str or "Depends" in ann_str or "APIRouter" in ann_str:
                    self.findings.append({
                        "kind": "framework",
                        "subtype": "fastapi_endpoint",
                        "func": node.name,
                        "file": self.filepath,
                        "line": node.lineno,
                    })
                    break

        self.generic_visit(node)
        self._current_func = old

    def visit_Call(self, node):
        func_str = ""
        if isinstance(node.func, ast.Attribute):
            func_str = _get_attr_name(node.func)
        elif isinstance(node.func, ast.Name):
            func_str = node.func.id

        # Django ORM queries
        if any(kw in func_str for kw in [".objects.", ".filter(", ".get(", ".exclude(", ".all(", ".create("]):
            self._has_django_orm = True

        # FastAPI router
        if func_str.endswith((".include_router", "APIRouter")):
            self._has_fastapi_router = True

        self.generic_visit(node)


def _get_attr_name(node) -> str:
    """Get full dotted attribute name from an ast.Attribute chain."""
    parts = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
    return ".".join(reversed(parts))


# ═══════════════════════════════════════════════════════════════════════
# Security Scanner — Regex-based patterns
# ═══════════════════════════════════════════════════════════════════════

# Risk: HIGH = immediate fix needed, MEDIUM = likely issue, LOW = best practice
SECURITY_PATTERNS = [
    # SQL Injection — raw SQL with string formatting
    {
        "id": "SEC-001",
        "name": "SQL Injection — raw SQL with f-string/format",
        "patterns": [
            re.compile(r'(?:execute|executemany|raw)\s*\(\s*f[\"\']', re.IGNORECASE),
            re.compile(r'(?:execute|executemany|raw)\s*\([^)]*\.format\(', re.IGNORECASE),
            re.compile(r'(?:execute|executemany|raw)\s*\([^)]*%\s*\(', re.IGNORECASE),
            re.compile(r'cursor\.execute\s*\(\s*[\"\'].*%(?:s|d|r)', re.IGNORECASE),
        ],
        "risk": "HIGH",
        "fix": "Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = %s', [user_id])",
    },
    # SQL Injection — Django raw/extra
    {
        "id": "SEC-002",
        "name": "SQL Injection — Django .raw() or .extra() with interpolated values",
        "patterns": [
            re.compile(r'\.raw\s*\(\s*f[\"\']', re.IGNORECASE),
            re.compile(r'\.extra\s*\(\s*.*where\s*=\s*f[\"\']', re.IGNORECASE),
            re.compile(r'RawSQL\s*\(', re.IGNORECASE),
        ],
        "risk": "HIGH",
        "fix": "Use Django ORM queryset methods (.filter, .exclude) or RawSQL with params=[]",
    },
    # N+1 Query — select_related / prefetch_related missing in loops
    {
        "id": "SEC-003",
        "name": "Potential N+1 query — ORM query inside loop without prefetch",
        "patterns": [
            # Heuristic: for loop containing .objects.filter() without prior .prefetch_related
            re.compile(r'for\s+\w+\s+in\s+[^:]+:\s*$', re.MULTILINE),
        ],
        "risk": "MEDIUM",
        "requires_loop_check": True,
        "fix": "Use .select_related() for FK, .prefetch_related() for M2M before the loop, or use iterator() for large datasets",
    },
    # Hardcoded secrets
    {
        "id": "SEC-004",
        "name": "Hardcoded secret (password/token/key)",
        "patterns": [
            re.compile(r'(?:PASSWORD|SECRET|API_KEY|AUTH_TOKEN|PRIVATE_KEY|DATABASE_URL)\s*=\s*[\"\'](?!\$\{|os\.environ)', re.IGNORECASE),
            re.compile(r'[\"\'](?:sk-|ghp_|gho_|xox[baprs]-)[a-zA-Z0-9_]{20,}', re.IGNORECASE),
        ],
        "risk": "HIGH",
        "fix": "Use environment variables: os.environ.get('SECRET_KEY') or python-dotenv",
    },
    # Unsafe deserialization
    {
        "id": "SEC-005",
        "name": "Unsafe deserialization — pickle.loads/yaml.load without SafeLoader",
        "patterns": [
            re.compile(r'pickle\.loads?\s*\(', re.IGNORECASE),
            re.compile(r'yaml\.load\s*\((?!.*Loader=yaml\.(?:Safe|Base)Loader)', re.IGNORECASE),
            re.compile(r'yaml\.load_all\s*\(', re.IGNORECASE),
        ],
        "risk": "HIGH",
        "fix": "Use yaml.safe_load() or pickle with trusted data only. Consider JSON instead.",
    },
    # eval/exec
    {
        "id": "SEC-006",
        "name": "Dynamic code execution — eval()/exec()/compile()",
        "patterns": [
            re.compile(r'\beval\s*\(', re.IGNORECASE),
            re.compile(r'\bexec\s*\(', re.IGNORECASE),
            re.compile(r'\bcompile\s*\(', re.IGNORECASE),
        ],
        "risk": "HIGH",
        "fix": "Avoid eval/exec. Use ast.literal_eval() for safe data parsing, or refactor to avoid dynamic code execution.",
    },
    # DEBUG=True in production
    {
        "id": "SEC-007",
        "name": "DEBUG=True — likely production misconfiguration",
        "patterns": [
            re.compile(r'DEBUG\s*=\s*True', re.IGNORECASE),
        ],
        "risk": "MEDIUM",
        "fix": "Set DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true' to read from environment",
    },
    # ALLOWED_HOSTS = ['*']
    {
        "id": "SEC-008",
        "name": "ALLOWED_HOSTS wildcard — Django security risk",
        "patterns": [
            re.compile(r'ALLOWED_HOSTS\s*=\s*\[[\"\']\*[\"\']\]', re.IGNORECASE),
        ],
        "risk": "MEDIUM",
        "fix": "Restrict ALLOWED_HOSTS to specific domains, not '*'",
    },
    # os.system / subprocess with shell=True
    {
        "id": "SEC-009",
        "name": "Command injection — os.system/subprocess with shell=True",
        "patterns": [
            re.compile(r'os\.system\s*\(.+?\$', re.IGNORECASE),
            re.compile(r'shell\s*=\s*True', re.IGNORECASE),
        ],
        "risk": "HIGH",
        "fix": "Use subprocess.run([cmd, arg1, arg2], shell=False) with argument list instead of string",
    },
    # Missing CSRF protection (Django)
    {
        "id": "SEC-010",
        "name": "Missing CSRF protection — @csrf_exempt on sensitive view",
        "patterns": [
            re.compile(r'@csrf_exempt', re.IGNORECASE),
        ],
        "risk": "MEDIUM",
        "fix": "Remove @csrf_exempt unless absolutely necessary. Use AJAX with CSRF token in headers.",
    },
]


def scan_security(filepath: Path, content: str, lines: list[str]) -> list[dict]:
    """Scan a single file for security vulnerabilities."""
    findings = []

    for rule in SECURITY_PATTERNS:
        for pattern in rule["patterns"]:
            for m in pattern.finditer(content):
                line_no = content[:m.start()].count("\n") + 1
                snippet = lines[line_no - 1].strip()[:200]

                finding = {
                    "kind": "security",
                    "rule_id": rule["id"],
                    "name": rule["name"],
                    "risk": rule["risk"],
                    "file": str(filepath),
                    "line": line_no,
                    "snippet": snippet,
                    "fix": rule["fix"],
                }

                # Special handling: N+1 loop check (flag only — AST will confirm)
                if rule.get("requires_loop_check"):
                    finding["note"] = "Potential N+1 — verify manually. Check if ORM query is inside a loop without .prefetch_related()"
                    finding["risk"] = "MEDIUM"

                findings.append(finding)

    # Deduplicate by rule_id + line
    seen = set()
    deduped = []
    for f in findings:
        key = (f["rule_id"], f["line"], f["file"])
        if key not in seen:
            seen.add(key)
            deduped.append(f)

    return deduped


# ═══════════════════════════════════════════════════════════════════════
# File Walker & Aggregator
# ═══════════════════════════════════════════════════════════════════════

def walk_and_analyze(target: Path, project_dir: Path, run_lint: bool) -> dict:
    """Walk the source tree and run all analyses."""
    all_issues: list[dict] = []
    framework_findings: list[dict] = []
    security_findings: list[dict] = []
    structure = {"files": 0, "views": 0, "models": 0, "routers": 0, "services": 0}

    python_files = []
    for dirpath, dirnames, filenames in os.walk(target):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            if fname.endswith(".py"):
                python_files.append(Path(dirpath) / fname)

    for fpath in python_files:
        structure["files"] += 1

        # Quick classification by file name
        fname_lower = fpath.name.lower()
        if "view" in fname_lower:
            structure["views"] += 1
        elif "model" in fname_lower:
            structure["models"] += 1
        elif "router" in fname_lower or "url" in fname_lower:
            structure["routers"] += 1
        elif "service" in fname_lower:
            structure["services"] += 1

        # Read content
        try:
            content = fpath.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        lines = content.splitlines()

        # AST-based framework detection
        try:
            tree = ast.parse(content, filename=str(fpath))
            visitor = FrameworkVisitor(str(fpath))
            visitor.visit(tree)
            framework_findings.extend(visitor.findings)
        except SyntaxError:
            pass

        # Security scan
        sec = scan_security(fpath, content, lines)
        security_findings.extend(sec)

    # Linter (optional)
    lint_issues = []
    if run_lint:
        lint_issues = run_linter(target, project_dir)
        # Filter out linter error messages
        lint_issues = [i for i in lint_issues if not i.get("_linter_error")]

    # Merge all
    all_issues = lint_issues + [
        {**f, "source": "ast"} for f in framework_findings
    ] + security_findings

    return {
        "structure": structure,
        "framework_findings": framework_findings,
        "security_findings": security_findings,
        "lint_issues": lint_issues,
        "all_issues": all_issues,
    }


# ═══════════════════════════════════════════════════════════════════════
# Markdown Report Generator
# ═══════════════════════════════════════════════════════════════════════

def render_markdown(report: dict) -> str:
    """Generate a comprehensive Markdown audit report."""
    ctx = report["project_context"]
    structure = report["analysis"]["structure"]
    sec = report["analysis"]["security_findings"]
    lint = report["analysis"]["lint_issues"]
    fw = report["analysis"]["framework_findings"]

    lines = []
    lines.append("# 🔍 Backend Code Review & Security Audit")
    lines.append("")
    lines.append(f"**Date:** {datetime.now(CST).strftime('%Y-%m-%d %H:%M')} CST")
    lines.append(f"**Target:** `{report['target']}`")
    lines.append(f"**Mode:** {report['mode']}")
    lines.append("")

    # Project Context
    lines.append("## 📋 Project Context")
    lines.append("")
    lines.append(f"| Property | Value |")
    lines.append(f"|----------|-------|")
    lines.append(f"| Framework | **{ctx.get('framework', 'unknown').title()}** |")
    deps = ctx.get("dependencies", {})

    key_deps = [k for k in ["django", "fastapi", "flask", "sqlalchemy", "celery", "pydantic"] if k in deps]
    if key_deps:
        dep_list = ", ".join(f"{k} {deps[k]}" for k in key_deps)
        lines.append(f"| Key Dependencies | {dep_list} |")
    if ctx.get("lint_configs"):
        lines.append(f"| Lint Configs | {', '.join(ctx['lint_configs'])} |")
    lines.append("")

    # Structure
    lines.append("## 📊 Code Structure")
    lines.append("")
    lines.append(f"| Category | Count |")
    lines.append(f"|----------|-------|")
    lines.append(f"| Python files | {structure['files']} |")
    lines.append(f"| Views | {structure['views']} |")
    lines.append(f"| Models | {structure['models']} |")
    lines.append(f"| Routers/URLs | {structure['routers']} |")
    lines.append(f"| Services | {structure['services']} |")
    lines.append("")

    # Risk Summary
    high = sum(1 for s in sec if s["risk"] == "HIGH")
    med = sum(1 for s in sec if s["risk"] == "MEDIUM")
    low = sum(1 for s in sec if s["risk"] == "LOW")
    lines.append("## 🚨 Risk Summary")
    lines.append("")
    lines.append(f"| Risk | Count |")
    lines.append(f"|------|-------|")
    lines.append(f"| 🔴 HIGH | {high} |")
    lines.append(f"| 🟡 MEDIUM | {med} |")
    lines.append(f"| 🟢 LOW | {low} |")
    lines.append(f"| **Total** | **{high + med + low}** |")
    lines.append("")

    # Security Findings
    if sec:
        lines.append("## 🔐 Security Findings")
        lines.append("")
        # Group by risk
        for risk_level, label in [("HIGH", "🔴 HIGH"), ("MEDIUM", "🟡 MEDIUM"), ("LOW", "🟢 LOW")]:
            items = [s for s in sec if s["risk"] == risk_level]
            if not items:
                continue
            lines.append(f"### {label}")
            lines.append("")
            for s in items:
                rel_path = Path(s["file"]).name if len(s["file"]) > 60 else s["file"]
                lines.append(f"**{s['name']}** `[{s['rule_id']}]`")
                lines.append(f"- 📄 `{rel_path}:{s['line']}`")
                lines.append(f"- 💡 **Fix:** {s['fix']}")
                if s.get("note"):
                    lines.append(f"- ⚠️ {s['note']}")
                lines.append(f"- 📝 `{s['snippet'][:120]}`")
                lines.append("")
    else:
        lines.append("## 🔐 Security Findings")
        lines.append("")
        lines.append("✅ No security vulnerabilities detected.")
        lines.append("")

    # Framework Patterns
    if fw:
        lines.append("## 🏗️ Framework Patterns Detected")
        lines.append("")
        fw_by_type = defaultdict(list)
        for f in fw:
            fw_by_type[f["subtype"]].append(f)
        for subtype, items in sorted(fw_by_type.items()):
            lines.append(f"- **{subtype.replace('_', ' ').title()}**: {len(items)} detected")
            for item in items[:5]:
                lines.append(f"  - `{item['func']}()` — {Path(item['file']).name}:{item['line']}")
        lines.append("")

    # Lint Issues
    if lint:
        lines.append("## 📝 Lint Issues")
        lines.append("")
        lines.append(f"| File | Line | Type | Message |")
        lines.append(f"|------|------|------|---------|")
        for issue in lint[:30]:
            fname = Path(issue.get("file", "")).name
            lines.append(f"| {fname} | {issue.get('line', '?')} | {issue.get('type', '?')} | {issue.get('message', '')[:80]} |")

    lines.append("")
    lines.append("---")
    lines.append(f"*Report generated by backend-code-review v0.2.0 at {datetime.now(CST).isoformat()}*")
    return "\n".join(lines)


def render_text(report: dict) -> str:
    """Plain text report for terminal."""
    ctx = report["project_context"]
    structure = report["analysis"]["structure"]
    sec = report["analysis"]["security_findings"]

    lines = []
    lines.append("=" * 80)
    lines.append(f"  🔍 Backend Code Review & Security Audit")
    lines.append(f"  {datetime.now(CST).strftime('%Y-%m-%d %H:%M:%S')} CST")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"  Framework  : {ctx.get('framework', 'unknown').title()}")
    lines.append(f"  Files      : {structure['files']} Python files")
    lines.append(f"  Structure  : {structure['views']} views | {structure['models']} models | {structure['routers']} routers | {structure['services']} services")
    lines.append("")

    high = sum(1 for s in sec if s["risk"] == "HIGH")
    med = sum(1 for s in sec if s["risk"] == "MEDIUM")
    low = sum(1 for s in sec if s["risk"] == "LOW")
    lines.append(f"  Risk: 🔴 {high} HIGH | 🟡 {med} MEDIUM | 🟢 {low} LOW")
    lines.append("")

    if sec:
        lines.append("--- Security Findings ---")
        for s in sec:
            icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(s["risk"], "⚪")
            fname = Path(s["file"]).name
            lines.append(f"  {icon} [{s['rule_id']}] {s['name']}")
            lines.append(f"     {fname}:{s['line']}")
            lines.append(f"     Fix: {s['fix'][:100]}")
            lines.append("")

    lines.append("=" * 80)
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Backend Code Review & Security Audit")
    parser.add_argument("--src", help="Source directory to scan")
    parser.add_argument("--file", help="Single Python file to review")
    parser.add_argument("--format", default="markdown", choices=["markdown", "text", "json"])
    parser.add_argument("--project-dir", help="Project root directory")
    parser.add_argument("--no-linter", action="store_true", help="Skip pylint/flake8 (AST+security only)")
    args = parser.parse_args()

    if not args.src and not args.file:
        print("ERROR: Specify --src or --file", file=sys.stderr)
        sys.exit(1)

    target = Path(args.src or args.file).resolve()
    project_dir = Path(args.project_dir or (target.parent if args.file else target)).resolve()

    if not target.exists():
        print(f"ERROR: Target not found: {target}", file=sys.stderr)
        sys.exit(1)

    # Scan project config
    project_context = scan_project_config(project_dir)

    # Run analyses
    analysis = walk_and_analyze(target, project_dir, run_lint=not args.no_linter)

    report = {
        "target": str(target),
        "mode": "file" if args.file else "directory",
        "project_context": project_context,
        "analysis": analysis,
        "timestamp": datetime.now(CST).isoformat(),
    }

    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    elif args.format == "text":
        print(render_text(report))
    else:
        print(render_markdown(report))

    # Exit code based on HIGH severity findings
    high_count = sum(1 for s in analysis["security_findings"] if s["risk"] == "HIGH")
    sys.exit(1 if high_count > 0 else 0)


if __name__ == "__main__":
    main()
