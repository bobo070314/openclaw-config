#!/usr/bin/env python3
"""
archive_b_line_report.py — Archive B-line observation data after 24h window.
Moves evolution_status.json + hardcases.jsonl into reports/YYYYMMDD/.

Usage:
    python scripts/archive_b_line_report.py [--force]
"""

import argparse, json, shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ARCHIVE_DIR = ROOT / "reports"

def archive():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Overwrite existing archive")
    args = parser.parse_args()

    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    dest = ARCHIVE_DIR / date_str
    dest.mkdir(parents=True, exist_ok=True)

    sources = [
        ROOT / "data" / "runs" / "evolution_status.json",
        ROOT / "data" / "evals" / "hardcases.jsonl",
        ROOT / "data" / "runs" / "latest_eval.json",
    ]

    archived = []
    for src in sources:
        if src.exists():
            dst = dest / src.name
            if not dst.exists() or args.force:
                shutil.copy2(str(src), str(dst))
                archived.append(str(dst))
                print(f"  ✅ {src.name} → {dst}")
            else:
                print(f"  ⏭️  {src.name} already exists, use --force to overwrite")
        else:
            print(f"  ⚠️  {src.name} not found")

    summary = {
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "archive_path": str(dest),
        "files": archived,
    }
    summary_path = dest / "archive_manifest.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  ✅ Manifest written to {summary_path}")
    print(f"  📍 Archive root: {dest}")


if __name__ == "__main__":
    archive()
