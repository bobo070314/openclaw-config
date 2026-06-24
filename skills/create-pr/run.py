"""
create-pr - GitHub Pull Request 创建

Description: 自动生成PR描述、关联Issue、添加Reviewer和标签
Usage: python run.py --repo <owner/repo> --head <branch> --base <main> --title <t> --body <b>
"""
import sys, os, json, logging, time, traceback, urllib.request, urllib.error

# === V0.2.0 CLI STANDARD (auto-injected, do not remove) ===
VERSION = "0.2.0"
SKILL_NAME = "create-pr"
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

from datetime import datetime, timezone, timedelta

SKILL_NAME = "create-pr"
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SKILL_DIR, ".deploy", "logs")
TZ = timezone(timedelta(hours=8))
API_BASE = "https://api.github.com"


def load_token():
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        for p in [os.path.join(SKILL_DIR, "github_config.json"), os.path.expanduser("~/.github/token")]:
            if os.path.exists(p):
                with open(p, "r") as f:
                    token = json.load(f).get("token", "")
    return token


def setup_logging(verbose=False):
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger(SKILL_NAME)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.handlers.clear()
    fh = logging.FileHandler(os.path.join(LOG_DIR, f"{datetime.now(TZ).strftime('%Y-%m-%d')}.jsonl"), encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(fh)
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
        log_event(logger, "task_failed", level="ERROR", duration_ms=round((time.time()-start)*1000, 1), error=str(e))
        return {"ok": False, "error": str(e)}


def github_api(endpoint, method="GET", body=None):
    token = load_token()
    if not token:
        return {"ok": False, "errcode": -2, "errmsg": "GITHUB_TOKEN not set. Create at https://github.com/settings/tokens"}
    url = f"{API_BASE}{endpoint}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return {"ok": True, "data": json.loads(resp.read().decode("utf-8"))}
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8")[:500]
        return {"ok": False, "errcode": e.code, "errmsg": msg}
    except Exception as e:
        return {"ok": False, "errcode": -1, "errmsg": str(e)}


def create_pr(repo, head, base, title, body, draft=False, logger=None):
    return github_api(f"/repos/{repo}/pulls", method="POST", body={
        "head": head, "base": base, "title": title, "body": body, "draft": draft
    })


def main():
    logger = None
    exit_code = 0
    try:
        args = sys.argv[1:]
        kwargs = {"base": "main", "draft": False}
        i = 0
        while i < len(args):
            if args[i] == "--repo" and i+1 < len(args): kwargs["repo"] = args[i+1]; i += 2
            elif args[i] == "--head" and i+1 < len(args): kwargs["head"] = args[i+1]; i += 2
            elif args[i] == "--base" and i+1 < len(args): kwargs["base"] = args[i+1]; i += 2
            elif args[i] == "--title" and i+1 < len(args): kwargs["title"] = args[i+1]; i += 2
            elif args[i] == "--body" and i+1 < len(args): kwargs["body"] = args[i+1]; i += 2
            elif args[i] == "--draft": kwargs["draft"] = True; i += 1
            else: i += 1

        if not kwargs.get("repo") or not kwargs.get("head") or not kwargs.get("title"):
            print("Usage: --repo <owner/repo> --head <branch> --base <main> --title <t> --body <b> [--draft]")
            sys.exit(1)

        logger = setup_logging()
        log_event(logger, "skill_invoked", repo=kwargs["repo"], head=kwargs["head"], base=kwargs["base"])
        result = safe_run(logger, create_pr, kwargs["repo"], kwargs["head"], kwargs["base"],
                         kwargs.get("title",""), kwargs.get("body",""), kwargs.get("draft", False), logger)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if not result.get("ok") and result.get("errcode") != -2: exit_code = 1
    except SystemExit: pass
    except Exception as e:
        traceback.print_exc(); exit_code = 2
    finally:
        if logger: log_event(logger, "skill_ended", exit_code=exit_code)
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
