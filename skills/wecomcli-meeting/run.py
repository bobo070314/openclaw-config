#!/usr/bin/env python3
"""wecomcli-meeting v0.2.0 — 企业微信会议管理"""
import argparse, json, os, sys

VERSION = "0.2.0"
SKILL_NAME = "wecomcli-meeting"
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

def api_create(title, start, end, attendees="", logger=None):
    body = {"meeting_title": title, "meeting_start": start, "meeting_end": end}
    if attendees: body["attendees"] = [a.strip() for a in attendees.split(",")]
    return api_call("meeting/create", method="POST", body=body)

def api_cancel(meetingid, logger=None):
    return api_call("meeting/cancel", method="POST", body={"meetingid": meetingid})

def api_list(userid="", logger=None):
    return api_call(f"meeting/get_user_meetinginfo?userid={userid}" if userid else "meeting/list")

def main():
    parser = argparse.ArgumentParser(description=f"wecomcli-meeting v{VERSION}")
    sub = parser.add_subparsers(dest="action")
    cp = sub.add_parser("create"); cp.add_argument("--title", required=True); cp.add_argument("--start", required=True); cp.add_argument("--end", required=True); cp.add_argument("--attendees")
    canp = sub.add_parser("cancel"); canp.add_argument("--meetingid", required=True)
    lp = sub.add_parser("list"); lp.add_argument("--userid")
    parser.add_argument("--json", action="store_true"); parser.add_argument("--dry-run", action="store_true"); parser.add_argument("--version", action="store_true"); parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if args.version: print(json.dumps({"skill":SKILL_NAME,"version":VERSION,"status":"live"}, indent=2)); return
    if args.json and not args.action: print(json.dumps({"skill":SKILL_NAME,"version":VERSION,"status":"live","features":["create","cancel","list"],"requires":["wecomcli-setup"]}, indent=2)); return
    if not args.action: parser.print_help(); return
    if args.dry_run:
        dry = {"action":args.action,"dry_run":True,"config_available":bool(load_config())}
        if args.action=="create": dry["title"]=args.title; dry["start"]=args.start; dry["end"]=args.end; dry["attendees"]=args.attendees
        elif args.action=="cancel": dry["meetingid"]=args.meetingid
        elif args.action=="list": dry["userid"]=args.userid
        dry["note"]="Dry run — no API call made."; print(json.dumps(dry,indent=2)); return

    logger = setup_logger(SKILL_NAME, LOG_DIR, args.verbose)
    log_event(logger, "skill_invoked", action=args.action)
    ec = 0
    try:
        if args.action=="create": result = safe_run(logger, api_create, args.title, args.start, args.end, args.attendees or "", logger)
        elif args.action=="cancel": result = safe_run(logger, api_cancel, args.meetingid, logger)
        elif args.action=="list": result = safe_run(logger, api_list, args.userid or "", logger)
        else: result = {"ok":False,"error":f"Unknown: {args.action}"}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if not result.get("ok") and result.get("errcode",-999) not in (-2,-3): ec = 1
    except Exception as e: print(json.dumps({"ok":False,"error":str(e)}, indent=2)); ec = 2
    finally:
        if logger: log_event(logger, "skill_ended", exit_code=ec)
    return ec

if __name__=="__main__": sys.exit(main())
