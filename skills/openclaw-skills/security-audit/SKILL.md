---
name: security-audit
description: >
  Infrastructure security audit — scans Dockerfile, docker-compose,
  CI/CD workflows (.github, .gitlab-ci, Jenkins), .env files, Terraform,
  shell scripts, private keys (.pem/.key), and JSON/YAML configs for
  hardcoded secrets, misconfigurations, and compliance violations.
  12 rules across 4 risk tiers: CRITICAL (tokens/keys), HIGH (latest tag,
  root user, privileged mode, CI injection), MEDIUM (exposed ports,
  missing .dockerignore), LOW. Generates Markdown report with fix examples.
  Critical findings exit 1. Use when user says "security audit",
  "scan for secrets", "check Dockerfile", "audit infrastructure",
  "review CI/CD security".
metadata:
  openclaw:
    requires:
      bins: ["python"]
---

# Security Audit v0.2.0

## What it scans

| File Type | Scanned | Rules Applied |
|-----------|---------|---------------|
| Dockerfile* | FROM/RUN/EXPOSE/USER | HIGH-001, HIGH-002, MED-001, MED-002 |
| docker-compose*.yml | services/ports/cap_add | HIGH-003, MED-001 |
| .env / .env.* | KEY=VALUE lines | CRIT-001, CRIT-002, CRIT-004, MED-004 |
| .github/workflows/*.yml | steps/secrets/env | CRIT-001, HIGH-004 |
| *.tf / *.tfvars | resource/variable blocks | CRIT-002, CRIT-004 |
| *.pem / *.key / *.crt | file content + magic bytes | CRIT-003 |
| *.sh / *.ps1 | export/assignment lines | CRIT-001, CRIT-004 |
| JSON/YAML configs | recursive key traversal | CRIT-001 |

## Rule List

### 🔴 CRITICAL
| ID | Rule |
|----|------|
| CRIT-001 | GitHub/AWS/API tokens exposed in config/shell/workflow |
| CRIT-002 | AWS Access Key (AKIA/ASIA) hardcoded in Terraform/CI |
| CRIT-003 | Private key file (.pem/.key) committed to repository |
| CRIT-004 | .env file contains real tokens (non-placeholder values) |

### 🟠 HIGH
| ID | Rule |
|----|------|
| HIGH-001 | Dockerfile FROM ...:latest — unreproducible builds |
| HIGH-002 | Dockerfile missing USER directive — runs as root |
| HIGH-003 | docker-compose privileged:true or cap_add:SYS_ADMIN |
| HIGH-004 | CI workflow: secret piped/redirected in shell command |

### 🟡 MEDIUM
| ID | Rule |
|----|------|
| MED-001 | Sensitive port (22/3306/5432/6379/9200) mapped to 0.0.0.0 |
| MED-002 | Dockerfile missing .dockerignore |
| MED-003 | CI/CD missing minimal GITHUB_TOKEN permissions |
| MED-004 | .env not in .gitignore — risk of accidental commit |

## When to use
- User says "security audit" / "scan for secrets" / "check infrastructure"
- "audit Dockerfile" / "review CI/CD security" / "find keys in repo"
- Pre-deployment compliance check

## How to invoke

```bash
# Full audit
bash "{baseDir}/run.sh" /path/to/project

# Text output for terminal
bash "{baseDir}/run.sh" /path/to/project --format text

# JSON for CI pipeline
bash "{baseDir}/run.sh" /path/to/project --format json
```

## Exit codes
- `0` = no CRITICAL findings
- `1` = CRITICAL findings detected (fails CI)
