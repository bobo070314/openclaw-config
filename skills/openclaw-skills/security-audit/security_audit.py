#!/usr/bin/env python
"""
security-audit v0.2.0 — Infrastructure Security Audit

Scans non-code artifacts: Dockerfile, docker-compose, CI/CD workflows,
.env files, Terraform, shell scripts, JSON configs, certificate files.

12 rules across 4 risk tiers: CRITICAL > HIGH > MEDIUM > LOW

Usage:
    python security_audit.py <project-dir> [--format markdown|text|json] [--no-git]
"""

import fnmatch
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path


CST = timezone(timedelta(hours=8))
SKIP_DIRS = {"node_modules", ".git", ".next", "dist", "build", "__pycache__",
             ".venv", "venv", "env", ".tox", ".eggs", "target", "coverage"}

# ═══════════════════════════════════════════════════════════════════════
# File Discovery — classify non-code artifacts
# ═══════════════════════════════════════════════════════════════════════

TARGET_PATTERNS = [
    "Dockerfile*", "docker-compose*.yml", "docker-compose*.yaml",
    ".env*", "*.env",
    ".github/workflows/**/*.yml", ".github/workflows/**/*.yaml",
    ".gitlab-ci.yml", ".circleci/config.yml", "Jenkinsfile",
    "*.tf", "*.tfvars", "terraform.tfvars",
    "*.pem", "*.key", "*.crt", "*.cert",
    "secrets.yaml", "secrets.yml", "credentials.json",
    "*.sh", "*.ps1", "Makefile",
]

DOCKERFILE_PATTERN = re.compile(r'^(?:Dockerfile.*)$', re.IGNORECASE)
COMPOSE_PATTERN = re.compile(r'^docker-compose.*\.(?:yml|yaml)$', re.IGNORECASE)
ENV_PATTERN = re.compile(r'\.env(\..*)?$', re.IGNORECASE)
CI_PATTERN = re.compile(r'\.github/workflows/.*\.(?:yml|yaml)$|\.gitlab-ci\.yml|\.circleci/|Jenkinsfile', re.IGNORECASE)
TERRAFORM_PATTERN = re.compile(r'.*\.tf(vars)?$', re.IGNORECASE)
PEM_PATTERN = re.compile(r'.*\.(?:pem|key|crt|cert)$', re.IGNORECASE)
JSON_PATTERN = re.compile(r'.*\.json$', re.IGNORECASE)
YAML_PATTERN = re.compile(r'(?<!docker-compose)\.(?:yml|yaml)$', re.IGNORECASE)
SHELL_PATTERN = re.compile(r'.*\.(?:sh|ps1)$', re.IGNORECASE)


def discover_files(root: Path) -> dict[str, list[Path]]:
    """Walk project tree, classify files by type."""
    classified: dict[str, list[Path]] = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fname in filenames:
            fpath = Path(dirpath) / fname
            rel_path = str(rel_dir / fname)

            if DOCKERFILE_PATTERN.match(fname):
                classified["dockerfile"].append(fpath)
            elif COMPOSE_PATTERN.match(fname):
                classified["compose"].append(fpath)
            elif ENV_PATTERN.match(fname):
                classified["env"].append(fpath)
            elif CI_PATTERN.search(rel_path):
                classified["ci"].append(fpath)
            elif TERRAFORM_PATTERN.match(fname):
                classified["terraform"].append(fpath)
            elif PEM_PATTERN.match(fname.lower()):
                classified["certificates"].append(fpath)
            elif SHELL_PATTERN.match(fname.lower()):
                classified["shell"].append(fpath)
            elif JSON_PATTERN.match(fname) and any(kw in fname.lower() for kw in ["secret", "credential", "config", "setting"]):
                classified["json_config"].append(fpath)
            elif YAML_PATTERN.match(fname) and any(kw in fname.lower() for kw in ["secret", "deploy", "k8s", "helm"]):
                classified["yaml_config"].append(fpath)
    return classified


# ═══════════════════════════════════════════════════════════════════════
# Secret Pattern Detection
# ═══════════════════════════════════════════════════════════════════════

SECRET_PATTERNS = [
    # GitHub tokens
    ("ghp_", re.compile(r'(?:^|[=\s:''"])(gh[pousr]_[a-zA-Z0-9]{36,})(?:$|[^a-zA-Z0-9])'), "GitHub Personal Access Token"),
    ("gho_", re.compile(r'(?:^|[=\s:''"])(gho_[a-zA-Z0-9]{36,})(?:$|[^a-zA-Z0-9])'), "GitHub OAuth Token"),
    ("ghu_", re.compile(r'(?:^|[=\s:''"])(ghu_[a-zA-Z0-9]{36,})(?:$|[^a-zA-Z0-9])'), "GitHub User Token"),
    ("ghs_", re.compile(r'(?:^|[=\s:''"])(ghs_[a-zA-Z0-9]{36,})(?:$|[^a-zA-Z0-9])'), "GitHub Server Token"),
    ("ghr_", re.compile(r'(?:^|[=\s:''"])(ghr_[a-zA-Z0-9]{36,})(?:$|[^a-zA-Z0-9])'), "GitHub Refresh Token"),
    # AWS keys
    ("AKIA", re.compile(r'(?:^|[=\s:''"])(AKIA[0-9A-Z]{16})(?:$|[^A-Z0-9])'), "AWS Access Key ID"),
    ("ASIA", re.compile(r'(?:^|[=\s:''"])(ASIA[0-9A-Z]{16})(?:$|[^A-Z0-9])'), "AWS Temporary Access Key"),
    # Generic token patterns
    ("sk-", re.compile(r'(?:^|[=\s:''"])(sk-[a-zA-Z0-9]{20,})(?:$|[^a-zA-Z0-9])'), "API Key (sk- prefix)"),
    ("BEGIN PRIVATE KEY", re.compile(r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----'), "Private Key Content"),
    # Generic secrets assignment
    ("PASSWORD=", re.compile(r'(?:PASSWORD|SECRET|API_KEY|AUTH_TOKEN|PRIVATE_KEY)\s*=\s*[''"]\s*[^\s''"]{8,}\s*[''"]', re.IGNORECASE), "Hardcoded Secret in assignment"),
    # JWT tokens
    ("JWT", re.compile(r'(?:^|[=\s:''"])(eyJ[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]{20,})(?:$|[^a-zA-Z0-9_-])'), "JWT Token"),
]


# ═══════════════════════════════════════════════════════════════════════
# Scanners per file type
# ═══════════════════════════════════════════════════════════════════════

def scan_dockerfile(fpath: Path) -> list[dict]:
    """CRIT-LEVEL scan of Dockerfile instructions."""
    findings = []
    try:
        lines = fpath.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return findings

    has_user = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # FROM ...:latest
        m = re.match(r'^FROM\s+(\S+):(latest)\b', stripped, re.IGNORECASE)
        if m:
            findings.append({
                "rule_id": "HIGH-001",
                "rule": "Docker: FROM with :latest tag",
                "risk": "HIGH",
                "file": str(fpath),
                "line": i,
                "snippet": stripped[:120],
                "fix": f"Pin a specific version: FROM {m.group(1)}:1.2.3-alpine",
            })

        # RUN commands as root without --chown
        if re.search(r'^\s*RUN\s+(?:apt|apk|yum|pip|npm)\s+(?:install|add)', stripped, re.IGNORECASE):
            if "USER" not in " ".join(lines[:i]):
                findings.append({
                    "rule_id": "HIGH-002-NOTE",
                    "rule": "Docker: RUN install without preceding USER switch",
                    "risk": "MEDIUM",
                    "file": str(fpath),
                    "line": i,
                    "snippet": stripped[:120],
                    "fix": "Add 'USER 1000' before RUN commands, or use --chown flag on COPY",
                })

        if re.match(r'^USER\s+\S+', stripped):
            has_user = True

    # Missing USER entirely
    if not has_user:
        findings.append({
            "rule_id": "HIGH-002",
            "rule": "Docker: No USER directive — container runs as root",
            "risk": "HIGH",
            "file": str(fpath),
            "line": 1,
            "snippet": "(entire Dockerfile)",
            "fix": "Add 'USER 1000:1000' to run as non-root user",
        })

    # EXPOSE check
    for i, line in enumerate(lines, 1):
        m = re.match(r'^EXPOSE\s+(\d+)', line)
        if m:
            port = int(m.group(1))
            if port in {22, 3306, 5432, 6379, 27017, 9200}:
                findings.append({
                    "rule_id": "MED-001",
                    "rule": f"Docker: EXPOSE {port} — sensitive port",
                    "risk": "MEDIUM",
                    "file": str(fpath),
                    "line": i,
                    "snippet": line.strip(),
                    "fix": f"Remove EXPOSE {port} unless intentionally exposed behind firewall",
                })

    return findings


def scan_env_file(fpath: Path, root: Path) -> list[dict]:
    """Scan .env files for real secrets vs placeholders."""
    findings = []
    try:
        lines = fpath.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return findings

    has_real_secrets = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue

        # Check SECRET_PATTERNS
        for token_id, pattern, desc in SECRET_PATTERNS:
            if pattern.search(stripped):
                has_real_secrets = True
                findings.append({
                    "rule_id": "CRIT-004",
                    "rule": f".env: {desc} exposed",
                    "risk": "CRITICAL",
                    "file": str(fpath),
                    "line": i,
                    "snippet": _mask_secret(stripped),
                    "fix": "Remove real secrets from .env. Use .env.example with placeholders.",
                })

        # Check for non-placeholder values (long random strings)
        m = re.match(r'^(\w+)\s*=\s*[\'"]?([^\s\'"]{20,})[\'"]?$', stripped)
        if m:
            value = m.group(2)
            if not any(placeholder in value.lower() for placeholder in ["example", "change", "your", "xxx", "todo", "placeholder", "test"]):
                if not re.match(r'^(localhost|127\.0\.0\.1|0\.0\.0\.0|true|false|\d+)$', value, re.IGNORECASE):
                    has_real_secrets = True
                    findings.append({
                        "rule_id": "CRIT-004",
                        "rule": f".env: {m.group(1)} contains a real value (not placeholder)",
                        "risk": "CRITICAL",
                        "file": str(fpath),
                        "line": i,
                        "snippet": _mask_secret(stripped),
                        "fix": f"Replace with placeholder: {m.group(1)}=your_{m.group(1).lower()}_here",
                    })

    # Check if .env is gitignored
    if (root / ".git").exists():
        gitignore = root / ".gitignore"
        if gitignore.exists():
            ignored = gitignore.read_text(encoding="utf-8", errors="replace")
            if ".env" not in ignored:
                findings.append({
                    "rule_id": "MED-004",
                    "rule": ".env file not in .gitignore — risk of committing secrets",
                    "risk": "MEDIUM",
                    "file": str(fpath),
                    "line": 0,
                    "snippet": "(add .env to .gitignore)",
                    "fix": "Add '.env*' and '!.env.example' to .gitignore",
                })

    return findings


def scan_ci_workflows(fpath: Path) -> list[dict]:
    """Scan CI/CD workflow files for secret exposure risks."""
    findings = []
    try:
        content = fpath.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
    except Exception:
        return findings

    # Secret pattern in workflow steps
    for i, line in enumerate(lines, 1):
        for token_id, pattern, desc in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append({
                    "rule_id": "CRIT-001",
                    "rule": f"CI: {desc} exposed in workflow",
                    "risk": "CRITICAL",
                    "file": str(fpath),
                    "line": i,
                    "snippet": _mask_secret(line.strip()[:120]),
                    "fix": "Use GitHub Secrets: ${{ secrets.MY_SECRET }} instead of hardcoded value",
                })

        # secrets interpolation in shell commands (injection risk)
        if "${{ secrets." in line or "${{ github.token" in line:
            if "echo" in line or ">" in line or "|" in line:
                findings.append({
                    "rule_id": "HIGH-004",
                    "rule": "CI: Secret piped/redirected in shell command — potential leak",
                    "risk": "HIGH",
                    "file": str(fpath),
                    "line": i,
                    "snippet": line.strip()[:120],
                    "fix": "Set secret as env var first: env: MY_VAR: ${{ secrets.TOKEN }}, then use $MY_VAR",
                })

    return findings


def scan_compose(fpath: Path) -> list[dict]:
    """Scan docker-compose files for security misconfigurations."""
    findings = []
    try:
        content = fpath.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
    except Exception:
        return findings

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # privileged: true
        if re.search(r'privileged\s*:\s*true', stripped, re.IGNORECASE):
            findings.append({
                "rule_id": "HIGH-003",
                "rule": "Compose: privileged: true — container has full host access",
                "risk": "HIGH",
                "file": str(fpath),
                "line": i,
                "snippet": stripped,
                "fix": "Remove 'privileged: true', add only needed capabilities: cap_add: [NET_ADMIN]",
            })

        # cap_add: SYS_ADMIN
        if "SYS_ADMIN" in stripped:
            findings.append({
                "rule_id": "HIGH-003",
                "rule": "Compose: cap_add: SYS_ADMIN — excessive privileges",
                "risk": "HIGH",
                "file": str(fpath),
                "line": i,
                "snippet": stripped,
                "fix": "Remove SYS_ADMIN. Use specific capabilities only.",
            })

        # Ports bound to 0.0.0.0
        m = re.search(r'["\']?(\d{1,5}):(\d{1,5})["\']?', stripped)
        if m:
            port = int(m.group(2))
            if port in {22, 3306, 5432, 6379, 27017, 9200}:
                findings.append({
                    "rule_id": "MED-001",
                    "rule": f"Compose: Port {port} mapped — sensitive service exposed",
                    "risk": "MEDIUM",
                    "file": str(fpath),
                    "line": i,
                    "snippet": stripped,
                    "fix": f"Remove port mapping for {port}, or bind to 127.0.0.1:{port}:{port}",
                })

    return findings


def scan_certificates(fpath: Path) -> list[dict]:
    """Detect committed private keys and certificates."""
    findings = []
    try:
        content = fpath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    # CRITICAL: private key content in file
    if "-----BEGIN" in content and "PRIVATE KEY-----" in content:
        findings.append({
            "rule_id": "CRIT-003",
            "rule": f"Private key committed: {fpath.name}",
            "risk": "CRITICAL",
            "file": str(fpath),
            "line": 1,
            "snippet": f"File contains private key ({fpath.suffix})",
            "fix": "Remove the key file, add to .gitignore, rotate the key immediately",
        })

    # MEDIUM: .key/.pem file itself (even without content)
    if fpath.suffix.lower() in {".key", ".pem", ".p12", ".pfx"}:
        findings.append({
            "rule_id": "CRIT-003",
            "rule": f"Key file committed: {fpath.name}",
            "risk": "CRITICAL",
            "file": str(fpath),
            "line": 0,
            "snippet": f"Key file present in repository",
            "fix": "Remove from repo, add *.key *.pem to .gitignore, rotate keys",
        })

    return findings


def scan_shell(fpath: Path) -> list[dict]:
    """Scan shell scripts for hardcoded secrets."""
    findings = []
    try:
        content = fpath.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
    except Exception:
        return findings

    for i, line in enumerate(lines, 1):
        for token_id, pattern, desc in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append({
                    "rule_id": "CRIT-001",
                    "rule": f"Shell: {desc} in script",
                    "risk": "CRITICAL",
                    "file": str(fpath),
                    "line": i,
                    "snippet": _mask_secret(line.strip()[:120]),
                    "fix": "Use environment variables or a secrets manager instead",
                })

        # export KEY=value
        m = re.match(r'^(?:export\s+)?(\w*(?:SECRET|PASSWORD|TOKEN|KEY)\w*)\s*=\s*[\'"]?([^\s\'"]{8,})', line, re.IGNORECASE)
        if m:
            value = m.group(2)
            if value not in {"$1", "${1}", "$VAR", "${VAR}", "YOUR_KEY_HERE", ""}:
                findings.append({
                    "rule_id": "CRIT-004",
                    "rule": f"Shell: hardcoded {m.group(1)}",
                    "risk": "CRITICAL",
                    "file": str(fpath),
                    "line": i,
                    "snippet": f"{m.group(1)}=***",
                    "fix": "Use export {}=\"$(op read ...)\" or source from an external secrets manager",
                })

    return findings


def scan_terraform(fpath: Path) -> list[dict]:
    """Scan Terraform files for hardcoded credentials."""
    findings = []
    try:
        content = fpath.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
    except Exception:
        return findings

    for i, line in enumerate(lines, 1):
        for token_id, pattern, desc in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append({
                    "rule_id": "CRIT-002",
                    "rule": f"Terraform: {desc} hardcoded",
                    "risk": "CRITICAL",
                    "file": str(fpath),
                    "line": i,
                    "snippet": _mask_secret(line.strip()[:120]),
                    "fix": "Use Terraform variables with sensitive=true or a secrets backend",
                })

        # password / secret = "..."
        m = re.match(r'\s*(password|secret|access_key|private_key)\s*=\s*[\'"](\S{8,})[\'"]', line, re.IGNORECASE)
        if m:
            findings.append({
                "rule_id": "CRIT-004",
                "rule": f"Terraform: {m.group(1)} hardcoded",
                "risk": "CRITICAL",
                "file": str(fpath),
                "line": i,
                "snippet": f'{m.group(1)} = "***"',
                "fix": "var.my_secret with sensitive=true",
            })

    return findings


def _mask_secret(snippet: str) -> str:
    """Truncate and mask potential secret values."""
    if len(snippet) > 80:
        return snippet[:77] + "..."
    return snippet


# ═══════════════════════════════════════════════════════════════════════
# Report Generators
# ═══════════════════════════════════════════════════════════════════════

RISK_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
RISK_ICON = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}


def render_markdown(report: dict) -> str:
    """Generate a Markdown security audit report."""
    ctx = report["project_context"]
    findings = report["findings"]
    by_risk = defaultdict(list)
    for f in findings:
        by_risk[f["risk"]].append(f)

    lines = []
    lines.append("# 🛡️ Infrastructure Security Audit Report")
    lines.append("")
    lines.append(f"**Date:** {datetime.now(CST).strftime('%Y-%m-%d %H:%M')} CST")
    lines.append(f"**Project:** `{ctx['project_root']}`")
    lines.append(f"**Files scanned:** {ctx['files_scanned']}")
    lines.append("")

    # Summary
    lines.append("## 📊 Risk Summary")
    lines.append("")
    lines.append("| Risk Level | Count |")
    lines.append("|------------|-------|")
    for level in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        count = len(by_risk.get(level, []))
        icon = RISK_ICON.get(level, "⚪")
        lines.append(f"| {icon} {level} | {count} |")
    lines.append(f"| **Total** | **{len(findings)}** |")
    lines.append("")

    # Findings by risk
    for risk_level in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        items = by_risk.get(risk_level, [])
        if not items:
            continue
        icon = RISK_ICON.get(risk_level, "⚪")
        lines.append(f"## {icon} {risk_level} Severity — {len(items)} finding(s)")
        lines.append("")

        for item in sorted(items, key=lambda x: (x["rule_id"], x["file"])):
            fname = Path(item["file"]).name if len(item["file"]) > 60 else item["file"]
            lines.append(f"### {item['rule_id']}: {item['rule']}")
            lines.append("")
            lines.append(f"| Property | Value |")
            lines.append(f"|----------|-------|")
            lines.append(f"| **File** | `{fname}` |")
            lines.append(f"| **Line** | {item.get('line', 'N/A')} |")
            lines.append(f"| **Snippet** | `{item.get('snippet', '')[:100]}` |")
            lines.append(f"| **Fix** | {item['fix']} |")
            lines.append("")

    if not findings:
        lines.append("## ✅ No security issues found")
        lines.append("")

    lines.append("---")
    lines.append(f"*Report generated by security-audit v0.2.0 at {datetime.now(CST).isoformat()}*")
    return "\n".join(lines)


def render_text(report: dict) -> str:
    """Plain text report for terminal."""
    ctx = report["project_context"]
    findings = report["findings"]
    by_risk = defaultdict(list)
    for f in findings:
        by_risk[f["risk"]].append(f)

    lines = []
    lines.append("=" * 80)
    lines.append("  🛡️ Infrastructure Security Audit")
    lines.append(f"  {datetime.now(CST).strftime('%Y-%m-%d %H:%M:%S')} CST")
    lines.append("=" * 80)
    lines.append(f"  Project      : {ctx['project_root']}")
    lines.append(f"  Files scanned: {ctx['files_scanned']}")
    lines.append("")

    for level in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        count = len(by_risk.get(level, []))
        icon = RISK_ICON.get(level, "⚪")
        lines.append(f"  {icon} {level}: {count} findings")

    lines.append(f"  ─────────────────")
    lines.append(f"  Total: {len(findings)} findings")
    lines.append("")

    for risk_level in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        items = by_risk.get(risk_level, [])
        if not items:
            continue
        icon = RISK_ICON.get(risk_level, "⚪")
        lines.append(f"--- {icon} {risk_level} ({len(items)}) ---")
        for item in sorted(items, key=lambda x: (x["rule_id"], x["file"])):
            fname = Path(item["file"]).name
            lines.append(f"  [{item['rule_id']}] {item['rule']}")
            lines.append(f"      {fname}:{item.get('line', '?')}")
            lines.append(f"      Fix: {item['fix'][:120]}")
            lines.append("")

    lines.append("=" * 80)
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Infrastructure Security Audit")
    parser.add_argument("project_dir", help="Project root directory")
    parser.add_argument("--format", default="markdown", choices=["markdown", "text", "json"])
    parser.add_argument("--no-git", action="store_true", help="Skip .gitignore checks")
    args = parser.parse_args()

    root = Path(args.project_dir).resolve()
    if not root.is_dir():
        print(f"ERROR: Directory not found: {root}", file=sys.stderr)
        sys.exit(1)

    # Discover and classify
    classified = discover_files(root)
    all_findings: list[dict] = []

    # Scan by type
    for fpath in classified.get("dockerfile", []):
        all_findings.extend(scan_dockerfile(fpath))

    for fpath in classified.get("env", []):
        all_findings.extend(scan_env_file(fpath, root))

    for fpath in classified.get("ci", []):
        all_findings.extend(scan_ci_workflows(fpath))

    for fpath in classified.get("compose", []):
        all_findings.extend(scan_compose(fpath))

    for fpath in classified.get("certificates", []):
        all_findings.extend(scan_certificates(fpath))

    for fpath in classified.get("shell", []):
        all_findings.extend(scan_shell(fpath))

    for fpath in classified.get("terraform", []):
        all_findings.extend(scan_terraform(fpath))

    # Generic file scanning for remaining
    for kind in ["json_config", "yaml_config"]:
        for fpath in classified.get(kind, []):
            try:
                content = fpath.read_text(encoding="utf-8", errors="replace")
                lines = content.splitlines()
                for i, line in enumerate(lines, 1):
                    for token_id, pattern, desc in SECRET_PATTERNS:
                        if pattern.search(line):
                            all_findings.append({
                                "rule_id": "CRIT-001",
                                "rule": f"{kind}: {desc} exposed",
                                "risk": "CRITICAL",
                                "file": str(fpath),
                                "line": i,
                                "snippet": _mask_secret(line.strip()[:120]),
                                "fix": "Remove hardcoded secrets, use environment variables or a vault",
                            })
            except Exception:
                pass

    # Deduplicate
    seen = set()
    deduped = []
    for f in all_findings:
        key = (f["rule_id"], f["file"], f.get("line", 0), f.get("snippet", "")[:40])
        if key not in seen:
            seen.add(key)
            deduped.append(f)

    # Count files
    total_files = sum(len(v) for v in classified.values())

    report = {
        "project_context": {
            "project_root": str(root),
            "files_scanned": total_files,
            "file_types": {k: len(v) for k, v in classified.items()},
        },
        "findings": deduped,
        "summary": {
            "CRITICAL": sum(1 for f in deduped if f["risk"] == "CRITICAL"),
            "HIGH": sum(1 for f in deduped if f["risk"] == "HIGH"),
            "MEDIUM": sum(1 for f in deduped if f["risk"] == "MEDIUM"),
            "LOW": sum(1 for f in deduped if f["risk"] == "LOW"),
        },
        "timestamp": datetime.now(CST).isoformat(),
    }

    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    elif args.format == "text":
        print(render_text(report))
    else:
        print(render_markdown(report))

    exit_code = 1 if report["summary"]["CRITICAL"] > 0 else 0
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
