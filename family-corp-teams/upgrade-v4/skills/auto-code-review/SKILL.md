---
name: auto-code-review
description: "IGP auto-code-review skill"
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

# Auto Code Review Skill
# auto-code-review Skill

## Description
Automated code review using v4 CodeReviewAgent

## Metadata
- version: 1.0
- author: IGP v4 self-bootstrapping
- category: development
- tags: [auto, code, review, skill]

## Instructions
1. Parse the input source code and associated context (e.g., language, framework, PR diff, or file path).
2. Invoke the v4 CodeReviewAgent with configured linting rules, security checks, best practices, and style guidelines.
3. Aggregate findings into structured feedback: severity-ranked issues, line-specific annotations, and actionable remediation suggestions.
4. Format and return concise, human-readable review output with optional JSON export for CI/CD integration.

## Usage
/auto-code-review [params]