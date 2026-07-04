#!/usr/bin/env python3
"""
Generate workspace snapshot for rollback/recovery reference.
Output: snapshots/20260704_<time>_workspace_snapshot.json
"""
import json, subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git(args: list[str]) -> str:
    r = subprocess.run(
        ["git", "-C", str(ROOT)] + args,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return r.stdout.strip()


snap = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "git_log": git(["log", "--oneline", "-10"]),
    "tags": git(["tag", "-l"]).split("\n"),
    "head_ref": git(["rev-parse", "HEAD"]),
    "b_line_status": None,
}

# Load evolution status
evo = Path(ROOT / "data" / "runs" / "evolution_status.json")
if evo.exists():
    snap["b_line_status"] = json.loads(evo.read_text(encoding="utf-8"))

# Write snapshot
out_dir = ROOT / "snapshots"
out_dir.mkdir(parents=True, exist_ok=True)
ts = datetime.now().strftime("%Y%m%d_%H%M")
out_path = out_dir / f"{ts}_workspace_snapshot.json"
out_path.write_text(json.dumps(snap, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"✅ Snapshot written to {out_path}")
print(f"   HEAD: {snap['head_ref'][:12]}")
print(f"   Tags: {', '.join(snap['tags'])}")
