#!/usr/bin/env python3
"""
linear v0.2.0 — Linear API Integration
=========================================
Issue/Project/Cycle management via Linear GraphQL API.

Authentication: LINEAR_API_KEY env var or skills/linear/linear_config.json

Usage:
  python run.py issues [--team <key>] [--assignee <id>]
  python run.py create --title <t> --team <key>
  python run.py projects [--team <key>]
  python run.py --version
  python run.py --json --dry-run issues --team ENG
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
SKILL_NAME = "linear"
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SKILL_DIR, ".deploy", "logs")
TZ = timezone(timedelta(hours=8))
API_BASE = "https://api.linear.app/graphql"


def load_token():
    token = os.environ.get("LINEAR_API_KEY", "")
    if not token:
        config_path = os.path.join(SKILL_DIR, "linear_config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                token = json.load(f).get("token", "")
    return token


def setup_logging(verbose=False):
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger(SKILL_NAME)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.handlers.clear()
    log_file = os.path.join(LOG_DIR, f"{datetime.now(TZ).strftime('%Y-%m-%d')}.jsonl")
    fh = logging.FileHandler(log_file, encoding="utf-8")
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


def graphql(query, variables=None):
    token = load_token()
    if not token:
        return {
            "ok": False,
            "errcode": -2,
            "errmsg": "LINEAR_API_KEY not set. Create at https://linear.app/settings/api",
        }
    body = {"query": query}
    if variables:
        body["variables"] = variables
    req = urllib.request.Request(
        API_BASE,
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": token, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return {"ok": True, "data": json.loads(resp.read().decode("utf-8"))}
    except urllib.error.HTTPError as e:
        return {"ok": False, "errcode": e.code, "errmsg": e.read().decode("utf-8")[:500]}
    except Exception as e:
        return {"ok": False, "errcode": -1, "errmsg": str(e)}


def list_issues(team_key="", assignee="", logger=None):
    q = """query Issues($teamKey: String, $assigneeId: String) {
      issues(first: 25, filter: {team: {key: {eq: $teamKey}}, assignee: {id: {eq: $assigneeId}}}) {
        nodes { id title state { name } assignee { name } priority }
      }
    }"""
    vars_dict = {}
    if team_key:
        vars_dict["teamKey"] = team_key
    if assignee:
        vars_dict["assigneeId"] = assignee
    return graphql(q, vars_dict)


def create_issue(title, team_key, logger=None):
    q = """mutation CreateIssue($title: String!, $teamKey: String!) {
      issueCreate(input: {title: $title, teamId: $teamKey}) {
        issue { id title url }
      }
    }"""
    return graphql(q, {"title": title, "teamKey": team_key})


def list_projects(team_key="", logger=None):
    q = """query Projects($teamKey: String) {
      projects(filter: {team: {key: {eq: $teamKey}}}) { nodes { id name state } }
    }"""
    return graphql(q, {"teamKey": team_key})


def main():
    parser = argparse.ArgumentParser(description=f"linear v{VERSION} — Linear API Integration")
    sub = parser.add_subparsers(dest="action", help="Action")

    # issues
    ip = sub.add_parser("issues", help="List issues")
    ip.add_argument("--team", help="Team key (e.g. ENG)")
    ip.add_argument("--assignee", help="Assignee ID")

    # create
    cp = sub.add_parser("create", help="Create an issue")
    cp.add_argument("--title", required=True, help="Issue title")
    cp.add_argument("--team", required=True, help="Team key (e.g. ENG)")

    # projects
    pp = sub.add_parser("projects", help="List projects")
    pp.add_argument("--team", help="Team key (e.g. ENG)")

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
            "features": ["issues", "create", "projects"],
            "requires": ["LINEAR_API_KEY (env var or linear_config.json)"],
            "api": "https://api.linear.app/graphql",
        }
        print(json.dumps(info, indent=2))
        return

    # No action
    if not args.action:
        parser.print_help()
        return

    # --dry-run
    if args.dry_run:
        dry_result = {
            "action": args.action,
            "dry_run": True,
            "token_available": bool(load_token()),
        }
        if args.action == "issues":
            dry_result["team"] = args.team
            dry_result["assignee"] = args.assignee
        elif args.action == "create":
            dry_result["title"] = args.title
            dry_result["team"] = args.team
        elif args.action == "projects":
            dry_result["team"] = args.team
        dry_result["note"] = "Dry run — no API call made. Remove --dry-run to execute."
        print(json.dumps(dry_result, indent=2))
        return

    # Real execution
    logger = setup_logging(args.verbose)
    log_event(logger, "skill_invoked", action=args.action)

    exit_code = 0
    try:
        if args.action == "issues":
            result = safe_run(logger, list_issues, args.team or "", args.assignee or "", logger)
        elif args.action == "create":
            result = safe_run(logger, create_issue, args.title, args.team, logger)
        elif args.action == "projects":
            result = safe_run(logger, list_projects, args.team or "", logger)
        else:
            result = {"ok": False, "error": f"Unknown action: {args.action}"}

        output = json.dumps(result, indent=2, ensure_ascii=False)
        print(output)

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
