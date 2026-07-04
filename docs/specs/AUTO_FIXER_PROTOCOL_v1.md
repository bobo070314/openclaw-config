# Auto-Fixer Protocol v1 (Silicon Substrate Binding)

> Bridges the gap between Logical Bugs (Software) and Physical Defects (Silicon Substrates).
> Version: 1.0 | Status: DRAFT | Date: 2026-07-04

## 1. Core Philosophy

Every software anomaly maps to a substrate-level fault class.
The fixer does not guess — it classifies, binds, and executes.

```
Fault Detected → Classify (protocol schema) → Bind (substrate) → Execute (strategy) → Verify (pass_rate)
```

## 2. Message Schema

Every repair action must follow this JSON structure:

```json
{
  "run_id": "<uuid>",
  "timestamp": "<ISO-8601>",
  "target_substrate": "<silicon|lithium_anode|sic_wafer|electrolyte>",
  "fault_type": "<crack|contamination|config_error|entropy_drift>",
  "repair_strategy": "<S1|S2|S3|S4>",
  "entropy_level": "<NORMAL|LOW_ENTROPY|CRITICAL>",
  "pass_rate_before": "<0.0-1.0>",
  "pass_rate_after": "<0.0-1.0>"
}
```

### Fault Type Definitions

| Fault | Description | Typical Strategy |
|-------|-------------|-----------------|
| `crack` | Physical fracture on substrate surface | S1: Thermal anneal |
| `contamination` | Foreign particle or chemical residue | S2: Chemical wash |
| `config_error` | Parameter misalignment in agent chain | S3: Config rollback |
| `entropy_drift` | Performance decay without clear root cause | S4: Re-cluster + re-train |

## 3. Deception Resistance

Hard thresholds that trigger escalation, not silence:

| Condition | Action |
|-----------|--------|
| `entropy_level == LOW_ENTROPY` | Log only, no escalation (expected) |
| `pass_rate < 1.0` | Escalate: log + notify + flag run_id |
| `block_count > 0` | Escalate: freeze pipeline, trigger rollback |
| `repeat_rate > 20%` | Escalate: mark substrate for deep inspection |

### Enforcement

```python
def enforce_protocol(action: dict) -> dict:
    """Validate and classify a repair action through the protocol."""
    errors = []
    for field in ["run_id", "target_substrate", "fault_type", "repair_strategy"]:
        if field not in action:
            errors.append(f"missing_field:{field}")

    if errors:
        return {"status": "rejected", "errors": errors}

    threshold_map = {
        "LOW_ENTROPY": (None, "log_only"),
        "NORMAL": (0.5, "auto_fix"),
        "CRITICAL": (0.8, "manual_intervention"),
    }
    entropy_level = action.get("entropy_level", "NORMAL")
    escalation_threshold, action_type = threshold_map.get(entropy_level, (0.5, "auto_fix"))

    return {
        "status": "accepted",
        "protocol_version": "1.0",
        "action_type": action_type,
        "escalation_threshold": escalation_threshold,
        "pass_rate_before": action.get("pass_rate_before", 1.0),
    }
```

## 4. Protocol Lifecycle

```
[Detect] → [Enforce Protocol] → Accepted? → [Execute Strategy] → [Verify]
                                              ↓
                                         Rejected → [Log Violation] → [Notify Gate]
```

## 5. Compatibility

- **Pipeline**: `orchestrator.py` v1.0.1+
- **RBAC**: `gate` role has `trigger_rollback` permission — rollback is a protocol-level action
- **Reporting**: `violations.jsonl` accepted, rejected, and escalated actions
