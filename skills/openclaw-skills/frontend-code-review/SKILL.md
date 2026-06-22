---
name: frontend-code-review
description: >
  ESLint-powered frontend code review for TypeScript/React projects.
  Parses ESLint JSON output, enriches with symbol cross-references
  (function definitions, class locations), suggests fixes, and reports
  a 0-100 quality score. Two modes: quick single-file review or deep
  directory scan. Use when user says "code review", "review this file",
  "check code quality", "lint project", "audit frontend".
metadata:
  openclaw:
    requires:
      bins: ["python", "npx"]
---

# Frontend Code Review v0.2.0

## What's new
- **Not just an ESLint wrapper**: symbol cross-references locate where
  functions/classes are defined, giving context beyond the error message
- **Fix suggestions**: 12 common ESLint rules mapped to actionable fixes
- **Quality score**: 0-100 based on error/warning/file counts
- **Three output formats**: text (terminal), markdown (PR comments), JSON (API)
- **Project context**: auto-detects framework version, ESLint config, ruleset

## When to use
- User says "code review" / "review this file" / "check quality"
- "lint my project" / "audit frontend code" / "find issues"
- Pre-commit check / PR quality gate

## How to invoke

```bash
# Quick single-file review
bash "{baseDir}/run.sh" --file src/components/Login.tsx

# Deep directory scan
bash "{baseDir}/run.sh" --src src/

# Markdown report (for PR comments)
bash "{baseDir}/run.sh" --src src/ --format markdown

# JSON output (for scripting)
bash "{baseDir}/run.sh" --src src/ --format json
```

## Parameters
| Flag | Description |
|------|-------------|
| `--file <path>` | Single file to review |
| `--src <dir>` | Source directory for deep scan |
| `--format text\|json\|markdown` | Output format (default: text) |
| `--project-dir <dir>` | Project root for config detection |

## Example output
```
📋 Frontend Code Review Report
--- Project Context ---
  Framework     : react
  React         : v18.2.0
  ESLint        : ^8.50.0

--- Summary ---
  Files scanned : 12
  Errors        : 3
  Warnings      : 7
  Score         : 🟡 76/100

--- Issues Detail ---
  📄 src/auth/login.tsx
     🔴 L42:5 [no-unused-vars] 'handleSubmit' is defined but never used
         → Defined at: src/hooks/useAuth.ts:15
            export function handleSubmit(credentials: Credentials)
         💡 Fix: Remove unused variable or prefix with '_'
```

## Exit codes
- `0` = clean or warnings only
- `1` = errors found
