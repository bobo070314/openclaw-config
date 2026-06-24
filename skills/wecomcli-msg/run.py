#!/usr/bin/env python3
"""
wecomcli-msg v0.2.0 — 企业微信消息发送
========================================
发送文本/图片/文件消息到指定用户。
Depends on: wecomcli-setup (shared wecom_common module)

Usage:
  python run.py send --to <userid> --text <message>
  python run.py recall --msgid <id>
  python run.py status --msgid <id>
  python run.py --version
  python run.py --json --dry-run send --to user1 --text "Hello"
"""
import argparse
import json
import os
import sys

VERSION = "0.2.0"
SKILL_NAME = "wecomcli-msg"
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SKILL_DIR, ".deploy", "logs")

# Import shared WeCom module
sys.path.insert(0, os.path.join(SKILL_DIR, "..", "wecomcli-setup"))
try:
    from wecom_common import api_call, setup_logger, log_event, safe_run, load_config
except ImportError:
    # Stub fallback when wecomcli-setup is not available
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


def send_text(to_user, content, logger):
    cfg = load_config()
    agentid = cfg.get("agentid", 0)
    if not agentid:
        return {"ok": False, "errcode": -2, "errmsg": "WeCom not configured. Set WECOM_AGENTID env var."}
    body = {"touser": to_user, "msgtype": "text", "agentid": agentid, "text": {"content": content}}
    return api_call("message/send", method="POST", body=body)


def recall_message(msgid, logger):
    return api_call("message/recall", method="POST", body={"msgid": msgid})


def main():
    parser = argparse.ArgumentParser(description=f"wecomcli-msg v{VERSION}")
    sub = parser.add_subparsers(dest="action", help="Action")

    # send
    sp = sub.add_parser("send", help="Send a message")
    sp.add_argument("--to", required=True, dest="to_user", help="Recipient userid or @all")
    sp.add_argument("--text", help="Text content")
    sp.add_argument("--image", help="Image file path")
    sp.add_argument("--file", help="File path")

    # recall
    rp = sub.add_parser("recall", help="Recall a message")
    rp.add_argument("--msgid", required=True, help="Message ID to recall")

    # status
    stp = sub.add_parser("status", help="Check message status")
    stp.add_argument("--msgid", required=True, help="Message ID")

    # Global
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--dry-run", action="store_true", help="Preview without API call")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--verbose", action="store_true", help="Debug logging")

    args = parser.parse_args()

    if args.version:
        print(json.dumps({"skill": SKILL_NAME, "version": VERSION, "status": "live"}, indent=2))
        return

    if args.json and not args.action:
        print(json.dumps({"skill": SKILL_NAME, "version": VERSION, "status": "live", "features": ["send", "recall", "status"], "requires": ["wecomcli-setup", "WECOM_AGENTID"]}, indent=2))
        return

    if not args.action:
        parser.print_help()
        return

    if args.dry_run:
        dry = {"action": args.action, "dry_run": True, "config_available": bool(load_config().get("agentid"))}
        if args.action == "send":
            dry["to"] = args.to_user
            dry["text"] = args.text
            dry["image"] = args.image
            dry["file"] = args.file
        elif args.action in ("recall", "status"):
            dry["msgid"] = args.msgid
        dry["note"] = "Dry run — no API call made."
        print(json.dumps(dry, indent=2))
        return

    logger = setup_logger(SKILL_NAME, LOG_DIR, args.verbose)
    log_event(logger, "skill_invoked", action=args.action)

    exit_code = 0
    try:
        if args.action == "send":
            if args.text:
                result = safe_run(logger, send_text, args.to_user, args.text, logger)
            elif args.image:
                result = {"ok": False, "error": "Image sending needs media upload. Not yet implemented."}
            elif args.file:
                result = {"ok": False, "error": "File sending needs media upload. Not yet implemented."}
            else:
                result = {"ok": False, "error": "Need --text, --image, or --file"}
        elif args.action == "recall":
            result = safe_run(logger, recall_message, args.msgid, logger)
        elif args.action == "status":
            result = {"ok": False, "error": "Message status query not yet implemented"}
        else:
            result = {"ok": False, "error": f"Unknown action: {args.action}"}

        print(json.dumps(result, indent=2, ensure_ascii=False))
        if not result.get("ok") and result.get("errcode", -999) not in (-2, -3):
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
