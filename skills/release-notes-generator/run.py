"""
release-notes-generator - 发布说明生成器

Description: 基于Git提交自动生成Release Notes，支持Conventional Commits解析和分类

Usage: python run.py [--from <tag>] [--to <tag>] [--format markdown|json] [--output <path>] [--verbose]
"""
import sys

# === V0.2.0 CLI STANDARD (auto-injected, do not remove) ===
VERSION = "0.2.0"
SKILL_NAME = "release-notes-generator"
import json
import sys as _sys

def _handle_std_flags():
    """Handle --version, --json, --dry-run before main logic."""
    _args = [a for a in _sys.argv[1:] if not a.startswith("-")]
    _flags = [a for a in _sys.argv[1:] if a.startswith("-")]

    if "--version" in _flags:
        print(json.dumps({"skill": SKILL_NAME, "version": VERSION, "status": "live"}, indent=2))
        _sys.exit(0)

    if "--json" in _flags and len(_args) == 0:
        print(json.dumps({"skill": SKILL_NAME, "version": VERSION, "status": "live"}, indent=2))
        _sys.exit(0)

    if "--dry-run" in _flags:
        dry = {"skill": SKILL_NAME, "version": VERSION, "dry_run": True, "note": "Dry run — skipping real execution."}
        print(json.dumps(dry, indent=2))
        _sys.exit(0)

    # Clean flags so original argv parsing doesn't break
    _sys.argv = [_sys.argv[0]] + _args

_handle_std_flags()
# === END CLI STANDARD ===

import os
import json
import logging
import time
import traceback
from datetime import datetime, timezone, timedelta

SKILL_NAME = "release-notes-generator"
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SKILL_DIR, ".deploy", "logs")
TZ = timezone(timedelta(hours=8))


def setup_logging(verbose=False):
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger(SKILL_NAME)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.handlers.clear()
    log_file = os.path.join(LOG_DIR, f"{datetime.now(TZ).strftime('%Y-%m-%d')}.jsonl")
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(fh)
    ch = logging.StreamHandler(sys.stderr)
    ch.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S"))
    logger.addHandler(ch)
    return logger


def log_event(logger, event, level="INFO", **kwargs):
    payload = {"timestamp": datetime.now(TZ).isoformat(), "skill": SKILL_NAME, "event": event, "pid": os.getpid(), **kwargs}
    getattr(logger, level.lower(), logger.info)(json.dumps(payload, ensure_ascii=False, default=str))


def safe_run(logger, fn, *a, **kw):
    start = time.time()
    try:
        r = fn(*a, **kw)
        log_event(logger, "task_completed", duration_ms=round((time.time()-start)*1000, 1), result=str(r)[:500])
        return r
    except Exception as e:
        log_event(logger, "task_failed", level="ERROR", duration_ms=round((time.time()-start)*1000, 1),
                  error=str(e), traceback=traceback.format_exc()[:2000])
        print(f"[{SKILL_NAME}] ERROR: {e}", file=sys.stderr)
        return None


def generate(from_tag, to_tag, fmt, output, logger):
    log_event(logger, "generate_started", from_tag=from_tag, to_tag=to_tag, format=fmt, output=output)
    # TODO: git log parsing + conventional commit classification
    notes = {"from": from_tag or "HEAD~10", "to": to_tag or "HEAD", "sections": {"features": [], "fixes": [], "chore": []}}
    log_event(logger, "generate_completed", commit_count=0)
    return notes


def main():
    logger = None
    exit_code = 0
    try:
        args = sys.argv[1:]
        kwargs = {"from_tag": None, "to_tag": None, "format": "markdown", "output": "RELEASE_NOTES.md", "verbose": False}
        i = 0
        while i < len(args):
            if args[i] == "--from" and i+1 < len(args):
                kwargs["from_tag"] = args[i+1]; i += 2
            elif args[i] == "--to" and i+1 < len(args):
                kwargs["to_tag"] = args[i+1]; i += 2
            elif args[i] == "--format" and i+1 < len(args):
                kwargs["format"] = args[i+1]; i += 2
            elif args[i] == "--output" and i+1 < len(args):
                kwargs["output"] = args[i+1]; i += 2
            elif args[i] == "--verbose":
                kwargs["verbose"] = True; i += 1
            else:
                i += 1
        logger = setup_logging(verbose=kwargs["verbose"])
        log_event(logger, "skill_invoked", args=sys.argv[1:])
        result = safe_run(logger, generate, kwargs["from_tag"], kwargs["to_tag"], kwargs["format"], kwargs["output"], logger)
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            exit_code = 1
    except Exception as e:
        print(f"[{SKILL_NAME}] FATAL: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        exit_code = 2
    finally:
        if logger:
            log_event(logger, "skill_ended", exit_code=exit_code)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
