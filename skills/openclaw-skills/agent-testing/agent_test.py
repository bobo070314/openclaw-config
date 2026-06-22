#!/usr/bin/env python
"""
agent-testing v0.2.0 — End-to-End Test Runner

Auto-detects the test framework in the target directory, runs tests,
and reports results with timing and coverage summary.

Supported frameworks (auto-detected):
  - pytest (Python)
  - vitest / jest (Node.js/TypeScript)
  - cargo test (Rust)
  - go test (Go)

Usage:
    python agent_test.py <project-dir> [test-pattern] [--framework pytest|vitest|...]

Examples:
    python agent_test.py D:/project/myapp
    python agent_test.py D:/project/myapp "test_auth"
    python agent_test.py D:/project/myapp --framework pytest
"""

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path


CST = timezone(timedelta(hours=8))


# ─── framework detection ───────────────────────────────────────────────
def detect_framework(project_dir: Path) -> str | None:
    """Auto-detect the test framework based on project files."""
    checks = [
        # (file_or_dir, framework_name)
        (project_dir / "pytest.ini", "pytest"),
        (project_dir / "pyproject.toml", "pytest"),
        (project_dir / "setup.cfg", "pytest"),
        (project_dir / "vitest.config.ts", "vitest"),
        (project_dir / "vitest.config.js", "vitest"),
        (project_dir / "jest.config.ts", "jest"),
        (project_dir / "jest.config.js", "jest"),
        (project_dir / "jest.config.json", "jest"),
        (project_dir / "Cargo.toml", "cargo"),
        (project_dir / "go.mod", "go"),
    ]

    for path, fw in checks:
        if path.exists():
            # For pyproject.toml, verify it actually has pytest config
            if path.name == "pyproject.toml":
                try:
                    content = path.read_text(encoding="utf-8", errors="replace")
                    if "[tool.pytest" in content or "pytest" in content:
                        return "pytest"
                except Exception:
                    pass
                continue
            if path.name == "setup.cfg":
                try:
                    content = path.read_text(encoding="utf-8", errors="replace")
                    if "[tool:pytest" not in content and "[pytest" not in content:
                        continue
                except Exception:
                    pass
            return fw

    # Fallback: check package.json for test scripts
    pkj = project_dir / "package.json"
    if pkj.exists():
        try:
            pkg = json.loads(pkj.read_text(encoding="utf-8"))
            scripts = pkg.get("scripts", {})
            deps = {**pkg.get("devDependencies", {}), **pkg.get("dependencies", {})}
            if "vitest" in str(scripts) or "vitest" in deps:
                return "vitest"
            if "jest" in str(scripts) or "jest" in deps:
                return "jest"
        except Exception:
            pass

    # Final fallback: check for test directories
    test_dirs = ["tests", "test", "__tests__", "spec"]
    for td in test_dirs:
        if (project_dir / td).is_dir():
            # check file extensions
            py_files = list((project_dir / td).glob("test_*.py")) + list((project_dir / td).glob("*_test.py"))
            ts_files = list((project_dir / td).glob("*.test.ts")) + list((project_dir / td).glob("*.spec.ts"))
            if py_files:
                return "pytest"
            if ts_files:
                return "vitest"  # default vitest over jest for modern TS
    return None


# ─── test runners ──────────────────────────────────────────────────────
def run_pytest(project_dir: Path, pattern: str = "") -> dict:
    """Run pytest and return results."""
    cmd = ["pytest", "-v", "--tb=short"]
    if pattern:
        cmd.extend(["-k", pattern])
    return _run_cmd(cmd, project_dir, "pytest")


def run_vitest(project_dir: Path, pattern: str = "") -> dict:
    """Run vitest and return results."""
    cmd = ["npx", "vitest", "run", "--reporter=verbose"]
    if pattern:
        cmd.extend(["-t", pattern])
    return _run_cmd(cmd, project_dir, "vitest")


def run_jest(project_dir: Path, pattern: str = "") -> dict:
    """Run jest and return results."""
    cmd = ["npx", "jest", "--verbose"]
    if pattern:
        cmd.extend(["-t", pattern])
    return _run_cmd(cmd, project_dir, "jest")


def run_cargo(project_dir: Path, pattern: str = "") -> dict:
    cmd = ["cargo", "test"]
    if pattern:
        cmd.append(pattern)
    return _run_cmd(cmd, project_dir, "cargo")


def run_go(project_dir: Path, pattern: str = "") -> dict:
    cmd = ["go", "test", "./...", "-v"]
    if pattern:
        cmd.extend(["-run", pattern])
    return _run_cmd(cmd, project_dir, "go")


def _run_cmd(cmd: list[str], cwd: Path, framework: str) -> dict:
    """Execute a test command and capture results."""
    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=120,
            env={**os.environ, "PYTHONIOENCODING": "utf-8", "CI": "true"},
        )
        elapsed = time.time() - start
        return {
            "framework": framework,
            "command": " ".join(cmd),
            "exit_code": result.returncode,
            "duration_s": round(elapsed, 2),
            "stdout": result.stdout[-4000:] if len(result.stdout) > 4000 else result.stdout,
            "stderr": result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {
            "framework": framework,
            "command": " ".join(cmd),
            "exit_code": -1,
            "duration_s": round(time.time() - start, 2),
            "stdout": "",
            "stderr": "TIMEOUT: test run exceeded 120 seconds",
        }
    except FileNotFoundError:
        return {
            "framework": framework,
            "command": " ".join(cmd),
            "exit_code": -2,
            "duration_s": 0,
            "stdout": "",
            "stderr": f"ERROR: {cmd[0]} not found. Is it installed?",
        }


# ─── result parsing ────────────────────────────────────────────────────
def parse_results(result: dict) -> dict:
    """Parse test output to extract pass/fail/skip counts."""
    summary = {"passed": 0, "failed": 0, "skipped": 0, "total": 0, "errors": []}
    if result["exit_code"] < 0:
        summary["errors"].append(result["stderr"])
        return summary

    stdout = result["stdout"]
    stderr = result["stderr"]

    # pytest pattern
    m = re.search(r"(\d+)\s+passed", stdout, re.IGNORECASE)
    if m:
        summary["passed"] = int(m.group(1))
    m = re.search(r"(\d+)\s+failed", stdout, re.IGNORECASE)
    if m:
        summary["failed"] = int(m.group(1))
    m = re.search(r"(\d+)\s+skipped", stdout, re.IGNORECASE)
    if m:
        summary["skipped"] = int(m.group(1))

    # jest/vitest pattern: "Tests: 5 passed, 2 failed, 1 skipped, 8 total"
    m = re.search(r"Tests:\s*(.+)$", stdout, re.MULTILINE | re.IGNORECASE)
    if m:
        detail = m.group(1)
        for part in detail.split(","):
            part = part.strip()
            pm = re.match(r"(\d+)\s+passed", part, re.IGNORECASE)
            fm = re.match(r"(\d+)\s+failed", part, re.IGNORECASE)
            sm = re.match(r"(\d+)\s+skipped", part, re.IGNORECASE)
            tm = re.match(r"(\d+)\s+total", part, re.IGNORECASE)
            if pm:
                summary["passed"] = int(pm.group(1))
            if fm:
                summary["failed"] = int(fm.group(1))
            if sm:
                summary["skipped"] = int(sm.group(1))
            if tm:
                summary["total"] = int(tm.group(1))

    # cargo test: "test result: ok. 5 passed; 0 failed; 1 ignored"
    m = re.search(r"test result:\s*(.+)", stdout, re.IGNORECASE)
    if m:
        detail = m.group(1)
        pm = re.search(r"(\d+)\s+passed", detail)
        fm = re.search(r"(\d+)\s+failed", detail)
        sm = re.search(r"(\d+)\s+ignored", detail)
        if pm:
            summary["passed"] = int(pm.group(1))
        if fm:
            summary["failed"] = int(fm.group(1))
        if sm:
            summary["skipped"] = int(sm.group(1))

    # go test: count lines with --- PASS / --- FAIL / --- SKIP
    pass_count = stdout.count("--- PASS:")
    fail_count = stdout.count("--- FAIL:")
    skip_count = stdout.count("--- SKIP:")
    if pass_count or fail_count or skip_count:
        summary["passed"] = max(summary["passed"], pass_count)
        summary["failed"] = max(summary["failed"], fail_count)
        summary["skipped"] = max(summary["skipped"], skip_count)

    summary["total"] = summary["passed"] + summary["failed"] + summary["skipped"]

    # collect failure lines
    for line in (stdout + stderr).splitlines():
        if "FAIL" in line or "Error" in line or "error" in line:
            s = line.strip()
            if s and len(s) > 5:
                summary["errors"].append(s[:200])

    if len(summary["errors"]) > 20:
        summary["errors"] = summary["errors"][:20]

    return summary


# ─── main ──────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: agent-testing <project-dir> [test-pattern] [--framework name]", file=sys.stderr)
        sys.exit(1)

    project_dir = Path(sys.argv[1]).resolve()
    pattern = ""
    framework_override = None

    # Parse remaining args
    for i, arg in enumerate(sys.argv[2:], start=2):
        if arg == "--framework" and i + 1 < len(sys.argv):
            framework_override = sys.argv[i + 1]
        elif not arg.startswith("--") and not framework_override:
            pattern = arg
        elif arg == "--framework":
            continue  # skip, value handled above

    if not project_dir.exists():
        print(f"ERROR: Project directory not found: {project_dir}", file=sys.stderr)
        sys.exit(1)

    framework = framework_override or detect_framework(project_dir)

    runners = {
        "pytest": run_pytest,
        "vitest": run_vitest,
        "jest": run_jest,
        "cargo": run_cargo,
        "go": run_go,
    }

    if framework not in runners:
        print(f"ERROR: No test framework detected in {project_dir}", file=sys.stderr)
        print("Supported: pytest, vitest, jest, cargo, go", file=sys.stderr)
        print("Use --framework to specify manually.", file=sys.stderr)
        sys.exit(1)

    ts = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 60)
    print("  Agent Testing Suite v0.2.0")
    print("=" * 60)
    print(f"  Project   : {project_dir}")
    print(f"  Framework : {framework}")
    print(f"  Pattern   : {pattern or '(all)'}")
    print(f"  Time      : {ts}")
    print()

    runner = runners[framework]
    result = runner(project_dir, pattern)
    summary = parse_results(result)

    # Output
    if result["stderr"] and result["exit_code"] != 0:
        print("--- STDERR ---")
        print(result["stderr"][:1000])
        print()

    if summary["total"] > 0:
        print("--- RESULTS ---")
        print(f"  Total   : {summary['total']}")
        print(f"  Passed  : {summary['passed']} ({_pct(summary['passed'], summary['total'])})")
        print(f"  Failed  : {summary['failed']} ({_pct(summary['failed'], summary['total'])})")
        print(f"  Skipped : {summary['skipped']}")
        print(f"  Duration: {result['duration_s']}s")
        if summary["errors"]:
            print()
            print("--- ISSUES ---")
            for e in summary["errors"][:10]:
                print(f"  - {e}")
    else:
        print("--- RAW OUTPUT (tail) ---")
        print(result["stdout"][-2000:])

    print()
    sys.exit(0 if summary["failed"] == 0 and result["exit_code"] >= 0 else 1)


def _pct(part: int, total: int) -> str:
    if total == 0:
        return "N/A"
    return f"{part / total * 100:.0f}%"


if __name__ == "__main__":
    main()
