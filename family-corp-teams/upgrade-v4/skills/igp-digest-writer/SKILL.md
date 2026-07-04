---
name: igp-digest-writer
description: "Writes structured documentation: JSON reports + Markdown summaries + Memory updates for IGP daily logs."
license: MIT
compatibility:
 - igp-v4
metadata:
 author: IGP v4
 version: 1.0.0
 tags:
  - documentation
allowed-tools:
 - read
 - write
 - exec
---

# Igp Digest Writer Skill

## When to Activate
Activate this skill at the end of each IGP daily log processing cycle—specifically after raw log ingestion, parsing, and preliminary analysis are complete—when the system requires authoritative, human-readable summaries, machine-parsable JSON reports, and persistent memory updates reflecting key insights, anomalies, or action items.

## Instructions
1. **Read latest IGP daily log data** using `read` with path `/logs/igp/daily/latest.json` (or fallback to `/logs/igp/daily/YYYY-MM-DD.json` if timestamped).
2. **Generate three artifacts**:  
   - A validated JSON report (`digest-report.json`) containing structured fields: `date`, `summary`, `key_metrics`, `anomalies`, `action_items`, and `confidence_score`.  
   - A concise Markdown summary (`digest-summary.md`) with headings: `## Overview`, `## Key Observations`, `## Notable Anomalies`, and `## Next Steps`.  
   - A memory update patch (`memory-patch.json`) in IGP memory schema format, targeting `/igp/digest/history` with `append: true` and including `timestamp`, `digest_id`, and `summary_ref`.
3. **Write all three artifacts** using `write`: JSON report to `/reports/igp/digest/YYYY-MM-DD.json`, Markdown summary to `/docs/igp/digest/YYYY-MM-DD.md`, and memory patch to `/memory/igp/digest-patch.json`.
4. **Validate outputs** via `exec` running `igp-validate-digest --strict` on the JSON report and Markdown summary; fail gracefully with error log if validation fails.
5. **Confirm completion** by emitting a structured success event: `{ "skill": "igp-digest-writer", "status": "completed", "artifacts": ["digest-report.json", "digest-summary.md", "memory-patch.json"] }`.

## Examples
On 2024-06-15, after ingesting `/logs/igp/daily/2024-06-15.json`, the skill reads the log, detects 3 latency spikes and 1 config drift alert, writes `/reports/igp/digest/2024-06-15.json` (with `"anomalies": [{"type":"latency_spike","count":3},{"type":"config_drift","count":1}]`), generates `/docs/igp/digest/2024-06-15.md` with clear bullet-point observations, and appends a memory patch referencing the digest ID `igp-digest-20240615-7a2f` to `/memory/igp/digest-patch.json`.

## Notes
- Always use ISO 8601 date formatting (e.g., `2024-06-15`) in filenames and JSON fields.  
- The JSON report must conform to the IGP Digest Schema v1.2 — refer to `/schemas/igp-digest-v1.2.json` for validation rules.  
- Never overwrite existing digest files; abort with error if target paths already exist unless `--force` is explicitly enabled (not permitted in production).  
- Memory updates must include `source_skill: "igp-digest-writer"` and `version: "1.0.0"` for traceability.