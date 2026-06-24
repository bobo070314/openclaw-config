---
name: causal-reasoner
version: 0.2.0
description: "Causal DAG engine — infers root cause from observed effects using Bayesian-weighted evidence chains"
enabled: true
category: intelligence
tags: [causal, reasoning, root-cause, bayesian, diagnostics]
---

# 🔮 causal-reasoner

Causal inference engine. Takes observed effects (CPU spike, memory pressure, deploy events) and backtracks through a directed acyclic causal graph with weighted evidence scoring.

## Architecture

```
[git_push] ──→ [deploy] ──→ [cpu_load]
                              ├──→ [memory_usage]
[config_change] ─────────────┘
[high_traffic] ──────────────┘
```

## Usage

```bash
python causal-reasoner/run.py --infer cpu_load              # infer root cause
python causal-reasoner/run.py --infer memory_usage --json    # JSON output
python causal-reasoner/run.py --evidence-path daemon/state.json  # read daemon state
python causal-reasoner/run.py --list-graph                   # dump causal DAG
python causal-reasoner/run.py --version
python causal-reasoner/run.py --dry-run --infer cpu_load
```

## Integration

- Reads daemon state from `skills/.daemon/state.json`
- Writes reasoning logs to `skills/causal-reasoner/logs/reasoning.jsonl`
- Scoring: Bayesian-weighted evidence chain with confidence decay (0.85^n)
- Used by `subconscious-daemon` to suppress expected alerts (e.g. deployment → CPU spike)
