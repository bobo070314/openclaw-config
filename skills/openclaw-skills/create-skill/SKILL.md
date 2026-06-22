---
name: create-skill
description: >
  Bootstrap a new OpenClaw skill with Context Snapshot. Scans
  workspace for related code (imports, exports, function signatures)
  and embeds findings into the generated SKILL.md. Use when user
  says "create a skill", "scaffold a new tool", "make a skill for ...".
metadata:
  openclaw:
    requires:
      bins: ["python"]
---

# Create Skill (Skill Factory) v0.2.0

## What's new in v0.2.0
- **Context Snapshot**: scans your workspace for code related to the skill's description keywords. Finds function signatures, imports, exports, class definitions in `.ts`, `.tsx`, `.py`, `.js`, `.jsx` files.
- **Cross-platform**: delegates to Python for file scanning (no ripgrep dependency).
- **Four output files**: `SKILL.md` (with context snapshot), `_meta.json`, `run.sh`, `run.bat`.

## When to use
- User says "create a skill called ..."
- User says "scaffold a new skill" / "make a new tool"
- Need to bootstrap SKILL.md, _meta.json, run.sh into skills/openclaw-skills/<name>/

## How to invoke

```bash
bash "{baseDir}/run.sh" "<skill-name>" "<description>" "[target-dir]"
```

or on Windows:

```bat
run.bat <skill-name> <description> [target-dir]
```

## Parameters
- `$1` = skill name (lowercase, hyphens allowed; e.g. `image-resizer`)
- `$2` = description (used as keywords for workspace scan)
- `$3` = target directory (optional, default: `skills/openclaw-skills/`)

## Exit codes
- `0` = created or already exists (idempotent)
