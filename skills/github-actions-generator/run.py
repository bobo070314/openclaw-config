#!/usr/bin/env python3
"""
github-actions-generator v0.2.0 — GitHub Actions Workflow Generator
====================================================================
Generates GitHub Actions workflow YAML from templates and parameter overrides.
Supports: CI (Node/Python/Go), Deploy (Pages/Vercel), Schedule (Cron).

Usage:
  python run.py --template ci --runtime node --node-version 20
  python run.py --template deploy-pages --branch main
  python run.py --template schedule --cron "0 9 * * *" --command "npm test"
  python run.py --json --list-templates
"""
import argparse
import json
import sys
import os
from pathlib import Path

VERSION = "0.2.0"

# ── Templates ─────────────────────────────────────
TEMPLATES = {
    "ci-node": {
        "name": "Node.js CI",
        "description": "Install deps, lint, test on Node.js",
        "yaml": """name: Node.js CI

on:
  push:
    branches: [{branch}]
  pull_request:
    branches: [{branch}]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [{node_version}]

    steps:
    - uses: actions/checkout@v4

    - name: Use Node.js ${{{{ matrix.node-version }}}}
      uses: actions/setup-node@v4
      with:
        node-version: ${{{{ matrix.node-version }}}}
        cache: '{pkg_manager}'

    - name: Install dependencies
      run: {install_cmd}

    - name: Lint
      run: {lint_cmd}

    - name: Test
      run: {test_cmd}
""",
    },
    "ci-python": {
        "name": "Python CI",
        "description": "Install deps, lint (ruff), test (pytest) on Python",
        "yaml": """name: Python CI

on:
  push:
    branches: [{branch}]
  pull_request:
    branches: [{branch}]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [{python_version}]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{{{ matrix.python-version }}}}
      uses: actions/setup-python@v5
      with:
        python-version: ${{{{ matrix.python-version }}}}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Lint with ruff
      run: ruff check .

    - name: Test with pytest
      run: pytest
""",
    },
    "ci-go": {
        "name": "Go CI",
        "description": "Build and test Go modules",
        "yaml": """name: Go CI

on:
  push:
    branches: [{branch}]
  pull_request:
    branches: [{branch}]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Go
      uses: actions/setup-go@v5
      with:
        go-version: '{go_version}'

    - name: Build
      run: go build -v ./...

    - name: Test
      run: go test -v ./...
""",
    },
    "deploy-pages": {
        "name": "Deploy to GitHub Pages",
        "description": "Build static site and deploy to Pages",
        "yaml": """name: Deploy to GitHub Pages

on:
  push:
    branches: [{branch}]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{{{ steps.deployment.outputs.page_url }}}}
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'

    - name: Install dependencies
      run: {install_cmd}

    - name: Build
      run: {build_cmd}

    - name: Setup Pages
      uses: actions/configure-pages@v5

    - name: Upload artifact
      uses: actions/upload-pages-artifact@v3
      with:
        path: '{build_dir}'

    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v4
""",
    },
    "schedule": {
        "name": "Scheduled Job",
        "description": "Run command on a cron schedule",
        "yaml": """name: Scheduled Job

on:
  schedule:
    - cron: '{cron}'
  workflow_dispatch:

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Run scheduled task
      run: {command}
""",
    },
}


def list_templates():
    """List available templates."""
    return {
        "templates": [
            {"id": tid, "name": t["name"], "description": t["description"]}
            for tid, t in TEMPLATES.items()
        ]
    }


def generate_workflow(args):
    """Generate workflow YAML from template and parameters."""
    template = TEMPLATES.get(args.template)
    if not template:
        return {"error": f"Unknown template: {args.template}", "available": list(TEMPLATES.keys())}

    # Build substitutions
    subs = {}
    subs["branch"] = args.branch or "main"
    subs["node_version"] = args.node_version or "20"
    subs["python_version"] = args.python_version or "3.12"
    subs["go_version"] = args.go_version or "1.22"
    subs["pkg_manager"] = args.pkg_manager or "npm"
    subs["install_cmd"] = args.install_cmd or "npm ci"
    subs["lint_cmd"] = args.lint_cmd or "npm run lint"
    subs["test_cmd"] = args.test_cmd or "npm test"
    subs["build_cmd"] = args.build_cmd or "npm run build"
    subs["build_dir"] = args.build_dir or "./out"
    subs["cron"] = args.cron or "0 9 * * *"
    subs["command"] = args.command or "echo 'Hello from scheduled job'"

    yaml = template["yaml"].format(**subs)

    workflow_name = f"github-actions-{args.template.replace('-', '_')}.yml"
    output_path = Path(args.output or ".")

    return {
        "template": args.template,
        "workflow_name": workflow_name,
        "yaml": yaml,
        "output": str(output_path / workflow_name),
    }


def main():
    parser = argparse.ArgumentParser(
        description="GitHub Actions Workflow Generator v{0}".format(VERSION),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Templates: " + ", ".join(TEMPLATES.keys()),
    )
    parser.add_argument("--template", "-t", help="Template to use")
    parser.add_argument("--list-templates", action="store_true", help="List available templates")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing file")
    parser.add_argument("--output", "-o", help="Output directory (default: cwd)")
    parser.add_argument("--version", action="store_true", help="Show version")

    # Template parameters
    parser.add_argument("--branch", help="Git branch (default: main)")
    parser.add_argument("--node-version", help="Node.js version (default: 20)")
    parser.add_argument("--python-version", help="Python version (default: 3.12)")
    parser.add_argument("--go-version", help="Go version (default: 1.22)")
    parser.add_argument("--pkg-manager", help="Package manager: npm/pnpm/yarn (default: npm)")
    parser.add_argument("--install-cmd", help="Install command (default: npm ci)")
    parser.add_argument("--lint-cmd", help="Lint command (default: npm run lint)")
    parser.add_argument("--test-cmd", help="Test command (default: npm test)")
    parser.add_argument("--build-cmd", help="Build command (default: npm run build)")
    parser.add_argument("--build-dir", help="Build output directory (default: ./out)")
    parser.add_argument("--cron", help="Cron expression (default: 0 9 * * *)")
    parser.add_argument("--command", help="Command to run (schedule template)")

    args = parser.parse_args()

    # Version
    if args.version:
        print(json.dumps({"skill": "github-actions-generator", "version": VERSION, "status": "live"}, indent=2))
        return

    # List templates
    if args.list_templates:
        result = list_templates()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("Available templates:\n")
            for t in result["templates"]:
                print(f"  {t['id']:<20} {t['name']:<25} {t['description']}")
        return

    # Generate
    if args.template:
        result = generate_workflow(args)
        if "error" in result:
            print(json.dumps(result, indent=2))
            sys.exit(1)

        if args.dry_run:
            result["dry_run"] = True
            print(json.dumps(result, indent=2))
            return

        # Write YAML file
        output_path = Path(result["output"])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("# Generated by github-actions-generator v{0}\n".format(VERSION) + result["yaml"])
        result["written"] = True
        print(json.dumps(result, indent=2))
        return

    # No action specified
    parser.print_help()


if __name__ == "__main__":
    main()
