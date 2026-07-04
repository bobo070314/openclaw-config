# OpenClaw Delivery Package (Customer Guide)

> **Delivery Version:** v1.0<br>
> **Build Date:** 2026-07-04<br>
> **Repository:** igp-life-v3-2026-06-30<br>
> **Phase:** Phase 2 - Productization

## 1) Quick Start

1. Copy `.env.example` to `.env` and fill required values.
2. Run initializer:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\init.ps1
```

Expected output: `INIT: OK`

3. Run main pipeline:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_all.ps1
```

---

## 2) How to Read Reports

Reports live in `data/runs/`.

| Report | What It Tells You |
|--------|------------------|
| `latest_eval.json` | Pass rate, cost breakdown, collaboration chain |
| `rollback_report.json` | Auto-rollback status when something went wrong |

---

## 3) Troubleshooting

### Service unreachable
```powershell
# Check OpenClaw Gateway status
python family-corp-teams/v5/v6/api/igp_heartbeat.py
```

### Rollback
```powershell
.\scripts\auto_rollback.ps1
```

### View logs
```powershell
Get-ChildItem .\logs\* -ErrorAction SilentlyContinue | Get-Content -Tail 50
```

---

## 4) FAQ

**Q: init.ps1 says "unreachable" — is that bad?**
A: No. The health endpoint only responds when the gateway is running. If you haven't started it yet, the warning is normal.

**Q: Can I modify the configuration?**
A: Yes. Edit `configs/agent_chain.yaml` for agent routing, or `.env` for API keys.

**Q: How do I roll back a bad deployment?**
A: Run `.\scripts\auto_rollback.ps1`. The system restores the last known-good state from `data/runs/rollback_report.json`.

---

**Version:** v1.0.0-delivery
**Tech Support:** OpenClaw Family-Corp (IGP)
