---
name: skill-generator
description: "IGP skill-generator skill"
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

# Skill Generator Skill
# skill-generator Skill

## Description
Generate new IGP Skills via LLM

## Metadata
- version: 1.0
- author: IGP v4 self-bootstrapping
- category: development
- tags: [skill, generator, skill]

## Instructions
1. Parse and validate input parameters including skill name, description, category, tags, and optional template constraints.
2. Construct a precise LLM prompt conforming to the IGP SKILL.md specification format and enforced structural rules.
3. Invoke the configured LLM with temperature=0.1 and max_tokens=2048 to generate a complete, syntactically valid SKILL.md file.
4. Validate the LLM output against the IGP skill schema (headers, metadata fields, required sections) and reject or regenerate on failure.

## Usage
/skill-generator --name "<skill-name>" --desc "<description>" --category "<category>" --tags "<tag1>,<tag2>" [--template "<custom-template>"]