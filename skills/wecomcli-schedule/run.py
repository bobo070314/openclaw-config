#!/usr/bin/env python3
"""wecomcli-schedule v0.2.0 — 企业微信日程管理"""
import argparse, json, os, sys

VERSION = "0.2.0"
SKILL_NAME = "wecomcli-schedule"
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

def api_add(title, time_str, repeat="", remind="", logger=None):
    body = {"schedule_title": title, "schedule_time": time_str}
    if repeat: body["repeat_type"] = repeat
    if remind: body["remind_before"] = int(remind)
    return api_call("oa/schedule/add", method="POST", body=body)

def api_list(date_from="", date_to="", logger=None):
    return api_call("oa/schedule/get_by_calendar")

def api_delete(scheduleid, logger=None):
    return api_call("oa/schedule/del", method="POST", body={"schedule_id": scheduleid})

def main():
    parser = argparse.ArgumentParser(description=f"wecomcli-schedule v{VERSION}")
    sub = parser.add_subparsers(dest="action")
    ap = sub.add_parser("add"); ap.add_argument("--title", required=True); ap.add_argument("--time", required=True); ap.add_argument("--repeat", choices=["daily","weekly"]); ap.add_argument("--remind", help="Minutes before")
    lp = sub.add_parser("list"); lp.add_argument("--from-date", dest="from_date"); lp.add_argument("--to-date", dest="to_date")
    dp = sub.add_parser("delete"); dp.add_argument("--scheduleid", required=True)
    parser.add_argument("--json", action="store_true"); parser.add_argument("--dry-run", action="store_true"); parser.add_argument("--version", action="store_true"); parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if args.version: print(json.dumps({"skill":SKILL_NAME,"version":VERSION,"status":"live"}, indent=2)); return
    if args.json and not args.action: print(json.dumps({"skill":SKILL_NAME,"version":VERSION,"status":"live","features":["add","list","delete"],"requires":["wecomcli-setup"]}, indent=2)); return
    if not args.action: parser.print_help(); return
    if args.dry_run:
        dry = {"action":args.action,"dry_run":True,"config_available":bool(load_config())}
        if args.action=="add": dry["title"]=args.title; dry["time"]=args.time; dry["repeat"]=args.repeat; dry["remind"]=args.remind
        elif args.action=="list": dry["from_date"]=args.from_date; dry["to_date"]=args.to_date
        elif args.action=="delete": dry["scheduleid"]=args.scheduleid
        dry["note"]="Dry run — no API call made."; print(json.dumps(dry,indent=2)); return

    logger = setup_logger(SKILL_NAME, LOG_DIR, args.verbose)
    log_event(logger, "skill_invoked", action=args.action)
    ec = 0
    try:
        if args.action=="add": result = safe_run(logger, api_add, args.title, args.time, args.repeat or "", args.remind or "", logger)
        elif args.action=="list": result = safe_run(logger, api_list, args.from_date or "", args.to_date or "", logger)
        elif args.action=="delete": result = safe_run(logger, api_delete, args.scheduleid, logger)
        else: result = {"ok":False,"error":f"Unknown: {args.action}"}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if not result.get("ok") and result.get("errcode",-999) not in (-2,-3): ec = 1
    except Exception as e: print(json.dumps({"ok":False,"error":str(e)}, indent=2)); ec = 2
    finally:
        if logger: log_event(logger, "skill_ended", exit_code=ec)
    return ec

if __name__=="__main__": sys.exit(main())
