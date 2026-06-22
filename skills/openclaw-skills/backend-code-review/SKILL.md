---
name: backend-code-review
description: >
  Python backend code review + security audit. Runs pylint/flake8 linting,
  AST-based Django/FastAPI pattern detection (views, ORM queries, routers,
  dependency injection), and 10-category security scan (SQL injection,
  N+1 queries, hardcoded secrets, unsafe deserialization, eval/exec,
  command injection, DEBUG=True, ALLOWED_HOSTS wildcard, CSRF bypass).
  Generates markdown report with risk levels (HIGH/MEDIUM/LOW) and fix
  examples. Use when user says "review backend", "audit Python code",
  "security scan", "check Django/FastAPI", "backend code review".
metadata:
  openclaw:
    requires:
      bins: ["python"]
---

# Backend Code Review & Security Audit v0.2.0

## Three-Layer Analysis
1. **Linting** — pylint (primary) or flake8 (fallback) with JSON parsing
2. **AST Framework Detection** — identifies Django views, FastAPI endpoints,
   ORM query patterns, router registrations
3. **Security Scanner** — 10 vulnerability categories, regex-based with
   line-level precision

## Security Rules (10 categories)

| Rule ID | Name | Risk |
|---------|------|------|
| SEC-001 | SQL Injection — raw SQL with f-string/format/%s | 🔴 HIGH |
| SEC-002 | SQL Injection — Django .raw()/.extra() with interpolated values | 🔴 HIGH |
| SEC-003 | Potential N+1 query — ORM in loop without prefetch | 🟡 MEDIUM |
| SEC-004 | Hardcoded secret (password/token/key/API key) | 🔴 HIGH |
| SEC-005 | Unsafe deserialization — pickle.loads/yaml.load | 🔴 HIGH |
| SEC-006 | Dynamic code execution — eval()/exec()/compile() | 🔴 HIGH |
| SEC-007 | DEBUG=True — production misconfiguration | 🟡 MEDIUM |
| SEC-008 | ALLOWED_HOSTS=['*'] — Django wildcard | 🟡 MEDIUM |
| SEC-009 | Command injection — os.system/subprocess shell=True | 🔴 HIGH |
| SEC-010 | Missing CSRF protection — @csrf_exempt | 🟡 MEDIUM |

## When to use
- User says "review backend" / "audit Python code" / "security scan"
- "check Django/FastAPI project" / "find vulnerabilities"
- Pre-deployment security audit

## How to invoke

```bash
# Full directory audit (markdown report)
bash "{baseDir}/run.sh" --src api/

# AST + security only (no linter)
bash "{baseDir}/run.sh" --src api/ --no-linter

# Single file review
bash "{baseDir}/run.sh" --file views.py

# JSON output for CI pipeline
bash "{baseDir}/run.sh" --src api/ --format json
```

## Parameters
| Flag | Description |
|------|-------------|
| `--src <dir>` | Source directory to scan |
| `--file <path>` | Single Python file to review |
| `--format markdown\|text\|json` | Output format (default: markdown) |
| `--project-dir <dir>` | Project root for dependency/config detection |
| `--no-linter` | Skip pylint/flake8 — AST + security only |

## Exit codes
- `0` = no HIGH severity findings
- `1` = HIGH severity findings detected

## Context Snapshot (auto-generated)
_Scanned D:/bobo/openclaw-foreign/workspace/gh-enterprise-baseline_
### Dify API
- `DifyApp` (class) — Flask app factory
- `create_flask_app_with_configs()` — app initialization
- `AgentBackendRunClient` / `DifyAgentBackendRunClient` (classes) — RPC clients
- Celery entrypoints with gevent/grpc integration
- Gunicorn post_patch hooks
