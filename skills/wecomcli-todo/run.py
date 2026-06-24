#!/usr/bin/env python3
"""wecomcli-todo v0.2.0 — 企业微信待办管理"""
import argparse, json, os, sys

VERSION = "0.2.0"
SKILL_NAME = "wecomcli-todo"
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SKILL_DIR, ".deploy", "logs")

sys.path.insert(0, os.path.join(SKILL_DIR, "..", "wecomcli-setup"))
try:
    from wecom_common import api_call, setup_logger, log_event, safe_run, load_config
except ImportError:
    def api_call(*a, **kw): return {"ok": False, "errcode": -3, "errmsg": "wecomcli-setup not installed"}
    def setup_logger(n, d, v=False): return None
    def log_event(*a, **kw): pass
    def safe_run(l, fn, *a, **kw): return fn(*a, **kw)
    def load_config(): return {}

def api_add(title, priority="", due="", assign="", logger=None):
    body = {"todo_title": title}
    if priority: body["priority"] = int(priority)
    if due: body["due_date"] = due
    if assign: body["assignee"] = assign
    return api_call("oa/todo/add", method="POST", body=body)

def api_done(todoid, logger=None):
    return api_call("oa/todo/done", method="POST", body={"todoid": todoid})

def api_list(status="", logger=None):
    return api_call(f"oa/todo/list?status={status}" if status else "oa/todo/list")

def main():
    parser = argparse.ArgumentParser(description=f"wecomcli-todo v{VERSION}")
    sub = parser.add_subparsers(dest="action")
    ap = sub.add_parser("add"); ap.add_argument("--title", required=True); ap.add_argument("--priority", choices=[1,2,3], type=int); ap.add_argument("--due"); ap.add_argument("--assign")
    dp = sub.add_parser("done"); dp.add_argument("--todoid", required=True)
    lp = sub.add_parser("list"); lp.add_argument("--status", choices=["pending","done","all"])
    parser.add_argument("--json", action="store_true"); parser.add_argument("--dry-run", action="store_true"); parser.add_argument("--version", action="store_true"); parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if args.version: print(json.dumps({"skill":SKILL_NAME,"version":VERSION,"status":"live"}, indent=2)); return
    if args.json and not args.action: print(json.dumps({"skill":SKILL_NAME,"version":VERSION,"status":"live","features":["add","done","list"],"requires":["wecomcli-setup"]}, indent=2)); return
    if not args.action: parser.print_help(); return
    if args.dry_run:
        dry = {"action":args.action,"dry_run":True,"config_available":bool(load_config())}
        if args.action=="add": dry["title"]=args.title; dry["priority"]=args.priority; dry["due"]=args.due; dry["assign"]=args.assign
        elif args.action=="done": dry["todoid"]=args.todoid
        elif args.action=="list": dry["status"]=args.status
        dry["note"]="Dry run — no API call made."; print(json.dumps(dry,indent=2)); return

    logger = setup_logger(SKILL_NAME, LOG_DIR, args.verbose)
    log_event(logger, "skill_invoked", action=args.action)
    ec = 0
    try:
        if args.action=="add": result = safe_run(logger, api_add, args.title, str(args.priority) if args.priority else "", args.due or "", args.assign or "", logger)
        elif args.action=="done": result = safe_run(logger, api_done, args.todoid, logger)
        elif args.action=="list": result = safe_run(logger, api_list, args.status or "", logger)
        else: result = {"ok":False,"error":f"Unknown: {args.action}"}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if not result.get("ok") and result.get("errcode",-999) not in (-2,-3): ec = 1
    except Exception as e: print(json.dumps({"ok":False,"error":str(e)}, indent=2)); ec = 2
    finally:
        if logger: log_event(logger, "skill_ended", exit_code=ec)
    return ec

if __name__=="__main__": sys.exit(main())
