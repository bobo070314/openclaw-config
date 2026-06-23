---
name: sandbox-executor
description: Isolated Docker sandbox execution for AI-generated code
version: 0.1.0
category: safety
enabled: true
---

# sandbox-executor v0.1.0

Isolated execution gateway. Every AI-generated script execution MUST go through this.

## Safety Guarantees

| Guarantee | Mechanism |
|-----------|-----------|
| Immutable root FS | `--read-only` |
| No network | `--network none` (opt-in) |
| Memory cap | `--memory 512m` |
| CPU cap | `--cpus 1` |
| Fork bomb protection | `--pids-limit 100` |
| No privilege escalation | `--security-opt no-new-privileges` |
| Non-root | `USER sandbox` |
| Ephemeral /tmp | `--tmpfs /tmp:rw,noexec,nosuid,size=64M` |

## Usage

```bash
# Basic execution
python skills/sandbox-executor/run.py security-audit --target workspace/test.py

# With network (explicit opt-in)
python skills/sandbox-executor/run.py web-scraper --url https://example.com --allow-network

# Force rebuild image
python skills/sandbox-executor/run.py any-skill --build
```

## Logging

All executions are logged to `.deploy/logs/sandbox.jsonl` with structured JSON entries.
