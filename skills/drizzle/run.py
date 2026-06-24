#!/usr/bin/env python
"""
drizzle v0.2.0 — 数据库迁移工具（增强版）
==========================================
drizzle-kit wrapper with structured JSON output and dry-run support.

用法:
    python run.py [--dry-run] [--json] [generate|push|migrate|status]

安全保证:
    --dry-run 模式仅预览命令，不实际执行
    所有输出可通过 --json 获得结构化结果
"""

import subprocess

# === V0.2.0 CLI STANDARD (auto-injected, do not remove) ===
VERSION = "0.2.0"
SKILL_NAME = "drizzle"
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
import argparse
from datetime import datetime, timezone
from pathlib import Path


# ===== 核心逻辑 =====

def run_drizzle_command(args: list, dry_run: bool = False, timeout: int = 60) -> dict:
    """执行 drizzle-kit 命令，返回结构化结果"""
    cmd = ["npx", "drizzle-kit"] + args

    # Dry-run: 只预览
    if dry_run:
        return {
            "success": True,
            "dry_run": True,
            "message": f"[DRY RUN] Would execute: {' '.join(cmd)}",
            "command": " ".join(cmd),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # 真实执行
    try:
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace",
        )
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        success = result.returncode == 0

        # 统计错误/警告
        error_lines = [l for l in (stdout + stderr).splitlines() if "error" in l.lower() or "fail" in l.lower()]
        warn_lines = [l for l in (stdout + stderr).splitlines() if "warn" in l.lower()]

        return {
            "success": success,
            "dry_run": False,
            "exit_code": result.returncode,
            "stdout": stdout.strip(),
            "stderr": stderr.strip(),
            "stdout_preview": stdout[:500],
            "stderr_preview": stderr[:200],
            "error_count": len(error_lines),
            "warning_count": len(warn_lines),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"Command timed out after {timeout}s"}
    except FileNotFoundError:
        return {"success": False, "error": "npx not found. Install Node.js 18+ from https://nodejs.org"}
    except Exception as e:
        return {"success": False, "error": f"Execution failed: {e}"}


def check_drizzle_installed() -> dict:
    """Check if drizzle-kit is available."""
    try:
        result = subprocess.run(
            ["npx", "drizzle-kit", "--version"],
            capture_output=True, text=True, timeout=15,
            encoding="utf-8", errors="replace",
        )
        return {
            "installed": result.returncode == 0,
            "version": result.stdout.strip().split("\n")[0] if result.stdout else "unknown",
        }
    except FileNotFoundError:
        return {"installed": False, "reason": "npx not found"}
    except Exception as e:
        return {"installed": False, "reason": str(e)}


# ===== CLI =====

def main():
    parser = argparse.ArgumentParser(description="Drizzle database migration tool")
    parser.add_argument(
        "action", nargs="?", default="status",
        choices=["generate", "push", "migrate", "status", "check"],
        help="Action to perform (default: status)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no execution")
    parser.add_argument("--json", action="store_true", help="Output as structured JSON")
    args = parser.parse_args()

    # Handle 'check' separately
    if args.action == "check":
        result = check_drizzle_installed()
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if result["installed"]:
                print(f"✅ drizzle-kit available: {result.get('version', 'yes')}")
            else:
                print(f"❌ drizzle-kit not available: {result.get('reason', 'unknown')}")
        sys.exit(0 if result["installed"] else 1)

    # Build drizzle-kit args
    drizzle_args = [args.action]

    # Execute
    result = run_drizzle_command(drizzle_args, dry_run=args.dry_run)

    # Output
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    else:
        if result.get("dry_run"):
            print(result["message"])
        elif result.get("error"):
            print(f"[drizzle] ERROR: {result['error']}")
        elif result.get("success"):
            print("[drizzle] OK")
            if result.get("stdout"):
                print(result["stdout"][:1000])
        else:
            print(f"[drizzle] FAIL (exit {result.get('exit_code', '?')})")
            if result.get("stderr"):
                print(result["stderr"][:1000])

    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
