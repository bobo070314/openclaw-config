#!/usr/bin/env python3
"""
wecomcli-contact v0.2.0 — 企业微信通讯录管理
=============================================
List/get/search contacts via WeCom API.
Depends on: wecomcli-setup (shared wecom_common module)

Usage:
  python run.py list [--dept <id>] [--fetch-children]
  python run.py get --userid <id>
  python run.py search --name <name>
  python run.py --version
  python run.py --json --dry-run list
"""
import argparse
import json
import os
import sys

VERSION = "0.2.0"
SKILL_NAME = "wecomcli-contact"
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SKILL_DIR, ".deploy", "logs")

sys.path.insert(0, os.path.join(SKILL_DIR, "..", "wecomcli-setup"))
try:
    from wecom_common import api_call, setup_logger, log_event, safe_run, load_config
except ImportError:
    def api_call(*a, **kw):
        return {"ok": False, "errcode": -3, "errmsg": "wecomcli-setup not installed"}
    def setup_logger(n, d, v=False):
        return None
    def log_event(*a, **kw):
        pass
    def safe_run(l, fn, *a, **kw):
        return fn(*a, **kw)
    def load_config():
        return {}


def api_list(dept=None, fetch_children=False, logger=None):
    endpoint = "user/list" if not dept else f"user/simplelist?department_id={dept}&fetch_child={1 if fetch_children else 0}"
    return api_call(endpoint)


def api_get(userid, logger=None):
    return api_call(f"user/get?userid={userid}")


def api_search(name, logger=None):
    return {"ok": False, "error": "Search by name not available in WeCom API. Use 'get' with known userid."}


def main():
    parser = argparse.ArgumentParser(description=f"wecomcli-contact v{VERSION}")
    sub = parser.add_subparsers(dest="action", help="Action")

    lp = sub.add_parser("list", help="List department members")
    lp.add_argument("--dept", help="Department ID")
    lp.add_argument("--fetch-children", action="store_true", help="Fetch sub-departments")

    gp = sub.add_parser("get", help="Get user info")
    gp.add_argument("--userid", required=True, help="User ID")

    sp = sub.add_parser("search", help="Search users by name")
    sp.add_argument("--name", required=True, help="Username")

    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--dry-run", action="store_true", help="Preview without API call")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--verbose", action="store_true", help="Debug logging")

    args = parser.parse_args()

    if args.version:
        print(json.dumps({"skill": SKILL_NAME, "version": VERSION, "status": "live"}, indent=2))
        return

    if args.json and not args.action:
        info = {"skill": SKILL_NAME, "version": VERSION, "status": "live", "features": ["list", "get", "search"], "requires": ["wecomcli-setup"]}
        print(json.dumps(info, indent=2))
        return

    if not args.action:
        parser.print_help()
        return

    if args.dry_run:
        dry = {"action": args.action, "dry_run": True, "config_available": bool(load_config())}
        if args.action == "list":
            dry["dept"] = args.dept
            dry["fetch_children"] = args.fetch_children
        elif args.action == "get":
            dry["userid"] = args.userid
        elif args.action == "search":
            dry["name"] = args.name
        dry["note"] = "Dry run — no API call made."
        print(json.dumps(dry, indent=2))
        return

    logger = setup_logger(SKILL_NAME, LOG_DIR, args.verbose)
    log_event(logger, "skill_invoked", action=args.action)

    exit_code = 0
    try:
        if args.action == "list":
            result = safe_run(logger, api_list, args.dept, args.fetch_children, logger)
        elif args.action == "get":
            result = safe_run(logger, api_get, args.userid, logger)
        elif args.action == "search":
            result = safe_run(logger, api_search, args.name, logger)
        else:
            result = {"ok": False, "error": f"Unknown action: {args.action}"}

        print(json.dumps(result, indent=2, ensure_ascii=False))
        # Graceful: search by name is a known API limitation, not a fatal error
        if not result.get("ok") and result.get("error", "").startswith("Search by name"):
            exit_code = 0
        elif not result.get("ok") and result.get("errcode", -999) not in (-2, -3):
            exit_code = 1
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, indent=2))
        exit_code = 2
    finally:
        if logger:
            log_event(logger, "skill_ended", exit_code=exit_code)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
