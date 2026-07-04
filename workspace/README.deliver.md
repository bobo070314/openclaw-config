# OpenClaw Delivery Package v1.0.1

Silicon Base Group — "30-second startup, zero-maintenance."

## System Requirements

- **OS**: Windows 10/11 or Windows Server 2019+
- **Runtime**: Python 3.10+ (no dependencies required for basic operation)
- **Disk**: Minimum 200 MB free space
- **Memory**: Minimum 512 MB RAM
- **Network**: Not required for local operation

## Quick Start

```powershell
# Step 1: Initialize environment
.\scripts\init.ps1
# Expected output: INIT: OK

# Step 2: Run the full pipeline
.\scripts\run_all.ps1
```

## Verification

After running, check `data/runs/latest_eval.json`:
- `pass_rate`: 1.0 means system is healthy
- `cost_breakdown`: Shows token consumption per department

## Known Limitations

1. **Windows-only**: This release supports Windows hosts only. Linux/macOS support is planned for v1.2.
2. **Single-instance**: Running multiple pipelines concurrently may cause resource contention — stress testing is in progress.
3. **RBAC current scope**: RBAC enforcement covers file operations only; network access control is planned for v1.1.
4. **Auto-rollback scope**: Rollback restores configuration files only. Data files are preserved.

## SHA256

```
0A75C289B9E407DEC7589375C1E015E85B7C1B0AD6E44B63A1A3345CBDBFC1576
```

## License

Proprietary — Silicon Base Group. All rights reserved.
