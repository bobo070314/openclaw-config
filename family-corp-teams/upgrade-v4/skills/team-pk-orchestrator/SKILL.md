---
name: team-pk-orchestrator
description: "IGP team-pk-orchestrator skill"
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

# Team Pk Orchestrator Skill
# team-pk-orchestrator Skill

## Description
Orchestrate department PK rounds

## Metadata
- version: 1.0
- author: IGP v4 self-bootstrapping
- category: development
- tags: [team, pk, orchestrator, skill]

## Instructions
1. Parse and validate input parameters including department ID, round duration, participant list, and scoring rules.
2. Coordinate scheduling across team calendars, reserve required collaboration tools (e.g., video conferencing, shared whiteboards), and notify all participants with agenda and pre-round materials.
3. Launch and monitor live PK execution: track time, enforce turn-based speaking, capture real-time scoring inputs from judges, and handle mid-round contingencies (e.g., disconnections, disputes).
4. Aggregate results, generate performance analytics and feedback summaries per participant, archive session artifacts, and trigger follow-up actions (e.g., coaching assignments, leaderboard updates).

## Usage
/team-pk-orchestrator --dept-id <id> --duration <minutes> --participants <list> --scoring-mode <mode>