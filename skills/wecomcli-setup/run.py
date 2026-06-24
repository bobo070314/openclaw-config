"""
wecomcli-setup - 企业微信CLI环境配置

Description: 安装配置wecomcli、验证连接、环境诊断
Usage: python run.py init [--corpid <id> --secret <secret> --agentid <id>]
       python run.py check
       python run.py diagnose
       python run.py config
"""
import sys

# === V0.2.0 CLI STANDARD (auto-injected, do not remove) ===
VERSION = "0.2.0"
SKILL_NAME = "wecomcli-setup"
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wecom_common import (
    api_call, load_config, get_access_token,
    setup_logger, log_event, safe_run,
)

SKILL_NAME = "wecomcli-setup"
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".deploy", "logs")


def init_config(corpid, secret, agentid, logger=None):
    """初始化配置文件"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wecom_config.json")
    config = {
        "corpid": corpid,
        "corpsecret": secret,
        "agentid": int(agentid) if agentid else 0,
        "api_base": "https://qyapi.weixin.qq.com/cgi-bin",
    }
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return {"ok": True, "config_path": config_path, "message": "Configuration saved"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def check_connection(logger=None):
    """验证企微API连接"""
    cfg = load_config()
    result = {
        "ok": True,
        "checks": {},
        "config": {
            "corpid": cfg.get("corpid", "NOT SET")[:8] + "***" if cfg.get("corpid") else "NOT SET",
            "has_secret": bool(cfg.get("corpsecret")),
            "agentid": cfg.get("agentid", "NOT SET"),
            "api_base": cfg.get("api_base", "default"),
        },
    }

    # Check 1: Can reach API
    try:
        import urllib.request
        urllib.request.urlopen("https://qyapi.weixin.qq.com", timeout=5)
        result["checks"]["api_reachable"] = True
    except Exception as e:
        result["checks"]["api_reachable"] = False
        result["checks"]["api_error"] = str(e)
        result["ok"] = False

    # Check 2: Can get token
    try:
        token = get_access_token(cfg)
        result["checks"]["token_ok"] = True
        result["checks"]["token_preview"] = token[:8] + "***"
    except Exception as e:
        result["checks"]["token_ok"] = False
        result["checks"]["token_error"] = str(e)
        result["ok"] = False

    # Check 3: List departments (basic permission check)
    try:
        dept_resp = api_call("department/list")
        result["checks"]["department_access"] = dept_resp.get("ok", False)
        if not dept_resp.get("ok"):
            result["checks"]["department_error"] = dept_resp.get("errmsg", "unknown")
            result["ok"] = False
    except Exception as e:
        result["checks"]["department_access"] = False
        result["checks"]["department_error"] = str(e)

    return result


def show_config(logger=None):
    """显示当前配置（脱敏）"""
    cfg = load_config()
    return {"ok": True, "data": {
        "corpid": cfg.get("corpid", "NOT SET")[:8] + "***" if cfg.get("corpid") else "NOT SET",
        "has_secret": bool(cfg.get("corpsecret")),
        "agentid": cfg.get("agentid", 0),
        "api_base": cfg.get("api_base", "https://qyapi.weixin.qq.com/cgi-bin"),
        "config_sources": [
            p for p in [
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "wecom_config.json"),
                os.path.expanduser("~/.wecom/config.json"),
            ] if os.path.exists(p)
        ],
        "env_vars": {
            k: "SET" for k in ["WECOM_CORPID", "WECOM_CORPSECRET", "WECOM_AGENTID"] if os.environ.get(k)
        },
    }}


def diagnose(logger=None):
    """全面环境诊断"""
    result = {
        "python_version": sys.version,
        "platform": sys.platform,
        "skill_dir": os.path.dirname(os.path.abspath(__file__)),
        "wecom_common_exists": os.path.exists(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "wecom_common.py")
        ),
    }

    # Check config
    cfg = load_config()
    result["config"] = {
        "corpid_set": bool(cfg.get("corpid")),
        "secret_set": bool(cfg.get("corpsecret")),
        "agentid_set": bool(cfg.get("agentid")),
    }

    # Check network
    try:
        import urllib.request
        urllib.request.urlopen("https://qyapi.weixin.qq.com", timeout=5)
        result["network"] = "ok"
    except Exception as e:
        result["network"] = f"blocked: {e}"

    # Check other wecom skills exist
    siblings = [
        "wecomcli-contact", "wecomcli-msg", "wecomcli-doc",
        "wecomcli-meeting", "wecomcli-schedule", "wecomcli-todo",
    ]
    parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result["sibling_skills"] = {
        s: os.path.exists(os.path.join(parent, s, "run.py")) for s in siblings
    }

    return {"ok": True, "data": result}


def main():
    logger = None
    exit_code = 0
    try:
        args = sys.argv[1:]
        if not args or args[0] not in ("init", "check", "diagnose", "config"):
            print("Usage: python run.py <action> [options]")
            print("  init --corpid <id> --secret <secret> --agentid <id>")
            print("  check     # Test API connection")
            print("  diagnose  # Full environment diagnostic")
            print("  config    # Show current config (sanitized)")
            print(f"\nLogs: {LOG_DIR}")
            print(f"\nEnv vars: WECOM_CORPID, WECOM_CORPSECRET, WECOM_AGENTID")
            sys.exit(1)

        action = args[0]
        kwargs = {"verbose": False}
        i = 1
        while i < len(args):
            if args[i] == "--corpid" and i + 1 < len(args):
                kwargs["corpid"] = args[i + 1]; i += 2
            elif args[i] == "--secret" and i + 1 < len(args):
                kwargs["secret"] = args[i + 1]; i += 2
            elif args[i] == "--agentid" and i + 1 < len(args):
                kwargs["agentid"] = args[i + 1]; i += 2
            elif args[i] == "--verbose":
                kwargs["verbose"] = True; i += 1
            else:
                i += 1

        logger = setup_logger(SKILL_NAME, LOG_DIR, kwargs["verbose"])
        log_event(logger, "skill_invoked", action=action, args=sys.argv[1:])

        if action == "init":
            result = safe_run(logger, init_config,
                kwargs.get("corpid", ""), kwargs.get("secret", ""),
                kwargs.get("agentid", "0"), logger)
        elif action == "check":
            result = safe_run(logger, check_connection, logger)
        elif action == "diagnose":
            result = safe_run(logger, diagnose, logger)
        elif action == "config":
            result = safe_run(logger, show_config, logger)

        print(json.dumps(result, indent=2, ensure_ascii=False))
        if not result.get("ok"):
            exit_code = 1

    except SystemExit:
        pass
    except Exception as e:
        print(f"[{SKILL_NAME}] FATAL: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        exit_code = 2
    finally:
        if logger:
            log_event(logger, "skill_ended", exit_code=exit_code)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
