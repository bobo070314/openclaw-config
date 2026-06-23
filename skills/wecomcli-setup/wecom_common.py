"""
wecomcli 共享配置与API客户端
被 wecomcli-* 系列技能引用
"""
import os
import json
import logging
import urllib.request
import urllib.error
import time
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))

# 配置优先级: 环境变量 > wecom_config.json > 默认值
CONFIG_PATHS = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "wecom_config.json"),
    os.path.expanduser("~/.wecom/config.json"),
    "wecom_config.json",
]

DEFAULT_CONFIG = {
    "corpid": "",
    "corpsecret": "",
    "agentid": 0,
    "api_base": "https://qyapi.weixin.qq.com/cgi-bin",
    "token": "",
    "token_expires_at": 0,
}


def load_config():
    """加载企微配置，环境变量优先"""
    cfg = dict(DEFAULT_CONFIG)
    
    for path in CONFIG_PATHS:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    file_cfg = json.load(f)
                cfg.update(file_cfg)
                break
            except Exception:
                pass

    # 环境变量覆盖
    env_map = {
        "WECOM_CORPID": "corpid",
        "WECOM_CORPSECRET": "corpsecret",
        "WECOM_AGENTID": "agentid",
        "WECOM_API_BASE": "api_base",
    }
    for env_key, cfg_key in env_map.items():
        val = os.environ.get(env_key, "")
        if val:
            if cfg_key == "agentid":
                cfg[cfg_key] = int(val)
            else:
                cfg[cfg_key] = val

    return cfg


def get_access_token(cfg):
    """获取或刷新 access_token，带缓存"""
    now = time.time()
    if cfg.get("token") and cfg.get("token_expires_at", 0) > now + 60:
        return cfg["token"]

    if not cfg.get("corpid") or not cfg.get("corpsecret"):
        return None  # not configured yet; callers should check

    url = (
        f"https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        f"?corpid={cfg['corpid']}&corpsecret={cfg['corpsecret']}"
    )
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if data.get("errcode") != 0:
            raise RuntimeError(f"gettoken failed: {data.get('errmsg', 'unknown')} (errcode={data.get('errcode')})")
        cfg["token"] = data["access_token"]
        cfg["token_expires_at"] = now + data.get("expires_in", 7200) - 300
        return cfg["token"]
    except urllib.error.URLError as e:
        raise RuntimeError(f"Cannot reach WeCom API: {e}")


def api_call(endpoint, method="GET", body=None, params=None):
    """通用企微API调用"""
    cfg = load_config()
    token = get_access_token(cfg)
    if token is None:
        return {
            "ok": False,
            "errcode": -2,
            "errmsg": "WeCom not configured. Set WECOM_CORPID/WECOM_CORPSECRET env vars or run: python wecomcli-setup/run.py init --corpid <id> --secret <secret>",
        }
    base = cfg.get("api_base", "https://qyapi.weixin.qq.com/cgi-bin")
    url = f"{base}/{endpoint}"

    if params is None:
        params = {}
    params["access_token"] = token

    qs = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
    full_url = f"{url}?{qs}"

    data_bytes = None
    if body:
        data_bytes = json.dumps(body, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(
        full_url,
        data=data_bytes,
        headers={"Content-Type": "application/json"} if data_bytes else {},
        method=method,
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        if result.get("errcode", -1) != 0:
            return {
                "ok": False,
                "errcode": result.get("errcode"),
                "errmsg": result.get("errmsg", "unknown"),
            }
        return {"ok": True, "data": result}
    except urllib.error.HTTPError as e:
        body_text = ""
        try:
            body_text = e.read().decode("utf-8")
        except Exception:
            pass
        return {"ok": False, "errcode": e.code, "errmsg": body_text or str(e)}
    except urllib.error.URLError as e:
        return {"ok": False, "errcode": -1, "errmsg": f"Network error: {e}"}


def log_event(logger, event, level="INFO", **kwargs):
    """结构化日志"""
    payload = {
        "timestamp": datetime.now(TZ).isoformat(),
        "skill": logger.name,
        "event": event,
        **kwargs,
    }
    getattr(logger, level.lower(), logger.info)(
        json.dumps(payload, ensure_ascii=False, default=str)
    )


def setup_logger(name, log_dir=None, verbose=False):
    """设置结构化日志"""
    if log_dir is None:
        log_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), ".deploy", "logs"
        )
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.handlers.clear()

    log_file = os.path.join(
        log_dir, f"{datetime.now(TZ).strftime('%Y-%m-%d')}.jsonl"
    )
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(
        logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S"
        )
    )
    logger.addHandler(ch)
    return logger


def safe_run(logger, fn, *a, **kw):
    """安全执行，捕获异常，记录日志"""
    start = time.time()
    try:
        result = fn(*a, **kw)
        elapsed_ms = round((time.time() - start) * 1000, 1)
        log_event(logger, "task_completed", duration_ms=elapsed_ms,
                  result=str(result)[:500])
        return result
    except Exception as e:
        elapsed_ms = round((time.time() - start) * 1000, 1)
        import traceback
        log_event(logger, "task_failed", level="ERROR",
                  duration_ms=elapsed_ms, error=str(e),
                  traceback=traceback.format_exc()[:2000])
        return {"ok": False, "error": str(e)}


# 导出常量
__all__ = [
    "load_config", "get_access_token", "api_call",
    "log_event", "setup_logger", "safe_run", "TZ",
]
