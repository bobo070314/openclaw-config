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

## 5. Industry Integration Example — Hesheng Silicon (合盛硅业)

### Scenario A: Anode Crack on Silicon Substrate

A production-line vision system detects a micro-crack on a silicon negative electrode surface.
The protocol translates this physical defect into a machine-actionable repair:

```json
{
  "run_id": "hs-20260704-001",
  "timestamp": "2026-07-04T08:30:00+08:00",
  "target_substrate": "silicon",
  "fault_type": "crack",
  "repair_strategy": "S1",
  "entropy_level": "NORMAL",
  "pass_rate_before": 0.73,
  "pass_rate_after": 0.91
}
```

**Outcome:** S1 thermal anneal applied. Yield increased from 73% → 91%.
Protocol logs the action. Gate role receives a notification if post-repair pass_rate < 1.0.

### Scenario B: Electrolyte Contamination

Batch of lithium-ion electrolyte shows trace metal contamination.
Protocol handles it as a non-code physical defect:

```json
{
  "run_id": "hs-20260704-002",
  "timestamp": "2026-07-04T09:15:00+08:00",
  "target_substrate": "electrolyte",
  "fault_type": "contamination",
  "repair_strategy": "S2",
  "entropy_level": "CRITICAL",
  "pass_rate_before": 0.42,
  "pass_rate_after": null
}
```

**Outcome:** `entropy_level == CRITICAL` triggers manual intervention.
S2 wash is queued. Gate role blocks further production until verified.
Protocol enforces that `pass_rate_after` cannot be null on close — it forces re-inspection.

### Copy-Paste HTTP Examples

#### Request: Anode Crack → S1 Repair

```http
POST /api/v1/protocol/repair HTTP/1.1
Host: fixer.silicon-body.local
Content-Type: application/json
X-Api-Key: ${API_KEY}

{
  "run_id": "20260704-crack-001",
  "source": "mes.heshan-silicone.com",
  "target_substrate": "silicon",
  "fault_type": "crack",
  "repair_strategy": "S1",
  "entropy_level": "NORMAL",
  "pass_rate_before": 0.73
}
```

**Response (202 Accepted):**
```json
{
  "status": "accepted",
  "protocol_version": "1.0",
  "action_type": "auto_fix",
  "run_id": "20260704-crack-001",
  "estimated_completion": "2026-07-04T08:35:00+08:00"
}
```

#### Request: Electrolyte Contamination → CRITICAL Escalation

```http
POST /api/v1/protocol/repair HTTP/1.1
Host: fixer.silicon-body.local
Content-Type: application/json
X-Api-Key: ${API_KEY}

{
  "run_id": "20260704-contam-002",
  "source": "mes.heshan-silicone.com",
  "target_substrate": "electrolyte",
  "fault_type": "contamination",
  "repair_strategy": "S2",
  "entropy_level": "CRITICAL",
  "pass_rate_before": 0.42
}
```

**Response (403 Forbidden + Violation Logged):**
```json
{
  "status": "rejected",
  "protocol_version": "1.0",
  "reason": "CRITICAL entropy requires manual intervention",
  "gate_notified": true,
  "violation_id": "v-20260704-contam-002"
}
```

### Integration Steps (for Hesheng MES Team)

1. **Configure API Key** — Add `X-Api-Key` header with your provisioned key.
2. **POST defects** — Send JSON payload to `POST /api/v1/protocol/repair`.
3. **Handle response** — `202` = auto-fix queued, `4xx` = needs attention.
4. **Check status** — `GET /api/v1/protocol/status/{run_id}` returns current state + pass_rate.
5. **Close loop** — When repair completes, protocol POSTs back to MES callback URL.

> No changes to factory-floor PLCs or SCADA required. MES only needs HTTP outbound.

## 6. Compatibility

- **Pipeline**: `orchestrator.py` v1.0.1+
- **RBAC**: `gate` role has `trigger_rollback` permission — rollback is a protocol-level action
- **Reporting**: `violations.jsonl` accepted, rejected, and escalated actions
- **MES Integration**: HTTP POST to `/api/v1/protocol/repair` with protocol JSON schema
