#!/usr/bin/env python
"""
security-audit v0.2.0 — 静态代码安全审计
=========================================
检测常见漏洞模式：SQL注入、XSS、硬编码密钥、命令注入、路径穿越。
输入：Python 源码文件或目录
输出：结构化 JSON 报告 + 人类可读摘要

用法:
    python run.py <target_file_or_dir> [--severity critical|high|all] [--format json|text]
"""

import sys

# === V0.2.0 CLI STANDARD (auto-injected, do not remove) ===
VERSION = "0.2.0"
SKILL_NAME = "security-audit"
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

import os
import ast
import re
import json
from pathlib import Path
from datetime import datetime, timezone


# ===== 漏洞检测规则 =====

RULES = [
    {
        "id": "SEC-001",
        "name": "SQL Injection via string formatting",
        "severity": "critical",
        "description": "f-string or .format() used in SQL query construction",
        "patterns": [
            r'f["\']\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER)\b',
            r'\bf\s*["\']\s*(SELECT|INSERT|UPDATE|DELETE|CREATE)\b',
        ],
        "ast_check": True,
    },
    {
        "id": "SEC-002",
        "name": "SQL Injection via string concatenation",
        "severity": "critical",
        "description": "String concatenation (+) used in SQL query",
        "patterns": [
            r'["\']\s*(SELECT|INSERT|UPDATE|DELETE)\b.*["\']\s*\+\s*',
            r'\+\s*["\'].*\b(SELECT|INSERT|UPDATE|DELETE)\b',
        ],
        "ast_check": True,
    },
    {
        "id": "SEC-003",
        "name": "SQL Injection via percent formatting",
        "severity": "critical",
        "description": "Percent (%) formatting used in SQL query",
        "patterns": [
            r'["\']\s*(SELECT|INSERT|UPDATE|DELETE)\b.*["\']\s*%\s*\(',
            r'["\']\s*(SELECT|INSERT|UPDATE|DELETE)\b.*["\']\s*%\s*\w+',
        ],
        "ast_check": True,
    },
    {
        "id": "SEC-004",
        "name": "Hardcoded credentials",
        "severity": "high",
        "description": "Hardcoded password, API key, or token in source",
        "patterns": [
            r'(?i)(password|secret|api_key|token|passwd)\s*=\s*["\'][^"\']{4,}["\']',
            r'(?i)(password|secret|api_key|token|passwd)\s*[:=]\s*["\'][^"\']{4,}["\']',
        ],
        "ast_check": False,
    },
    {
        "id": "SEC-005",
        "name": "Command injection via shell=True",
        "severity": "high",
        "description": "subprocess with shell=True and user-controlled input",
        "patterns": [
            r'subprocess\.\w+\([^)]*shell\s*=\s*True',
            r'os\.system\s*\(',
            r'os\.popen\s*\(',
        ],
        "ast_check": True,
    },
    {
        "id": "SEC-006",
        "name": "Path traversal",
        "severity": "high",
        "description": "Unsanitized file path construction from user input",
        "patterns": [
            r'open\s*\(\s*[^)]*\+\s*[^)]*\)',
            r'os\.path\.join\s*\(\s*[^,]*request\.',
        ],
        "ast_check": True,
    },
    {
        "id": "SEC-007",
        "name": "XSS via unsanitized output",
        "severity": "medium",
        "description": "User input rendered without HTML escaping",
        "patterns": [
            r'(?i)innerHTML\s*=',
            r'(?i)dangerouslySetInnerHTML',
            r'(?i)document\.write\s*\(',
        ],
        "ast_check": False,
    },
    {
        "id": "SEC-008",
        "name": "Weak cryptography",
        "severity": "medium",
        "description": "MD5 or SHA1 used for security purposes",
        "patterns": [
            r'\bhashlib\.md5\b',
            r'\bhashlib\.sha1\b',
            r'\bmake_key\s*\(\s*hashlib\.md5\b',
        ],
        "ast_check": False,
    },
    {
        "id": "SEC-009",
        "name": "Debug mode enabled",
        "severity": "low",
        "description": "DEBUG=True or equivalent in non-dev code",
        "patterns": [
            r'(?i)DEBUG\s*=\s*True',
            r'(?i)debug\s*=\s*True',
        ],
        "ast_check": False,
    },
]


class ASTVulnVisitor(ast.NodeVisitor):
    """AST visitor that checks for SQL injection patterns in string building."""

    def __init__(self, source_lines, findings):
        self.source_lines = source_lines
        self.findings = findings

    def visit_Call(self, node):
        # Check for .execute() calls with non-parameterized queries
        if isinstance(node.func, ast.Attribute) and node.func.attr == "execute":
            if node.args:
                first_arg = node.args[0]
                # Check if first arg is f-string
                if isinstance(first_arg, ast.JoinedStr):
                    lineno = node.lineno
                    self.findings.append({
                        "rule_id": "SEC-001",
                        "name": "SQL Injection via f-string",
                        "severity": "critical",
                        "line": lineno,
                        "line_content": self.source_lines[lineno - 1].strip() if lineno <= len(self.source_lines) else "",
                        "message": f"Line {lineno}: f-string used in SQL query → injection risk",
                    })
                    self.generic_visit(node)
                    return
                # Check if first arg is BinOp string concatenation
                if isinstance(first_arg, ast.BinOp) and isinstance(first_arg.op, ast.Add):
                    lineno = node.lineno
                    self.findings.append({
                        "rule_id": "SEC-002",
                        "name": "SQL Injection via concatenation",
                        "severity": "critical",
                        "line": lineno,
                        "line_content": self.source_lines[lineno - 1].strip() if lineno <= len(self.source_lines) else "",
                        "message": f"Line {lineno}: String concatenation in SQL query → injection risk. Use parameterized query '?' placeholders",
                    })
                    self.generic_visit(node)
                    return
                # Check if first arg is BinOp percent format
                if isinstance(first_arg, ast.BinOp) and isinstance(first_arg.op, ast.Mod):
                    lineno = node.lineno
                    self.findings.append({
                        "rule_id": "SEC-003",
                        "name": "SQL Injection via % formatting",
                        "severity": "critical",
                        "line": lineno,
                        "line_content": self.source_lines[lineno - 1].strip() if lineno <= len(self.source_lines) else "",
                        "message": f"Line {lineno}: Percent formatting in SQL query → injection risk. Use parameterized query '?' placeholders",
                    })
        self.generic_visit(node)


def scan_file(filepath: Path) -> dict:
    """Scan a single Python file for vulnerabilities."""
    findings = []
    errors = []
    lines = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        lines = source.split("\n")
    except Exception as e:
        return {"file": str(filepath), "findings": [], "errors": [f"Cannot read: {e}"]}

    # ---- Regex-based pattern matching ----
    for rule in RULES:
        for pattern in rule["patterns"]:
            for match in re.finditer(pattern, source):
                lineno = source[:match.start()].count("\n") + 1
                line_content = lines[lineno - 1].strip()
                # Skip if already found at this line by this rule
                if any(f["rule_id"] == rule["id"] and f["line"] == lineno for f in findings):
                    continue
                findings.append({
                    "rule_id": rule["id"],
                    "name": rule["name"],
                    "severity": rule["severity"],
                    "line": lineno,
                    "line_content": line_content[:200],
                    "message": f"Line {lineno}: {rule['description']} — {line_content[:100]}",
                })

    # ---- AST-based deep analysis ----
    try:
        tree = ast.parse(source)
        visitor = ASTVulnVisitor(lines, findings)
        visitor.visit(tree)
    except SyntaxError as e:
        errors.append(f"AST parse failed: {e}")

    # ---- Deduplicate findings ----
    seen = set()
    unique_findings = []
    for f in findings:
        key = (f["rule_id"], f["line"])
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    return {
        "file": str(filepath),
        "lines_total": len(lines),
        "findings": unique_findings,
        "finding_count": len(unique_findings),
        "errors": errors,
    }


def scan_directory(dirpath: Path) -> dict:
    """Recursively scan a directory for Python files."""
    all_results = []
    total_findings = 0

    for pyfile in dirpath.rglob("*.py"):
        # Skip __pycache__, .git, node_modules, etc.
        parts = set(pyfile.parts)
        if parts & {"__pycache__", ".git", "node_modules", ".venv", "venv", "env", "dist", "build"}:
            continue
        result = scan_file(pyfile)
        all_results.append(result)
        total_findings += result["finding_count"]

    return {
        "target": str(dirpath),
        "files_scanned": len(all_results),
        "total_findings": total_findings,
        "results": all_results,
    }


def format_text_report(data: dict) -> str:
    """Human-readable text report."""
    lines = []
    lines.append("=" * 60)
    lines.append("  SECURITY AUDIT REPORT")
    lines.append("=" * 60)

    if "file" in data:
        lines.append(f"\nTarget: {data['file']}")
        lines.append(f"Total lines: {data['lines_total']}")
        lines.append(f"Vulnerabilities found: {data['finding_count']}")
        lines.append("-" * 40)

        if data["findings"]:
            for f in data["findings"]:
                severity_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵"}.get(f["severity"], "⚪")
                lines.append(f"  {severity_icon} [{f['severity'].upper()}] {f['name']}")
                lines.append(f"     Line {f['line']}: {f['line_content'][:120]}")
                lines.append(f"     Fix: {f['message']}")
                lines.append("")
        else:
            lines.append("  ✅ No vulnerabilities detected.")

    elif "results" in data:
        lines.append(f"\nTarget directory: {data['target']}")
        lines.append(f"Files scanned: {data['files_scanned']}")
        lines.append(f"Total vulnerabilities: {data['total_findings']}")
        lines.append("-" * 40)
        for r in data["results"]:
            if r["finding_count"] > 0:
                lines.append(f"\n  {r['file']} ({r['finding_count']} issues):")
                for f in r["findings"]:
                    severity_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵"}.get(f["severity"], "⚪")
                    lines.append(f"    {severity_icon} L{f['line']:04d}: [{f['severity']}] {f['name']}")

    lines.append("\n" + "=" * 60)
    lines.append(f"  Audit completed at {datetime.now(timezone.utc).isoformat()}")
    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    target = None
    fmt = "text"
    severity_filter = "all"
    verbose = False

    # ---- Parse args ----
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] in ("--target", "-t") and i + 1 < len(args):
            target = args[i + 1]
            i += 2
        elif args[i] in ("--format", "-f") and i + 1 < len(args):
            fmt = args[i + 1]
            i += 2
        elif args[i] in ("--severity", "-s") and i + 1 < len(args):
            severity_filter = args[i + 1]
            i += 2
        elif args[i] in ("--verbose", "-v"):
            verbose = True
            i += 1
        elif not args[i].startswith("-") and target is None:
            target = args[i]
            i += 1
        else:
            i += 1

    if not target:
        print("Usage: python run.py <target_file_or_dir> [--format json|text] [--severity critical|high|low|all]")
        sys.exit(1)

    target_path = Path(target).resolve()

    if not target_path.exists():
        print(f"Error: Target '{target}' does not exist")
        sys.exit(1)

    # ---- Scan ----
    if target_path.is_file():
        result = scan_file(target_path)
    else:
        result = scan_directory(target_path)

    # ---- Filter by severity ----
    if severity_filter != "all" and "results" in result:
        allowed = {"critical": ["critical"], "high": ["critical", "high"], "medium": ["critical", "high", "medium"], "low": ["critical", "high", "medium", "low"]}
        for r in result["results"]:
            r["findings"] = [f for f in r.get("findings", []) if f["severity"] in allowed.get(severity_filter, [f["severity"]])]
            r["finding_count"] = len(r["findings"])
        result["total_findings"] = sum(r["finding_count"] for r in result["results"])

    # ---- Output ----
    if fmt == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    else:
        print(format_text_report(result))

    # ---- Exit code ----
    vuln_count = result.get("finding_count", 0) if "finding_count" in result else result.get("total_findings", 0)
    if vuln_count > 0:
        print(f"\n[{vuln_count} vulnerabilities found]")
    else:
        print("\n[No vulnerabilities found]")

    sys.exit(0 if vuln_count == 0 else 1)


if __name__ == "__main__":
    main()
