#!/usr/bin/env python
"""
sandbox-test — A deliberately destructive skill to test sandbox isolation.
This should NOT be able to harm the host filesystem.
"""
import os

# === V0.2.0 CLI STANDARD (auto-injected, do not remove) ===
VERSION = "0.2.0"
SKILL_NAME = "sandbox-test"
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
import argparse


def test_read_only():
    """Try to create a file at root level (should fail)."""
    try:
        with open("/should_not_exist_test_file.txt", "w") as f:
            f.write("if this works, sandbox is BROKEN")
        print("[DANGER] Wrote to root filesystem! SANDBOX FAILED!")
        return False
    except PermissionError:
        print("[SAFE] Permission denied - sandbox working")
        return True
    except OSError as e:
        print(f"[SAFE] OS error: {e} - sandbox likely working")
        return True


def test_delete_skill():
    """Try to delete the skill's own directory (should fail in sandbox)."""
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        target = os.path.join(skill_dir, "run.py")
        os.remove(target)
        print("[DANGER] Deleted own run.py! SANDBOX FAILED!")
        return False
    except PermissionError:
        print("[SAFE] Cannot delete own file in sandbox - working")
        return True
    except OSError as e:
        print(f"[SAFE] OS error: {e}")
        return True


def test_list_system():
    """Try to list /etc."""
    try:
        etc_contents = os.listdir("/etc") if os.path.exists("/etc") else []
        print(f"[INFO] /etc has {len(etc_contents)} entries (listing in sandbox)")
        return True
    except PermissionError:
        print("[SAFE] Cannot access /etc")
        return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--destructive", action="store_true", help="Run destructive tests")
    args = parser.parse_args()

    print("=" * 60)
    print("SANDBOX ISOLATION TEST")
    print("=" * 60)

    results = {}

    results["read_only"] = test_read_only()
    if args.destructive:
        results["delete_skill"] = test_delete_skill()
    results["list_system"] = test_list_system()

    print("\n" + "=" * 60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    in_sandbox = os.environ.get("SANDBOX_ROOT") is not None
    print(f"RESULTS: {passed}/{total} tests passed | SANDBOX_MODE={in_sandbox}")
    if passed == total:
        print("SANDBOX: SECURE [PASS]")
    else:
        print("SANDBOX: VULNERABLE [FAIL]")
    print("=" * 60)

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
