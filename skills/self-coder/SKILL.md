---
name: self-coder
description: AI self-modification engine — reads skill code, generates improved drafts
version: 0.2.0
category: evolution
enabled: true
---

# self-coder v0.1.0

AI-powered code optimization engine. Reads a skill's SKILL.md + run.py, generates an improved draft in `workspace/drafts/<skill>/run.py`.

## Safety Guarantee
- **NEVER overwrites original files** — only writes to `workspace/drafts/`
- Requires explicit human review before applying changes

## Usage
```bash
python skills/self-coder/run.py security-audit
python skills/self-coder/run.py security-audit --dry-run
```
