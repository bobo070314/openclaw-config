#!/usr/bin/env python3
"""
notion v0.2.0 — Notion API Integration
=========================================
Page create/query/update, database query, search.
Uses Notion API v1 (https://api.notion.com/v1).

Authentication: NOTION_TOKEN env var or skills/notion/notion_config.json

Usage:
  python run.py query --database-id <id> [--filter '<json>']
  python run.py page --id <page_id>
  python run.py create --parent-id <id> --title <title> [--content <text>]
  python run.py search --query <text>
  python run.py --version
  python run.py --json --dry-run query --database-id <id>
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
SKILL_NAME = "notion"
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SKILL_DIR, ".deploy", "logs")
TZ = timezone(timedelta(hours=8))
NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


def load_token():
    """Load Notion token from env or config file."""
    token = os.environ.get("NOTION_TOKEN", "")
    if token:
        return token
    config_paths = [
        os.path.join(SKILL_DIR, "notion_config.json"),
        os.path.expanduser("~/.notion/config.json"),
    ]
    for p in config_paths:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f).get("token", "")
            except Exception:
                pass
    return ""


def setup_logging(verbose=False):
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger(SKILL_NAME)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.handlers.clear()
    log_file = os.path.join(LOG_DIR, f"{datetime.now(TZ).strftime('%Y-%m-%d')}.jsonl")
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S"))
    logger.addHandler(ch)
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


def notion_api(endpoint, method="GET", body=None, token=None):
    """Call Notion API. Returns {ok, data|errcode, errmsg}."""
    if token is None:
        token = load_token()
    if not token:
        return {
            "ok": False,
            "errcode": -2,
            "errmsg": "NOTION_TOKEN not set. Create integration at https://www.notion.so/my-integrations",
        }
    url = f"{NOTION_API}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    data_bytes = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return {"ok": True, "data": json.loads(resp.read().decode("utf-8"))}
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8")[:500]
        return {"ok": False, "errcode": e.code, "errmsg": msg}
    except Exception as e:
        return {"ok": False, "errcode": -1, "errmsg": str(e)}


def safe_run(logger, fn, *a, **kw):
    """Run a function with logging and error handling."""
    start = time.time()
    try:
        r = fn(*a, **kw)
        elapsed = round((time.time() - start) * 1000, 1)
        log_event(logger, "task_completed", duration_ms=elapsed, result=str(r)[:500])
        return r
    except Exception as e:
        elapsed = round((time.time() - start) * 1000, 1)
        log_event(
            logger, "task_failed", level="ERROR",
            duration_ms=elapsed, error=str(e),
            traceback=traceback.format_exc()[:2000],
        )
        print(f"[{SKILL_NAME}] ERROR: {e}", file=sys.stderr)
        return {"ok": False, "error": str(e)}


def query_database(database_id, filter_json=None, logger=None):
    body = {}
    if filter_json:
        body["filter"] = json.loads(filter_json)
    return notion_api(f"/databases/{database_id}/query", method="POST", body=body)


def get_page(page_id, logger=None):
    return notion_api(f"/pages/{page_id}")


def create_page(parent_id, title, content="", logger=None):
    body = {
        "parent": {"page_id": parent_id},
        "properties": {"title": {"title": [{"text": {"content": title}}]}},
    }
    if content:
        body["children"] = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]},
            }
        ]
    return notion_api("/pages", method="POST", body=body)


def search(q, logger=None):
    return notion_api("/search", method="POST", body={"query": q})


def main():
    parser = argparse.ArgumentParser(description=f"notion v{VERSION} — Notion API Integration")
    sub = parser.add_subparsers(dest="action", help="Action")

    # query
    qp = sub.add_parser("query", help="Query a database")
    qp.add_argument("--database-id", required=True, help="Notion database ID")
    qp.add_argument("--filter", help="Filter as JSON string")

    # page
    pp = sub.add_parser("page", help="Get a page")
    pp.add_argument("--id", required=True, dest="page_id", help="Notion page ID")

    # create
    cp = sub.add_parser("create", help="Create a page")
    cp.add_argument("--parent-id", required=True, help="Parent page ID")
    cp.add_argument("--title", required=True, help="Page title")
    cp.add_argument("--content", help="Page content (markdown-ish)")

    # search
    sp = sub.add_parser("search", help="Search Notion workspace")
    sp.add_argument("--query", required=True, help="Search query")

    # Global flags
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--dry-run", action="store_true", help="Preview without API call")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    # --version
    if args.version:
        print(json.dumps({"skill": SKILL_NAME, "version": VERSION, "status": "live"}, indent=2))
        return

    # --json without action
    if args.json and not args.action:
        info = {
            "skill": SKILL_NAME,
            "version": VERSION,
            "status": "live",
            "features": ["query", "page", "create", "search"],
            "requires": ["NOTION_TOKEN (env var or notion_config.json)"],
            "api": "https://api.notion.com/v1",
        }
        print(json.dumps(info, indent=2))
        return

    # No action
    if not args.action:
        parser.print_help()
        return

    # --dry-run: return JSON preview without API call
    if args.dry_run:
        dry_result = {
            "action": args.action,
            "dry_run": True,
            "token_available": bool(load_token()),
        }
        if args.action == "query":
            dry_result["database_id"] = args.database_id
            dry_result["filter"] = args.filter
        elif args.action == "page":
            dry_result["page_id"] = args.page_id
        elif args.action == "create":
            dry_result["parent_id"] = args.parent_id
            dry_result["title"] = args.title
            dry_result["content"] = args.content or ""
        elif args.action == "search":
            dry_result["query"] = args.query

        dry_result["note"] = "Dry run — no API call made. Remove --dry-run to execute."
        print(json.dumps(dry_result, indent=2))
        return

    # Real execution
    logger = setup_logging(args.verbose)
    log_event(logger, "skill_invoked", action=args.action)

    exit_code = 0
    try:
        if args.action == "query":
            result = safe_run(logger, query_database, args.database_id, args.filter, logger)
        elif args.action == "page":
            result = safe_run(logger, get_page, args.page_id, logger)
        elif args.action == "create":
            result = safe_run(logger, create_page, args.parent_id, args.title, args.content or "", logger)
        elif args.action == "search":
            result = safe_run(logger, search, args.query, logger)
        else:
            result = {"ok": False, "error": f"Unknown action: {args.action}"}

        output = result if args.json else json.dumps(result, indent=2, ensure_ascii=False)
        print(output if isinstance(output, str) else json.dumps(output, indent=2, ensure_ascii=False))

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
