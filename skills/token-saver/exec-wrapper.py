#!/usr/bin/env python
"""
exec-wrapper.py — 透明 token-saver 代理
=========================================
将所有被包裹的命令输出自动压缩，减少 Token 消耗。

用法:
    python exec-wrapper.py <原始命令> [参数...]
    python exec-wrapper.py python skills/security-audit/run.py --target foo.py

原理:
    1. 执行原始命令
    2. stdout/stderr 超 N 行则触发 token-saver 压缩
    3. 输出压缩版 + 统计摘要
    4. 保持原始 exit code 不变
"""

import subprocess
import sys
import os
from pathlib import Path

# 注入 token-saver 路径
ROOT = Path(__file__).resolve().parent.parent.parent
TOKEN_SAVER = ROOT / "skills" / "token-saver" / "run.py"

MAX_LINES = int(os.environ.get("TOKEN_SAVER_MAX_LINES", "50"))
TIMEOUT = int(os.environ.get("TOKEN_SAVER_TIMEOUT", "120"))


def run_wrapped(args: list) -> int:
    """Execute command via token-saver compression layer."""
    if not TOKEN_SAVER.exists():
        print("[exec-wrapper] token-saver not found, running raw", file=sys.stderr)
        result = subprocess.run(args)
        return result.returncode

    cmd = [sys.executable, str(TOKEN_SAVER)] + args
    result = subprocess.run(cmd)
    return result.returncode


def main():
    if len(sys.argv) < 2:
        print("Usage: python exec-wrapper.py <command> [args...]")
        sys.exit(1)

    args = sys.argv[1:]
    sys.exit(run_wrapped(args))


if __name__ == "__main__":
    main()
