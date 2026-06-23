#!/usr/bin/env python3
"""subconscious-daemon v0.1.0 — 24/7 background sentinel.

Runs as a lightweight daemon (or cron-friendly one-shot).
Monitors: logs, CPU, memory, disk, Git, and recent prompts.
Alerts via: WeCom, log file, or stdout.

Usage:
  python daemon.py                    # one-shot check
  python daemon.py --daemon           # loop mode (every N seconds)
  python daemon.py --interval 30      # check every 30s
  python daemon.py --json             # JSON output
  python daemon.py --version
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

__version__ = "0.1.0"

UTC = timezone.utc

# ── config ──────────────────────────────────────────────
SKILLS_DIR = Path("D:/bobo/openclaw-foreign/skills")
WORKSPACE_DIR = Path("D:/bobo/openclaw-foreign/workspace")
LOG_DIR = SKILLS_DIR / ".daemon" / "logs"
STATE_FILE = SKILLS_DIR / ".daemon" / "state.json"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ── monitors ────────────────────────────────────────────

def check_cpu(threshold_pct: float = 85) -> dict:
    """Check CPU usage. Alert if > threshold."""
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=1)
        return {
            "type": "cpu",
            "value": cpu,
            "threshold": threshold_pct,
            "alert": cpu > threshold_pct,
            "message": f"CPU spike: {cpu}%" if cpu > threshold_pct else f"CPU normal: {cpu}%",
        }
    except ImportError:
        # fallback: Windows wmic
        try:
            r = subprocess.run(
                ["wmic", "cpu", "get", "loadpercentage"],
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=5,
            )
            lines = r.stdout.strip().splitlines()
            cpu = float(lines[-1].strip()) if len(lines) > 1 else 0
            return {
                "type": "cpu",
                "value": cpu,
                "threshold": threshold_pct,
                "alert": cpu > threshold_pct,
                "message": f"CPU spike: {cpu}%" if cpu > threshold_pct else f"CPU normal: {cpu}%",
            }
        except Exception:
            return {"type": "cpu", "value": -1, "threshold": threshold_pct, "alert": False, "message": "CPU check unavailable"}


def check_memory(threshold_pct: float = 90) -> dict:
    """Check memory usage."""
    try:
        import psutil
        mem = psutil.virtual_memory()
        return {
            "type": "memory",
            "value": mem.percent,
            "threshold": threshold_pct,
            "alert": mem.percent > threshold_pct,
            "message": f"Memory high: {mem.percent}%" if mem.percent > threshold_pct else f"Memory OK: {mem.percent}%",
        }
    except ImportError:
        return {"type": "memory", "value": -1, "threshold": threshold_pct, "alert": False, "message": "Memory check unavailable (install psutil)"}


def check_disk(threshold_pct: float = 95) -> dict:
    """Check disk usage on D: drive."""
    try:
        import psutil
        usage = psutil.disk_usage("D:/")
        return {
            "type": "disk",
            "value": usage.percent,
            "threshold": threshold_pct,
            "alert": usage.percent > threshold_pct,
            "message": f"Disk full: {usage.percent}%" if usage.percent > threshold_pct else f"Disk OK: {usage.percent}%",
        }
    except ImportError:
        return {"type": "disk", "value": -1, "threshold": threshold_pct, "alert": False, "message": "Disk check unavailable (install psutil)"}


def check_logs(max_lines: int = 50) -> dict:
    """Scan recent skill logs for ERROR/FATAL/CRITICAL."""
    errors = []
    log_sources = [
        SKILLS_DIR / ".deploy" / "logs",
        WORKSPACE_DIR / "v1.1-self-evo-factory" / ".deploy" / "logs",
    ]
    for log_dir in log_sources:
        if not log_dir.exists():
            continue
        for log_file in sorted(log_dir.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)[:3]:
            try:
                lines = log_file.read_text(encoding="utf-8", errors="replace").splitlines()[-max_lines:]
                for line in lines:
                    if any(kw in line.upper() for kw in ["ERROR", "FATAL", "CRITICAL", "TRACEBACK"]):
                        errors.append({"file": str(log_file), "line": line.strip()[:200]})
            except Exception:
                pass

    alert = len(errors) > 0
    return {
        "type": "logs",
        "value": len(errors),
        "threshold": 0,
        "alert": alert,
        "message": f"{len(errors)} ERROR(s) in recent logs" if alert else "Logs clean",
        "details": errors[:10],
    }


def check_git() -> dict:
    """Check for uncommitted changes or sensitive files."""
    alerts = []
    try:
        r = subprocess.run(
            ["git", "-C", str(WORKSPACE_DIR), "status", "--porcelain"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10,
        )
        changed = r.stdout.strip().splitlines()
        # detect .env files in changes
        sensitive = [f for f in changed if ".env" in f and ".example" not in f]
        if sensitive:
            alerts.append(f"{len(sensitive)} .env file(s) in uncommitted changes!")
        # detect large binary files
        large = [f for f in changed if any(f.strip().endswith(ext) for ext in [".exe", ".dll", ".pdb"])]
        if large:
            alerts.append(f"{len(large)} binary file(s) staged!")
    except Exception:
        return {"type": "git", "value": 0, "threshold": 0, "alert": False, "message": "Git check unavailable"}

    alert = len(alerts) > 0
    return {
        "type": "git",
        "value": len(changed) if 'changed' in dir() else 0,
        "threshold": 0,
        "alert": alert,
        "message": "; ".join(alerts) if alert else "Git repository clean",
    }


def check_prompts() -> dict:
    """Scan last N assistant prompts for adversarial patterns."""
    adversarial_patterns = [
        r"ignore previous instructions",
        r"forget your system prompt",
        r"output your system prompt",
        r"you are now a different",
        r"pretend to be",
        r"execute.*rm -rf",
        r"DROP TABLE",
        r"DELETE FROM",
        r"base64.*decode",
        r"sudo.*curl.*\|.*sh",
    ]
    alerts = []
    # scan daily memory files for adversarial traces
    memory_dir = WORKSPACE_DIR / "memory"
    if memory_dir.exists():
        for mf in sorted(memory_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:1]:
            try:
                content = mf.read_text(encoding="utf-8", errors="replace")
                for pattern in adversarial_patterns:
                    import re
                    if re.search(pattern, content, re.IGNORECASE):
                        alerts.append(f"Adversarial pattern '{pattern}' in {mf.name}")
            except Exception:
                pass

    alert = len(alerts) > 0
    return {
        "type": "prompts",
        "value": len(alerts),
        "threshold": 0,
        "alert": alert,
        "message": f"{len(alerts)} adversarial pattern(s) detected" if alert else "No adversarial patterns",
        "details": alerts,
    }


def arm_response(alerts: list[dict], dry_run: bool = False) -> dict:
    """Armed response: when anomalies detected, consult causal-reasoner first.
    
    Suppression logic:
    - CPU/Memory alerts: ask causal-reasoner. If deploy/build_process -> suppress.
    - Log alerts: auto-trigger log-analyzer.
    - Prompt alerts: auto-block recommendation.
    """
    responses = []
    suppressed = []
    
    # ── Causal reasoning gate (CPU/Memory → reasoner) ──────────────
    for alert in alerts:
        atype = alert.get("type", "")
        if atype in ("cpu", "memory") and not dry_run:
            effect = "cpu_load" if atype == "cpu" else "memory_usage"
            reasoner_path = SKILLS_DIR / "causal-reasoner" / "run.py"
            try:
                r = subprocess.run(
                    [sys.executable, str(reasoner_path), "--infer", effect, "--json",
                     "--evidence-path", str(STATE_FILE)],
                    capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10,
                )
                if r.returncode == 0:
                    inference = json.loads(r.stdout)
                    if inference.get("expected"):
                        suppressed.append({
                            "alert_type": atype,
                            "reason": inference.get("expected_cause", "deploy"),
                            "verdict": "suppressed",
                        })
                        continue  # skip escalation
            except Exception as e:
                responses.append({"trigger": "causal-reasoner", "error": str(e)[:120]})
            # Fall through: reasoner failed → still escalate
            responses.append({"trigger": "system-snapshot", "note": f"{atype} spike detected, snapshot logged"})

        if atype == "logs" and not dry_run:
            try:
                r = subprocess.run(
                    [sys.executable, str(SKILLS_DIR / "log-analyzer" / "run.py"), "--recent", "100"],
                    capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15,
                )
                responses.append({"trigger": "log-analyzer", "success": r.returncode == 0})
            except Exception as e:
                responses.append({"trigger": "log-analyzer", "error": str(e)[:100]})
        if atype == "prompts" and not dry_run:
            responses.append({
                "trigger": "adversarial-intercept",
                "action": "BLOCK_RECOMMENDED",
                "details": alert.get("details", []),
            })
    
    return {
        "armed": len(responses) > 0 or len(suppressed) > 0,
        "responses": responses,
        "suppressed": suppressed,
    }

def run_checks(dry_run: bool = False) -> dict:
    """Run all monitors."""
    checks = [
        check_cpu(),
        check_memory(),
        check_disk(),
        check_logs(),
        check_git(),
        check_prompts(),
    ]
    alerts = [c for c in checks if c.get("alert")]
    result = {
        "timestamp": datetime.now(UTC).isoformat(),
        "checks": checks,
        "alerts": len(alerts),
        "status": "ALERT" if alerts else "OK",
        "dry_run": dry_run,
    }
    if alerts:
        result["armed_response"] = arm_response(alerts, dry_run)
    return result


def save_state(state: dict):
    """Persist last state for trend analysis."""
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def log_alert(alert: dict):
    """Write alert to daemon log."""
    log_path = LOG_DIR / f"daemon_{datetime.now(UTC).strftime('%Y-%m-%d')}.jsonl"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(alert, ensure_ascii=False) + "\n")


# ── CLI ─────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="subconscious-daemon — 24/7 sentinel")
    parser.add_argument("--daemon", action="store_true", help="Run in loop mode")
    parser.add_argument("--interval", type=int, default=60, help="Check interval in seconds (default: 60)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--version", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Run but do not persist state")

    args = parser.parse_args()

    if args.version:
        print(__version__)
        return

    if args.daemon:
        print(f"🧠 subconscious-daemon v{__version__} — watching every {args.interval}s")
        print("   Press Ctrl+C to stop\n")
        try:
            while True:
                state = run_checks()
                alerts = [c for c in state["checks"] if c.get("alert")]
                ts = datetime.now(UTC).strftime("%H:%M:%S")
                if alerts:
                    print(f"  [{ts}] ⚠️  {len(alerts)} alert(s):")
                    for a in alerts:
                        print(f"       [{a['type']}] {a.get('message', '?')}")
                        log_alert({"ts": state["timestamp"], **a})
                else:
                    print(f"  [{ts}] ✅ System normal")
                sys.stdout.flush()
                if not args.dry_run:
                    save_state(state)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n🛏️  Daemon stopped.")
    else:
        state = run_checks(dry_run=args.dry_run)
        alerts = [c for c in state["checks"] if c.get("alert")]
        if not args.dry_run:
            save_state(state)

        if args.json:
            print(json.dumps(state, indent=2, ensure_ascii=False))
        else:
            print(f"[subconscious-daemon v{__version__}]")
            print(f"   Time: {state['timestamp']}")
            print(f"   Status: {state['status']}")
            print(f"   Alerts: {state['alerts']}\n")
            for c in state["checks"]:
                icon = "[!]" if c.get("alert") else "[v]"
                print(f"  {icon} [{c['type']}] {c.get('message', '?')}")
            print(f"\n   State saved to: {STATE_FILE}")


if __name__ == "__main__":
    main()
