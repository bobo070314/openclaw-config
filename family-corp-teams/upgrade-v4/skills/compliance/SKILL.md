---
name: compliance
description: "IGP compliance skill"
license: MIT
compatibility:
 - igp-v4
 - claude-code
 - cursor
 - codex
metadata:
 author: IGP v4
 version: 1.0.0
 tags:
  - general
allowed-tools:
 - read
 - write
 - exec
 - web_search
---

# Compliance Skill
# compliance Department Skill

## Description
安全审计/合规/权限Skills

## Metadata
- version: 1.0
- author: IGP compliance team
- category: department
- tags: [compliance, department, skill]
- department: compliance
- teams: 3 active teams

## Teams
  - team1
  - team2
  - team3

## Instructions
1. Load department context from IGP engine
2. Execute department-specific tasks using v4 engine tools
3. Report results back to IGP engine for KPI tracking
4. Participate in department PK rounds

## Usage
/execute compliance [task] [params]
