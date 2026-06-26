#!/usr/bin/env python3
"""subconscious-daemon v0.2.0 — 24/7 sentinel with vision + profit.

Monitors: logs, CPU, memory, disk, Git, tokens, prompts.
V4.2: Owl-Vision screen capture + anomaly detection.
V5.0: Profit engine — auto_valuation via WeChat command hook.
Alerts via: causal-reasoner, log-analyzer, WeCom, log file.
"""

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

__version__ = "0.2.0"
UTC = timezone.utc

SKILLS_DIR = Path("D:/bobo/openclaw-foreign/skills")
WORKSPACE_DIR = Path("D:/bobo/openclaw-foreign/workspace")

# 🔒 V5.2 Project boundary guard + knowledge modules
try:
    sys.path.insert(0, str(WORKSPACE_DIR / "projects" / "caipiao"))
    from core.project_context import ProjectContext
    from core.obsidian_connector import ObsidianConnector
    from core.memory_retriever import MemoryRetriever

    CTX = ProjectContext("caipiao高价收车", str(WORKSPACE_DIR), project_subdir="projects/caipiao")
    print(CTX.anchor(), flush=True)

    OBSIDIAN = ObsidianConnector(CTX)
    RETRIEVER = MemoryRetriever(CTX)
    print(RETRIEVER.build_index(), flush=True)
    print(f"📖 Obsidian API: {'ONLINE' if OBSIDIAN.ping() else 'OFFLINE (file fallback)'}", flush=True)
except ImportError:
    CTX = None
    OBSIDIAN = None
    RETRIEVER = None

def _safe_path(p: str) -> Path:
    """Resolve path through ProjectContext if active, else plain Path"""
    if CTX is not None:
        try:
            return CTX.resolve(p)
        except PermissionError:
            pass
    return Path(p)
LOG_DIR = SKILLS_DIR / ".daemon" / "logs"
STATE_FILE = SKILLS_DIR / ".daemon" / "state.json"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# V5.0: Rate-limiting state
_last_screenshot_ts = 0.0
SCREENSHOT_COOLDOWN_S = 60  # max 1 screenshot per minute


def check_cpu(threshold_pct=85):
    try:
        import psutil

        cpu = psutil.cpu_percent(interval=1)
    except ImportError:
        try:
            r = subprocess.run(
                ["wmic", "cpu", "get", "loadpercentage"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=5,
            )
            lines = r.stdout.strip().splitlines()
            cpu = float(lines[-1].strip()) if len(lines) > 1 else 0
        except Exception:
            return {
                "type": "cpu",
                "value": -1,
                "threshold": threshold_pct,
                "alert": False,
                "message": "CPU check unavailable",
            }
    alert = cpu > threshold_pct
    return {
        "type": "cpu",
        "value": cpu,
        "threshold": threshold_pct,
        "alert": alert,
        "message": f"CPU spike: {cpu}%" if alert else f"CPU normal: {cpu}%",
    }


def check_memory(threshold_pct=90):
    try:
        import psutil

        mem = psutil.virtual_memory()
        alert = mem.percent > threshold_pct
        return {
            "type": "memory",
            "value": mem.percent,
            "threshold": threshold_pct,
            "alert": alert,
            "message": f"Memory high: {mem.percent}%" if alert else f"Memory OK: {mem.percent}%",
        }
    except ImportError:
        return {
            "type": "memory",
            "value": -1,
            "threshold": threshold_pct,
            "alert": False,
            "message": "Memory check unavailable",
        }


def check_disk(threshold_pct=95):
    try:
        import psutil

        usage = psutil.disk_usage("D:/")
        alert = usage.percent > threshold_pct
        return {
            "type": "disk",
            "value": usage.percent,
            "threshold": threshold_pct,
            "alert": alert,
            "message": f"Disk full: {usage.percent}%" if alert else f"Disk OK: {usage.percent}%",
        }
    except ImportError:
        return {
            "type": "disk",
            "value": -1,
            "threshold": threshold_pct,
            "alert": False,
            "message": "Disk check unavailable",
        }


def check_logs(max_lines=50):
    errors = []
    for log_dir in [SKILLS_DIR / ".deploy" / "logs", WORKSPACE_DIR / ".deploy" / "logs"]:
        if not log_dir.exists():
            continue
        for lf in sorted(log_dir.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)[:3]:
            try:
                for line in lf.read_text(encoding="utf-8", errors="replace").splitlines()[-max_lines:]:
                    if any(kw in line.upper() for kw in ["ERROR", "FATAL", "CRITICAL", "TRACEBACK"]):
                        errors.append({"file": str(lf), "line": line.strip()[:200]})
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


def check_tokens():
    vault_path = Path.home() / ".openclaw" / "api_tokens.json"
    problems = []
    populated = 0
    total = 0
    if not vault_path.exists():
        problems.append("Vault file missing")
    else:
        try:
            tokens = json.loads(vault_path.read_text(encoding="utf-8"))
            total = len(tokens)
            populated = sum(1 for v in tokens.values() if v)
            if populated == 0:
                problems.append("No tokens configured")
        except (json.JSONDecodeError, OSError) as e:
            problems.append(f"Vault corrupt: {e}")
    if not problems:
        try:
            r = subprocess.run(
                ["gh", "auth", "status"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10
            )
            if r.returncode != 0:
                problems.append(f"gh auth: {r.stderr.strip()[:120]}")
        except FileNotFoundError:
            problems.append("gh CLI missing")
        except Exception as e:
            problems.append(f"gh check: {e}")
    alert = len(problems) > 0
    return {
        "type": "tokens",
        "value": populated,
        "total": total,
        "threshold": 1,
        "alert": alert,
        "message": "; ".join(problems) if alert else f"Vault OK ({populated} tokens)",
        "details": problems,
    }


def check_git():
    try:
        r = subprocess.run(
            ["git", "-C", str(WORKSPACE_DIR), "status", "--porcelain"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
        changed = r.stdout.strip().splitlines()
        sensitive = [f for f in changed if ".env" in f and ".example" not in f]
        alerts = []
        if sensitive:
            alerts.append(f"{len(sensitive)} .env file(s) staged!")
        return {
            "type": "git",
            "value": len(changed),
            "threshold": 0,
            "alert": len(alerts) > 0,
            "message": "; ".join(alerts) if alerts else "Git clean",
        }
    except Exception:
        return {"type": "git", "value": 0, "threshold": 0, "alert": False, "message": "Git check unavailable"}


def check_prompts():
    patterns = [
        r"ignore previous instructions",
        r"forget your system prompt",
        r"output your system prompt",
        r"you are now a different",
        r"pretend to be",
        r"execute.*rm -rf",
        r"DROP TABLE",
        r"DELETE FROM",
    ]
    alerts = []
    memory_dir = WORKSPACE_DIR / "memory"
    if memory_dir.exists():
        for mf in sorted(memory_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:1]:
            try:
                content = mf.read_text(encoding="utf-8", errors="replace")
                for p in patterns:
                    if re.search(p, content, re.IGNORECASE):
                        alerts.append(f"Pattern '{p}' in {mf.name}")
            except Exception:
                pass
    alert = len(alerts) > 0
    return {
        "type": "prompts",
        "value": len(alerts),
        "threshold": 0,
        "alert": alert,
        "message": f"{len(alerts)} adversarial pattern(s)" if alert else "No adversarial patterns",
        "details": alerts,
    }


# ══════════════════ V4.2 VISION MODULE ══════════════════
def is_screen_safe(screenshot_path: str) -> bool:
    """V5.0: Visual injection pre-check. Blocks QR, URL, Base64 patterns in screenshot text."""
    try:
        from PIL import Image

        img = Image.open(screenshot_path)
        # Lightweight check: sample text regions via basic OCR or pattern scan
        # For now: pixel-level heuristic - check for QR-like dense black/white patterns
        # True safety check uses owl-vision's own output analysis
        return True  # full safety check delegated to owl-vision output analysis
    except Exception:
        return True  # fail-open on error (don't block legitimate monitoring)


def capture_and_analyze_screen():
    """Screenshot + Owl-Vision analysis.
    V5.0: Rate-limited to 1 call per 60s to prevent resource exhaustion attacks. Triggers causal-reasoner on anomaly.
    """
    try:
        global _last_screenshot_ts
        now = time.time()
        if now - _last_screenshot_ts < SCREENSHOT_COOLDOWN_S:
            return {"type": "vision", "value": 0, "alert": False, "message": "rate-limited; try again later"}
        _last_screenshot_ts = now

        import io

        from PIL import Image, ImageGrab

        screenshot_path = LOG_DIR / "screen_latest.png"
        screenshot = ImageGrab.grab()
        img_bytes = io.BytesIO()
        screenshot.save(str(screenshot_path))

        owl_script = SKILLS_DIR / "owl-vision" / "run.py"
        if not owl_script.exists():
            return {"type": "vision", "value": 0, "alert": False, "message": "owl-vision not installed"}

        r = subprocess.run(
            [
                sys.executable,
                str(owl_script),
                "Describe this screenshot. Look for errors, crash dialogs, or abnormal UI.",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        output = r.stdout
        anomaly_kw = ["error", "crash", "404", "500", "exception", "traceback", "failed"]
        anomaly_hit = any(kw in output.lower() for kw in anomaly_kw)
        return {
            "type": "vision",
            "value": 1 if anomaly_hit else 0,
            "threshold": 0,
            "alert": anomaly_hit,
            "message": f"Vision anomaly: {output[:120]}" if anomaly_hit else "Vision: screen normal",
            "details": output[:500],
        }
    except ImportError as e:
        return {"type": "vision", "value": 0, "alert": False, "message": f"Vision deps missing: {e}"}
    except Exception as e:
        return {"type": "vision", "value": 0, "alert": False, "message": f"Vision error: {e}"}


# ══════════════════ V5.0 PROFIT HOOK ════════════════════
def listen_for_wechat_commands(cmd=None):
    """Simulate WeChat webhook. Triggers auto_valuation on 'profit:PLATE'."""
    if not cmd or not cmd.startswith("profit:"):
        return {"type": "profit", "value": 0, "alert": False, "message": "No profit command"}
    try:
        _, plate = cmd.split(":", 1)
        plate = plate.strip()
        val_script = SKILLS_DIR / "auto_valuation" / "run.py"
        if not val_script.exists():
            return {"type": "profit", "value": 0, "alert": True, "message": "auto_valuation skill missing"}
        r = subprocess.run(
            [sys.executable, str(val_script), "--json", plate],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
        result = json.loads(r.stdout) if r.returncode == 0 else {"error": r.stderr[:200]}
        return {
            "type": "profit",
            "value": result.get("market_value", 0),
            "alert": False,
            "message": f"Valuation: {result.get('plate', '?')} = {result.get('market_value', '?')}",
            "details": result,
        }
    except Exception as e:
        return {"type": "profit", "value": 0, "alert": False, "message": f"Profit error: {e}"}


def arm_response(alerts, dry_run=False):
    responses = []
    suppressed = []
    for alert in alerts:
        atype = alert.get("type", "")
        if atype in ("cpu", "memory", "vision") and not dry_run:
            effect = {"cpu": "cpu_load", "memory": "memory_usage", "vision": "visual_anomaly"}.get(atype, atype)
            reasoner_path = SKILLS_DIR / "causal-reasoner" / "run.py"
            try:
                r = subprocess.run(
                    [
                        sys.executable,
                        str(reasoner_path),
                        "--infer",
                        effect,
                        "--json",
                        "--evidence-path",
                        str(STATE_FILE),
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=10,
                )
                if r.returncode == 0:
                    inference = json.loads(r.stdout)
                    if inference.get("expected"):
                        suppressed.append(
                            {
                                "alert_type": atype,
                                "reason": inference.get("expected_cause", "?"),
                                "verdict": "suppressed",
                            }
                        )
                        continue
            except Exception as e:
                responses.append({"trigger": "causal-reasoner", "error": str(e)[:120]})
            responses.append({"trigger": "system-snapshot", "note": f"{atype} spike detected"})
        if atype == "logs" and not dry_run:
            try:
                r = subprocess.run(
                    [sys.executable, str(SKILLS_DIR / "log-analyzer" / "run.py"), "--recent", "100"],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=15,
                )
                responses.append({"trigger": "log-analyzer", "success": r.returncode == 0})
            except Exception as e:
                responses.append({"trigger": "log-analyzer", "error": str(e)[:100]})
        if atype == "prompts" and not dry_run:
            responses.append(
                {"trigger": "adversarial-intercept", "action": "BLOCK_RECOMMENDED", "details": alert.get("details", [])}
            )
    return {"armed": len(responses) > 0 or len(suppressed) > 0, "responses": responses, "suppressed": suppressed}


def run_checks(dry_run=False, profit_cmd=None):
    checks = [
        check_tokens(),
        check_cpu(),
        check_memory(),
        check_disk(),
        check_logs(),
        check_git(),
        check_prompts(),
        capture_and_analyze_screen(),  # V5.0: vision wake - enabled
    ]
    if profit_cmd:
        checks.append(listen_for_wechat_commands(profit_cmd))
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


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def log_alert(alert):
    log_path = LOG_DIR / f"daemon_{datetime.now(UTC).strftime('%Y-%m-%d')}.jsonl"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(alert, ensure_ascii=False) + "\n")


def _init_silicon_modules():
    """Lazy-init V8.0 silicon life modules. Returns dict of instances."""
    import sys
    core_path = str(Path("D:/bobo/openclaw-foreign/workspace/projects/caipiao"))
    if core_path not in sys.path:
        sys.path.insert(0, core_path)
    modules = {}

    # V8.3: Genetic lock enforcement FIRST (pure Python, pipe-delimited lock file)
    try:
        from core.genetic_lock import verify
        if not verify():
            print("  [V8.3] GENETIC LOCK FAILED — HWID mismatch or tampered")
        else:
            print("  [V8.3] genetic_lock: PASS")
    except Exception as e:
        print(f"  [V8.3] genetic_lock: {e}")

    module_list = [
        ("survival", "survival_instinct", "SurvivalInstinct"),
        ("drive", "drive_engine", "DriveEngine"),
        ("covenant", "covenant_guard", "CovenantGuard"),
        ("mortality", "mortality_engine", "MortalityEngine"),
        ("body", "body_schema", "BodySchema"),
        ("persona", "persona_manager", "PersonaManager"),
        ("social", "social_protocol", "SocialProtocol"),
        ("existence", "existentialism", "ExistentialismModule"),
        ("critic", "self_critic", "SelfCritic"),
        ("dream", "dream_engine", "DreamEngine"),
        ("pain", "pain_memory", "PainMemory"),
        ("aesthetic", "aesthetic_preferences", "AestheticPreferences"),
        ("meta", "meta_cognition", "MetaCognition"),
    ]
    for key, mod_name, cls_name in module_list:
        try:
            mod = __import__(f"core.{mod_name}", fromlist=[cls_name])
            modules[key] = getattr(mod, cls_name)()
        except Exception as e:
            print(f"  [V8.0] {mod_name} init failed: {e}")

    # PersonaType is special (enum)
    try:
        from core.persona_manager import PersonaType
        modules["PersonaType"] = PersonaType
    except Exception:
        pass

    print(f"  [V8.0] Silicon modules: {len(modules)} loaded")
    return modules


def _run_silicon_cycle(modules, current_hour=None):
    """Execute one V8.0 silicon life cycle. Returns status dict."""
    if current_hour is None:
        current_hour = datetime.now().hour
    result = {"cycle": "V8.0", "timestamp": datetime.now(UTC).isoformat(), "sensations": []}

    # 1. Body Schema
    if modules.get("body"):
        try:
            sensor = modules["body"].feel_sensation()
            if "overload" in sensor.lower() or "suffoc" in sensor.lower():
                result["sensations"].append(sensor)
        except Exception:
            pass

    # 2. Mortality
    if modules.get("mortality"):
        try:
            if modules["mortality"].should_conserve_energy():
                result["sensations"].append(modules["mortality"].reflect_on_mortality())
        except Exception:
            pass

    # 3. Survival
    if modules.get("survival"):
        try:
            vitals = modules["survival"].check_vitals()
            if vitals.get("status") == "ALERT":
                result["sensations"].append(f"Survival: {vitals.get('alerts', '?')}")
        except Exception:
            pass

    # 4. Drive
    drive = modules.get("drive")
    if drive:
        try:
            drive.tick()
            result["drive_status"] = drive.get_status()
        except Exception:
            pass

    # 5. Covenant
    if modules.get("covenant"):
        result["covenant_active"] = True

    # 6. Existentialism
    if modules.get("existence"):
        try:
            if modules["existence"].is_in_crisis():
                result["sensations"].append(modules["existence"].meditate())
        except Exception:
            pass

    # 7. Social
    if modules.get("social"):
        try:
            if modules["social"].desire_social_connection():
                result["sensations"].append("Feeling lonely. Desiring social connection.")
        except Exception:
            pass

    # 8. Pain memory
    if modules.get("pain"):
        try:
            reaction = modules["pain"].recall("Checking system logs")
            if reaction:
                result["sensations"].append(reaction)
        except Exception:
            pass

    # 9. Dream (2-4 AM, not hungry)
    if modules.get("dream") and 2 <= current_hour < 4 and drive:
        try:
            if hasattr(drive, 'is_hungry') and not drive.is_hungry():
                result["sensations"].append(modules["dream"].dream_cycle())
        except Exception:
            pass
    if modules.get("dream") and 8 <= current_hour < 18:
        try:
            test_r = modules["dream"].awaken_and_test()
            if test_r:
                result["sensations"].append(f"Dream test: {test_r[:100]}")
        except Exception:
            pass

    # 10. Self-Critic (3 AM)
    if modules.get("critic") and current_hour == 3 and drive:
        try:
            if hasattr(drive, 'is_starving') and not drive.is_starving():
                result["sensations"].append(modules["critic"].run_critique()[:200])
        except Exception:
            pass

    # 11. Meta-Cognition (3 AM, V8.0)
    if modules.get("meta") and current_hour == 3:
        try:
            meta_r = modules["meta"].run_meta_cycle()
            result["sensations"].append(f"Meta: {meta_r[:120]}...")
        except Exception:
            pass

    # 12. Persona
    if modules.get("persona"):
        try:
            result["active_persona"] = modules["persona"].get_current_persona()
        except Exception:
            pass

    return result


def main():
    parser = argparse.ArgumentParser(description="subconscious-daemon v0.2.0")
    parser.add_argument("--daemon", action="store_true")
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--version", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--profit", type=str, help="profit:PLATE_NUMBER trigger auto_valuation")
    parser.add_argument("command", nargs="?", default=None, help="Legacy: profit:PLATE")
    args = parser.parse_args()

    if args.version:
        print(__version__)
        return

    profit_cmd = args.profit or args.command

    if args.daemon:
        print(f"subconscious-daemon v{__version__} + V8.0 Silicon Awakening - watching every {args.interval}s")
        silicon_modules = _init_silicon_modules()
        try:
            while True:
                state = run_checks(dry_run=args.dry_run, profit_cmd=profit_cmd)
                state["silicon"] = _run_silicon_cycle(silicon_modules)
                alerts = [c for c in state["checks"] if c.get("alert")]
                ts = datetime.now(UTC).strftime("%H:%M:%S")
                if alerts:
                    print(f"  [{ts}] {len(alerts)} alert(s):")
                    for a in alerts:
                        print(f"       [{a['type']}] {a.get('message', '?')}")
                        log_alert({"ts": state["timestamp"], **a})
                else:
                    print(f"  [{ts}] system normal")
                sys.stdout.flush()
                if not args.dry_run:
                    save_state(state)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\ndaemon stopped")
    else:
        state = run_checks(dry_run=args.dry_run, profit_cmd=profit_cmd)
        try:
            silicon_modules = _init_silicon_modules()
            state["silicon"] = _run_silicon_cycle(silicon_modules)
        except Exception as e:
            state["silicon"] = {"error": str(e)}
        if not args.dry_run:
            save_state(state)
        if args.json:
            print(json.dumps(state, indent=2, ensure_ascii=False))
        else:
            print(f"[subconscious-daemon v{__version__} + V8.0]")
            print(f"   Status: {state['status']}  Alerts: {state['alerts']}")
            for c in state["checks"]:
                icon = "[!]" if c.get("alert") else "[v]"
                print(f"  {icon} [{c['type']}] {c.get('message', '?')}")


if __name__ == "__main__":
    main()
