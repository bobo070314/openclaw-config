---
name: add-setting-env
description: "Validate environment variables — compares .env against .env.example, reports missing keys with defaults, masks secrets, shows coverage. Use when user asks to 'check env vars', 'verify environment', 'audit .env file', or 'what env vars am I missing'."
metadata:
  openclaw:
    requires:
      bins: ["python"]
---

# Environment Variable Validator v0.2.0

## What's new
- Scans `.env.example` / `.env.template` and compares against actual `.env`
- Reports missing variables with their default values
- Masks sensitive values (SECRET, KEY, TOKEN, PASSWORD, PWD)
- Monorepo-aware: checks one level deep for sub-project env files
- Coverage percentage summary

## When to use
- User says "check my env vars" / "verify environment" / "audit .env"
- "what env vars am I missing" / "validate .env"
- Before deployment to ensure all required env is set

## How to invoke

```bash
bash "{baseDir}/run.sh" "<project-dir>"
```

## Parameters
- `$1` = project directory path (required)

## Exit codes
- `0` = all required vars present
- `1` = one or more variables missing
