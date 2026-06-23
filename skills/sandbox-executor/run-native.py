#!/usr/bin/env python
"""
sandbox-executor v0.2.0 — Unified Sandbox Executor (Docker + Native fallback)
==============================================================================
Auto-detects Docker availability:
  - Docker available → containers (read-only root, no network, cap-drop ALL)
  - Docker unavailable → temp dir isolation (native fallback)

Usage:
    python sandbox-executor/run.py [--no-workspace] [--timeout N] <skill_name> [args...]
"""

import argparse
import json
import subprocess
import sys
import os
import time
import shutil
import tempfile
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional


# ── Configuration ──────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent.parent
SKILLS_DIR = ROOT / "skills"
WORKSPACE_DIR = ROOT / "workspace"
LOGS_DIR = ROOT / ".deploy" / "logs"
IMAGE_NAME = "openclaw-sandbox:latest"
TMPFS_SIZE = "64M"
DEFAULT_TIMEOUT = 60
SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.next', 'dist', 'build', 'target'}


def ensure_log_dir():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def log_event(event_type: str, details: dict):
    ensure_log_dir()
    log_file = LOGS_DIR / "sandbox.jsonl"
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event_type,
        **details,
    }
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def docker_available() -> bool:
    """Check if Docker daemon is running and sandbox image exists."""
    try:
        r = subprocess.run(
            ["docker", "ps"], capture_output=True, text=True,
            timeout=5, encoding="utf-8", errors="replace",
        )
        if r.returncode != 0:
            return False
    except Exception:
        return False

    try:
        r = subprocess.run(
            ["docker", "image", "inspect", IMAGE_NAME],
            capture_output=True, text=True, timeout=5,
            encoding="utf-8", errors="replace",
        )
        return r.returncode == 0
    except Exception:
        return False


def safe_copy(src_dir: Path, dst_dir: Path, max_size_mb: int = 50):
    """Copy directory to sandbox (one-way: never write back to host)."""
    items = list(src_dir.iterdir())
    print(f"[sandbox-executor:native] Copying {len(items)} items from {src_dir.name}...", flush=True)
    for item in items:
        if item.name in SKIP_DIRS:
            continue
        dst = dst_dir / item.name
        if item.is_dir():
            shutil.copytree(
                item, dst, symlinks=False, dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(*SKIP_DIRS)
            )
        else:
            size_mb = item.stat().st_size / (1024 * 1024)
            if size_mb > max_size_mb:
                print(f"[sandbox-executor:native] Skipping large file: {item.name} ({size_mb:.1f}MB)", flush=True)
                continue
            shutil.copy2(item, dst)


# ── Docker Sandbox ──────────────────────────────────────────────

def run_sandbox_docker(skill_name: str, args: list, allow_network: bool = False,
                       gpu: bool = False, timeout: int = DEFAULT_TIMEOUT) -> dict:
    skill_dir = SKILLS_DIR / skill_name
    if not skill_dir.exists():
        return {"exit_code": -1, "stdout": "", "stderr": f"Skill '{skill_name}' not found", "duration_ms": 0}

    run_py = skill_dir / "run.py"
    if not run_py.exists():
        return {"exit_code": -1, "stdout": "", "stderr": f"run.py missing in {skill_dir}", "duration_ms": 0}

    docker_cmd = [
        "docker", "run",
        "--rm",
        "--read-only",
        "--network", "none",
        "--tmpfs", f"/tmp:rw,noexec,nosuid,size={TMPFS_SIZE}",
        "--memory", "512m",
        "--cpus", "1",
        "--pids-limit", "100",
        "--security-opt", "no-new-privileges:true",
        "--cap-drop", "ALL",
        "--user", "sandbox",
        "-v", f"{skill_dir}:/skill:ro",
        "-v", f"{WORKSPACE_DIR}:/workspace:ro",
        "-w", "/skill",
    ]

    if allow_network:
        docker_cmd[docker_cmd.index("--network") + 1] = "bridge"

    if gpu:
        docker_cmd.insert(1, "--gpus")
        docker_cmd.insert(2, "all")

    docker_cmd.append(IMAGE_NAME)
    docker_cmd.extend(args)

    log_event("sandbox_invoked", {
        "skill": skill_name, "args": args,
        "allow_network": allow_network,
        "executor": "docker",
        "docker_cmd": " ".join(docker_cmd),
    })

    print(f"[sandbox-executor:docker] Running: {' '.join(docker_cmd)}", flush=True)

    start = time.perf_counter()
    try:
        result = subprocess.run(
            docker_cmd, capture_output=True, text=True,
            timeout=timeout, cwd=str(ROOT),
            encoding="utf-8", errors="replace",
        )
    except subprocess.TimeoutExpired:
        duration_ms = (time.perf_counter() - start) * 1000
        log_event("sandbox_timeout", {"skill": skill_name, "timeout_s": timeout})
        return {"exit_code": 137, "stdout": "", "stderr": f"Timed out after {timeout}s", "duration_ms": duration_ms}

    duration_ms = (time.perf_counter() - start) * 1000
    log_event("sandbox_completed", {
        "skill": skill_name, "exit_code": result.returncode,
        "duration_ms": round(duration_ms, 1), "executor": "docker",
    })

    return {
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "duration_ms": round(duration_ms, 1),
    }


# ── Native Sandbox (fallback) ───────────────────────────────────

def run_sandbox_native(skill_name: str, args: list, timeout: int = DEFAULT_TIMEOUT,
                       copy_workspace: bool = True) -> dict:
    skill_dir = SKILLS_DIR / skill_name
    if not skill_dir.exists():
        return {"exit_code": -1, "stdout": "", "stderr": f"Skill '{skill_name}' not found", "duration_ms": 0}

    run_py = skill_dir / "run.py"
    if not run_py.exists():
        return {"exit_code": -1, "stdout": "", "stderr": f"run.py missing in {skill_dir}", "duration_ms": 0}

    ensure_log_dir()
    print(f"[sandbox-executor:native] Creating sandbox for skill '{skill_name}'...", flush=True)
    sandbox_tmp = Path(tempfile.mkdtemp(prefix="oc_sandbox_"))
    try:
        sandbox_skill = sandbox_tmp / "skill"
        sandbox_skill.mkdir()
        safe_copy(skill_dir, sandbox_skill)

        if copy_workspace and WORKSPACE_DIR.exists():
            sandbox_ws = sandbox_tmp / "workspace"
            sandbox_ws.mkdir()
            safe_copy(WORKSPACE_DIR, sandbox_ws)

        cmd = [sys.executable, str(sandbox_skill / "run.py"), *args]

        log_event("sandbox_invoked", {
            "skill": skill_name, "args": args,
            "sandbox_tmp": str(sandbox_tmp),
            "executor": "native",
        })

        print(f"[sandbox-executor:native] Running: {' '.join(cmd)}", flush=True)
        print(f"[sandbox-executor:native] Isolated at: {sandbox_tmp}", flush=True)

        start = time.perf_counter()
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout,
                cwd=str(sandbox_tmp),
                encoding="utf-8", errors="replace",
                env={**os.environ, "PYTHONIOENCODING": "utf-8", "SANDBOX_ROOT": str(sandbox_tmp)},
            )
        except subprocess.TimeoutExpired:
            duration_ms = (time.perf_counter() - start) * 1000
            log_event("sandbox_timeout", {"skill": skill_name, "timeout_s": timeout})
            return {"exit_code": 137, "stdout": "", "stderr": f"Timed out after {timeout}s", "duration_ms": duration_ms}

        duration_ms = (time.perf_counter() - start) * 1000
        log_event("sandbox_completed", {
            "skill": skill_name, "exit_code": result.returncode,
            "duration_ms": round(duration_ms, 1), "executor": "native",
        })

        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration_ms": round(duration_ms, 1),
        }
    finally:
        try:
            shutil.rmtree(sandbox_tmp, ignore_errors=True)
        except Exception:
            pass


# ── Main Gateway ────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="sandbox-executor v0.2.0 — Unified Isolated Execution Gateway")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--no-workspace", action="store_true", help="Skip workspace copy (native only)")
    parser.add_argument("--allow-network", action="store_true", help="Allow network in sandbox (Docker only)")
    parser.add_argument("--gpu", action="store_true", help="Enable GPU (Docker only)")
    parser.add_argument("skill", help="Skill name")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Args for skill's run.py")
    parsed = parser.parse_args()

    use_docker = docker_available()
    executor = "docker" if use_docker else "native"
    print(f"[sandbox-executor] Mode: {executor}")

    if use_docker:
        result = run_sandbox_docker(
            parsed.skill, parsed.args,
            allow_network=parsed.allow_network,
            gpu=parsed.gpu,
            timeout=parsed.timeout,
        )
    else:
        result = run_sandbox_native(
            parsed.skill, parsed.args,
            timeout=parsed.timeout,
            copy_workspace=not parsed.no_workspace,
        )

    if result["stdout"]:
        print(result["stdout"])
    if result["stderr"]:
        print(result["stderr"], file=sys.stderr)

    print(f"\n[sandbox-executor:{executor}] Duration: {result['duration_ms']}ms | Exit: {result['exit_code']}")
    sys.exit(result["exit_code"])


if __name__ == "__main__":
    main()
