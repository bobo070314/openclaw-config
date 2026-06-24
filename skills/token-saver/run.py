#!/usr/bin/env python
"""
token-saver v0.1.0 - 命令输出智能压缩器
==========================================
拦截长命令输出，保留首尾+摘要统计，大幅减少 Token 消耗。

用法:
    python token-saver/run.py <命令> [参数...]
    python token-saver/run.py git log --oneline -100
    python token-saver/run.py npm audit

输出格式:
    人类可读摘要 + JSON 统计块（TOKEN_SAVER_SUMMARY）
"""

import subprocess
import shlex

# === V0.2.0 CLI STANDARD (auto-injected, do not remove) ===
VERSION = "0.2.0"
SKILL_NAME = "token-saver"
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

import sys
import json
from datetime import datetime, timezone

UTC = timezone.utc

# ===== 配置 =====
MAX_LINES = 50          # 超过此行数触发压缩
KEEP_HEAD = 12          # 保留开头行数
KEEP_TAIL = 12          # 保留结尾行数
DEFAULT_TIMEOUT = 120   # 默认超时秒数

# ===== 核心逻辑 =====


def compress_output(text: str, max_lines: int = MAX_LINES) -> dict:
    """压缩文本输出，返回结构化摘要"""
    if not text:
        return {"compressed": False, "full": "", "total_lines": 0, "preview": ""}

    lines = text.splitlines()
    total_lines = len(lines)

    if total_lines <= max_lines:
        return {"compressed": False, "full": text, "total_lines": total_lines, "preview": text}

    head = lines[:KEEP_HEAD]
    tail = lines[-KEEP_TAIL:] if KEEP_TAIL > 0 else []
    middle_count = total_lines - KEEP_HEAD - KEEP_TAIL

    # 中间采样：每隔 N 行取一行
    sample_interval = max(1, middle_count // 5)
    middle_sample = []
    for i in range(KEEP_HEAD, total_lines - KEEP_TAIL, sample_interval):
        if len(middle_sample) < 8:
            middle_sample.append(f"  [{i}] {lines[i][:120]}")

    # 统计模式
    lowered = text.lower()
    error_count = lowered.count("error") + lowered.count("err ") + lowered.count("fail")
    warning_count = lowered.count("warn")
    info_count = lowered.count("info")

    parts = [
        f"--- TOKEN-SAVER: {total_lines}行 -> 压缩显示 ---",
        f"=== HEAD ({KEEP_HEAD}/{total_lines}) ===",
        *head,
        f"=== ... {middle_count} 行省略 ({KEEP_TAIL}行尾部保留) ... ===",
    ]
    if middle_sample:
        parts.append("=== MIDDLE SAMPLE ===")
        parts.extend(middle_sample)
    parts.extend([
        f"=== TAIL ({KEEP_TAIL}/{total_lines}) ===",
        *tail,
        f"=== STATS: ERR={error_count} WARN={warning_count} INFO={info_count} ===",
    ])

    return {
        "compressed": True,
        "original_lines": total_lines,
        "compressed_lines": len(parts),
        "compressed_text": "\n".join(parts),
        "error_count": error_count,
        "warning_count": warning_count,
        "info_count": info_count,
        "head": head,
        "tail": tail,
    }


def run_command_with_compression(cmd: str, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """执行命令并压缩输出"""
    start_time = datetime.now(UTC).isoformat()

    try:
        # 安全修复: 禁用 shell=True，使用 shlex.split 避免命令注入
        safe_cmd = shlex.split(cmd) if isinstance(cmd, str) else cmd
        result = subprocess.run(
            safe_cmd,
            capture_output=True, text=True, timeout=timeout,
            shell=False,
            encoding="utf-8", errors="replace",
        ))
        stdout = result.stdout or ""
        stderr = result.stderr or ""

        return {
            "success": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": compress_output(stdout),
            "stderr": compress_output(stderr),
            "duration": datetime.now(UTC).isoformat(),
            "start_time": start_time,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"TIMEOUT ({timeout}s)", "exit_code": -1}
    except Exception as e:
        return {"success": False, "error": f"EXEC_FAIL: {e}", "exit_code": -1}


def main():
    if len(sys.argv) < 2:
        print("用法: python token-saver/run.py <命令> [参数...]")
        print("示例: python token-saver/run.py git log --oneline -100")
        sys.exit(1)

    cmd = " ".join(sys.argv[1:])
    print(f"[token-saver] RUN: {cmd[:100]}{'...' if len(cmd) > 100 else ''}")
    print("-" * 50)

    result = run_command_with_compression(cmd)

    if result.get("error"):
        print(f"[token-saver] FAIL: {result['error']}")
        sys.exit(1)

    # --- stdout ---
    sd = result.get("stdout", {})
    if sd:
        if sd.get("compressed"):
            print(f"[token-saver] COMPRESSED {sd['original_lines']} -> {sd['compressed_lines']} lines")
        print(sd.get("compressed_text") or sd.get("full", ""))

    # --- stderr ---
    se = result.get("stderr", {})
    if se and se.get("compressed_text"):
        print("\n[token-saver] STDERR:")
        print(se["compressed_text"])

    # --- JSON summary block ---
    summary = {
        "exit_code": result["exit_code"],
        "stdout_lines": sd.get("original_lines", 0) if sd else 0,
        "stderr_lines": se.get("original_lines", 0) if se else 0,
        "errors": (sd.get("error_count", 0) if sd else 0) + (se.get("error_count", 0) if se else 0),
        "duration": result.get("duration", ""),
    }
    print("\n--- TOKEN_SAVER_SUMMARY ---")
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    sys.exit(result["exit_code"])


if __name__ == "__main__":
    main()
