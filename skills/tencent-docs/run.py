#!/usr/bin/env python3
"""
tencent-docs v0.2.0 — 腾讯文档 API 集成
===========================================
创建/查询/列表 在线文档、表格、幻灯片。
API: https://docs.qq.com/openapi/v2

Authentication: TENCENT_DOCS_TOKEN env var

Usage:
  python run.py create --title <title> --type doc|sheet|slide
  python run.py list
  python run.py get --docid <id>
  python run.py --version
  python run.py --json --dry-run create --title "Test" --type doc
"""
import argparse
import json
import logging
import os
import sys
import time
import traceback
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

VERSION = "0.2.0"
SKILL_NAME = "tencent-docs"
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SKILL_DIR, ".deploy", "logs")
TZ = timezone(timedelta(hours=8))
API_BASE = "https://docs.qq.com/openapi/v2"


def load_creds():
    for env_key in ["TENCENT_DOCS_TOKEN", "WECOM_CORPSECRET"]:
        val = os.environ.get(env_key, "")
        if val:
            return val
    return ""


def setup_logging(verbose=False):
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger(SKILL_NAME)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.handlers.clear()
    fh = logging.FileHandler(
        os.path.join(LOG_DIR, f"{datetime.now(TZ).strftime('%Y-%m-%d')}.jsonl"),
        encoding="utf-8",
    )
    fh.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(fh)
    return logger


def log_event(logger, event, level="INFO", **kwargs):
    payload = {
        "timestamp": datetime.now(TZ).isoformat(),
        "skill": SKILL_NAME,
        "event": event,
        "pid": os.getpid(),
        **kwargs,
    }
    getattr(logger, level.lower(), logger.info)(json.dumps(payload, ensure_ascii=False, default=str))


def safe_run(logger, fn, *a, **kw):
    start = time.time()
    try:
        r = fn(*a, **kw)
        log_event(logger, "task_completed", duration_ms=round((time.time() - start) * 1000, 1), result=str(r)[:500])
        return r
    except Exception as e:
        log_event(logger, "task_failed", level="ERROR", duration_ms=round((time.time() - start) * 1000, 1), error=str(e))
        return {"ok": False, "error": str(e)}


def api_call(endpoint, method="GET", body=None):
    token = load_creds()
    if not token:
        return {
            "ok": False,
            "errcode": -2,
            "errmsg": "TENCENT_DOCS_TOKEN not set. Set env var or configure OAuth.",
        }
    url = f"{API_BASE}{endpoint}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data_bytes = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return {"ok": True, "data": json.loads(resp.read().decode("utf-8"))}
    except urllib.error.HTTPError as e:
        return {"ok": False, "errcode": e.code, "errmsg": e.read().decode("utf-8")[:500]}
    except Exception as e:
        return {"ok": False, "errcode": -1, "errmsg": str(e)}


def create_doc(title, doc_type, logger=None):
    type_map = {"doc": "word", "sheet": "excel", "slide": "ppt"}
    return api_call("/files", method="POST", body={"title": title, "type": type_map.get(doc_type, "word")})


def list_docs(logger=None):
    return api_call("/files")


def get_doc(docid, logger=None):
    return api_call(f"/files/{docid}")


def main():
    parser = argparse.ArgumentParser(description=f"tencent-docs v{VERSION} — 腾讯文档 API")
    sub = parser.add_subparsers(dest="action", help="Action")

    # create
    cp = sub.add_parser("create", help="Create a document")
    cp.add_argument("--title", required=True, help="Document title")
    cp.add_argument("--type", required=True, choices=["doc", "sheet", "slide"], help="Document type")

    # list
    sub.add_parser("list", help="List documents")

    # get
    gp = sub.add_parser("get", help="Get a document")
    gp.add_argument("--docid", required=True, help="Document ID")

    # Global flags
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--dry-run", action="store_true", help="Preview without API call")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    if args.version:
        print(json.dumps({"skill": SKILL_NAME, "version": VERSION, "status": "live"}, indent=2))
        return

    if args.json and not args.action:
        info = {
            "skill": SKILL_NAME,
            "version": VERSION,
            "status": "live",
            "features": ["create", "list", "get"],
            "requires": ["TENCENT_DOCS_TOKEN (env var)"],
            "api": "https://docs.qq.com/openapi/v2",
        }
        print(json.dumps(info, indent=2))
        return

    if not args.action:
        parser.print_help()
        return

    if args.dry_run:
        dry_result = {"action": args.action, "dry_run": True, "token_available": bool(load_creds())}
        if args.action == "create":
            dry_result["title"] = args.title
            dry_result["type"] = args.type
        elif args.action == "get":
            dry_result["docid"] = args.docid
        dry_result["note"] = "Dry run — no API call made. Remove --dry-run to execute."
        print(json.dumps(dry_result, indent=2))
        return

    logger = setup_logging(args.verbose)
    log_event(logger, "skill_invoked", action=args.action)

    exit_code = 0
    try:
        if args.action == "create":
            result = safe_run(logger, create_doc, args.title, args.type, logger)
        elif args.action == "list":
            result = safe_run(logger, list_docs, logger)
        elif args.action == "get":
            result = safe_run(logger, get_doc, args.docid, logger)
        else:
            result = {"ok": False, "error": f"Unknown action: {args.action}"}

        print(json.dumps(result, indent=2, ensure_ascii=False))

        if not result.get("ok") and result.get("errcode") != -2:
            exit_code = 1

    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, indent=2))
        traceback.print_exc(file=sys.stderr)
        exit_code = 2
    finally:
        log_event(logger, "skill_ended", exit_code=exit_code)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
