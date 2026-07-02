# Caliber Optimization

## Purpose
Maintain Caliber score above 80 by keeping agent configs fresh, adding project references, and ensuring valid file paths.

## Checklist
- [ ] All file references in CLAUDE.md and AGENTS.md point to real files
- [ ] Minimum 3 executable code blocks in CLAUDE.md
- [ ] .claude/skills/ has 2-3 workflow skills
- [ ] Project directories referenced in config match git-tracked files
- [ ] Run after every significant config change: `caliber score`

## Commands
```powershell
caliber score --json --quiet
caliber refresh
```
