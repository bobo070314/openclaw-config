# Project Directory Tree

## Root
- .claude/ -- Agent configs & rules
  - .claude/rules/ -- coding.md, git.md, agent.md
  - .claude/settings.json -- permissions & model config
- .claude/skills/ -- (empty, will add later)
- AGENTS.md -- Main agent config
- CLAUDE.md -- Project overview & model pin
- SOUL.md -- Agent personality
- TOOLS.md -- Local notes
- openclaw-minimal.json -- Gateway config
- directory_tree.md -- This file

## Workspace
- workspace/ -- Development workspace
  - workspace/AGENTS.md -- Agent config (sync'd)
  - workspace/family-corp-teams/ -- 11 team dirs (git-tracked)
    - 5/ -- Main version
      - 5/chromosomes/ -- a2a, provider, skills, guardian, mcp
      - 5/silicon_memory_pkg/ -- Memory system
      - 5/deploy/, 5/tests/, 5/v6/ -- infra & tests
    - 6/ -- Next version
    - bsorb/, job_descriptions/, mcp_servers/, pk_battle/, 	ests/, 6/, _tmp_kb_test/

## Config
- config/ -- Runtime configs
- .env -- Environment variables

## Infrastructure
- scripts/ -- Utility scripts
- cron/ -- Scheduled tasks
- gateway_wrapper.cmd -- Gateway launcher
