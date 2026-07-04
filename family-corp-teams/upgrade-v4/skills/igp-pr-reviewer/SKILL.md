---
name: igp-pr-reviewer
description: "Reviews PRs with IGP PK scoring: quality(1-10), token_cost tracking, and elimination recommendations."
license: MIT
compatibility:
 - igp-v4
metadata:
 author: IGP v4
 version: 1.0.0
 tags:
  - code-quality
allowed-tools:
 - read
 - write
 - exec
---

# Igp Pr Reviewer Skill

## When to Activate
Activate this skill when a pull request is opened or updated in a repository governed by IGP v4 policies, and the PR requires formal quality assessment—especially for critical paths, security-sensitive changes, or high-impact features. Do not activate for trivial documentation updates or automated dependency bumps unless explicitly requested.

## Instructions
1. Use `read` to fetch the full PR diff, title, description, and associated issue/epic context (if linked).  
2. Evaluate code quality using IGP PK scoring criteria: correctness, maintainability, test coverage, security hygiene, and adherence to style guides — assign an integer score from 1–10.  
3. Estimate token cost of the PR’s diff + review rationale using IGP’s standard LLM tokenization model (e.g., `cl100k_base`) and log it under `token_cost`.  
4. Determine if the PR should be eliminated (i.e., rejected outright) based on critical flaws: unpatched CVEs, missing tests for new logic, or violation of core architectural constraints — provide concise elimination rationale if applicable.  
5. Use `write` to post a structured comment in the PR with: `[IGP PK] Quality: X/10 | Token Cost: Y | Elimination: [Yes/No] — [Rationale]`.

## Examples
PR #42 adds a new auth middleware in `src/auth/middleware.ts`. The diff introduces a JWT validation bypass due to unchecked `algorithm` field. IGP PK scoring yields Quality: 3/10; token_cost = 1842; elimination recommended due to critical security flaw. Output comment: `[IGP PK] Quality: 3/10 | Token Cost: 1842 | Elimination: Yes — JWT algorithm validation omitted; allows arbitrary signature forgery.`

## Notes
- Elimination recommendations must cite specific lines and standards (e.g., “violates IGP-Sec-2.1”).  
- Token cost must include both diff parsing and review generation overhead — never omit baseline overhead (min 256 tokens).  
- Never approve or merge; this skill is strictly advisory. Always defer final disposition to human maintainers.