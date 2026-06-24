#!/usr/bin/env python3.
"""config-diff v0.2.0 — Compare config files across environments.

Usage:
  python run.py --file .env --against .env.example
  python run.py --file docker-compose.yml --against docker-compose.prod.yml
  python run.py --dry-run --json --version
"""

import argparse
import json
import sys
from pathlib import Path

__version__ = "0.2.0"


def load_config(filepath: str) -> dict:
    """Load a config file as key-value pairs."""
    path = Path(filepath)
    if not path.exists():
        return {"__error__": f"File not found: {filepath}"}

    content = path.read_text(encoding="utf-8", errors="replace")
    result = {}

    # .env format
    if path.suffix in (".env", ".example") or path.name.startswith("."):
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, val = line.partition("=")
                result[key.strip()] = val.strip().strip("\"'")

    # YAML (simple top-level)
    elif path.suffix in (".yml", ".yaml"):
        try:
            import yaml

            result = yaml.safe_load(content) or {}
        except ImportError:
            # Simple line-based fallback
            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line and not line.startswith(" "):
                    key, _, val = line.partition(":")
                    result[key.strip()] = val.strip()

    # JSON
    elif path.suffix == ".json":
        result = json.loads(content)

    return result


def diff_configs(file1: str, file2: str) -> dict:
    c1 = load_config(file1)
    c2 = load_config(file2)

    if "__error__" in c1 or "__error__" in c2:
        return {"error": c1.get("__error__") or c2.get("__error__")}

    all_keys = set(c1.keys()) | set(c2.keys())
    only_in_1 = [k for k in c1 if k not in c2]
    only_in_2 = [k for k in c2 if k not in c1]
    changed = []
    same = []

    for k in sorted(all_keys):
        if k in c1 and k in c2:
            v1 = str(c1[k])
            v2 = str(c2[k])
            if v1 != v2:
                # Mask sensitive values
                if any(s in k.lower() for s in ["secret", "password", "token", "key", "api"]):
                    v1 = v1[:3] + "***"
                    v2 = v2[:3] + "***"
                changed.append({"key": k, "from": v1, "to": v2})
            else:
                same.append(k)

    return {
        "file1": file1,
        "file2": file2,
        "keys_in_both": len(same) + len(changed),
        "keys_only_in_1": len(only_in_1),
        "keys_only_in_2": len(only_in_2),
        "keys_unchanged": len(same),
        "keys_changed": len(changed),
        "only_in_first": only_in_1,
        "only_in_second": only_in_2,
        "changed": changed,
    }


def main():
    # Handle --version/--dry-run/--json before argparse required checks
    if "--version" in sys.argv:
        print(__version__)
        return

    if "--dry-run" in sys.argv or "--json" in sys.argv:
        flags = [a for a in sys.argv[1:] if a in ("--dry-run", "--json", "--version")]
        result = {"dry_run": "--dry-run" in flags, "file": None, "against": None, "actions": ["load", "diff", "report"]}
        print(json.dumps(result) if "--json" in flags else "\ud83d\udd0d Config Diff dry-run \u2014 ready")
        return

    parser = argparse.ArgumentParser(description="Config Diff v0.2.0")
    parser.add_argument("--file", required=True, help="Primary config file")
    parser.add_argument("--against", required=True, help="Config to compare against")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print(__version__)
        return

    if args.dry_run:
        result = {"dry_run": True, "file": args.file, "against": args.against, "actions": ["load", "diff", "report"]}
        print(json.dumps(result) if args.json else "🔍 Config Diff dry-run — ready")
        return

    result = diff_configs(Path(args.file).as_posix(), Path(args.against).as_posix())

    if "error" in result:
        print(f"❌ {result['error']}")
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n📊 Config Diff: {args.file} ↔ {args.against}")
        print(f"   {result['keys_unchanged']} unchanged  |  {result['keys_changed']} changed")
        print(f"   +{result['keys_only_in_2']} only in 2nd  |  -{result['keys_only_in_1']} only in 1st")

        if result["only_in_first"]:
            print(f"\n   ⚠️  Missing in {args.against}: {', '.join(result['only_in_first'][:10])}")
        if result["only_in_second"]:
            print(f"\n   ⚠️  Extra in {args.against}: {', '.join(result['only_in_second'][:10])}")
        if result["changed"]:
            print(f"\n   Changed keys:")
            for c in result["changed"][:15]:
                print(f"     {c['key']}: {c['from']} → {c['to']}")
            if len(result["changed"]) > 15:
                print(f"     ... and {len(result['changed']) - 15} more")


if __name__ == "__main__":
    main()
