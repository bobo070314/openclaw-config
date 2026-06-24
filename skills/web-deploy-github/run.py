#!/usr/bin/env python3
"""
web-deploy-github v0.2.0 — Static Site Deployer
=================================================
Deploys a static site (build dir or single HTML) to GitHub Pages.
Supports: npm projects, plain HTML, custom domains.

Usage:
  python run.py deploy --dir ./out --repo user/repo
  python run.py deploy --file index.html --repo user/repo
  python run.py status --repo user/repo
  python run.py list --repo user/repo
"""
import argparse
import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime, timezone

VERSION = "0.2.0"
SKILL_NAME = "web-deploy-github"


def safe_run(cmd, cwd=None, timeout=60):
    """Run command safely with utf-8 encoding."""
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=cwd,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def check_gh_cli():
    """Check if GitHub CLI is installed."""
    rc, stdout, _ = safe_run(["gh", "--version"], timeout=10)
    return rc == 0


def check_git_repo(path):
    """Check if a path is a git repo."""
    rc, _, _ = safe_run(["git", "rev-parse", "--git-dir"], cwd=path, timeout=10)
    return rc == 0


def check_pages_status(repo):
    """Check GitHub Pages deployment status."""
    if check_gh_cli():
        rc, stdout, stderr = safe_run(["gh", "api", f"/repos/{repo}/pages"], timeout=15)
        if rc == 0:
            try:
                return json.loads(stdout)
            except json.JSONDecodeError:
                pass
        return {"error": stderr.strip() or "Failed to fetch Pages status"}
    return {"error": "gh CLI not found. Install: winget install GitHub.cli"}


def list_deployments(repo):
    """List recent deployments."""
    if check_gh_cli():
        rc, stdout, stderr = safe_run(
            ["gh", "api", f"/repos/{repo}/deployments?per_page=10"],
            timeout=15,
        )
        if rc == 0:
            try:
                deployments = json.loads(stdout)
                return [
                    {
                        "id": d["id"],
                        "ref": d.get("ref", ""),
                        "env": d.get("environment", ""),
                        "created_at": d.get("created_at", ""),
                    }
                    for d in deployments
                ]
            except json.JSONDecodeError:
                pass
        return {"error": stderr.strip() or "Failed to fetch deployments"}
    return {"error": "gh CLI not found"}


def find_build_dir(path, auto_detect=True):
    """Auto-detect common build output directories."""
    candidates = ["out", "dist", "build", ".next/out", "public", "_site"]
    for c in candidates:
        candidate = path / c
        if candidate.exists() and candidate.is_dir():
            # Check for index.html
            if (candidate / "index.html").exists():
                return candidate
    return None


def build_npm_project(path):
    """Run npm build on a project."""
    if not (path / "package.json").exists():
        return False, "No package.json found"

    rc, stdout, stderr = safe_run(["npm", "install"], cwd=path, timeout=120)
    if rc != 0:
        return False, f"npm install failed: {stderr[:200]}"

    rc, stdout, stderr = safe_run(["npm", "run", "build"], cwd=path, timeout=300)
    if rc != 0:
        return False, f"npm run build failed: {stderr[:200]}"

    return True, f"Build completed. Output:\n{stdout[-500:]}"


def deploy_to_pages(source_dir, repo, branch="gh-pages", message=None):
    """Deploy a directory to GitHub Pages using gh-pages pattern."""
    source_path = Path(source_dir)
    if not source_path.exists():
        return False, f"Source directory not found: {source_dir}"

    index_html = source_path / "index.html"
    if not index_html.exists():
        return False, f"No index.html found in {source_dir}"

    msg = message or f"Deploy {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}"

    # Strategy: use git subtree or orphan branch push
    # Clone temp, copy files, push
    import tempfile
    import shutil

    tmp_dir = Path(tempfile.mkdtemp(prefix="web-deploy-"))

    try:
        # Clone repo
        rc, stdout, stderr = safe_run(
            ["git", "clone", f"git@github.com:{repo}.git", "--single-branch", "--branch", branch, str(tmp_dir)],
            timeout=60,
        )
        if rc != 0:
            # Try creating orphan branch
            rc, stdout, stderr = safe_run(
                ["git", "clone", f"git@github.com:{repo}.git", "--single-branch", str(tmp_dir)],
                timeout=60,
            )
            if rc != 0:
                return False, f"Failed to clone repo: {stderr[:200]}"

        working = tmp_dir

        # If gh-pages doesn't exist, create orphan
        rc, _, _ = safe_run(["git", "rev-parse", "--verify", branch], cwd=working, timeout=10)
        if rc != 0:
            safe_run(["git", "checkout", "--orphan", branch], cwd=working, timeout=10)

        # Remove old files (keep .git)
        for item in working.iterdir():
            if item.name == ".git":
                continue
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

        # Copy new files
        for item in source_path.iterdir():
            dest = working / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

        # Git add + commit + push
        safe_run(["git", "add", "-A"], cwd=working, timeout=10)
        safe_run(["git", "commit", "-m", msg, "--allow-empty"], cwd=working, timeout=10)
        rc, stdout, stderr = safe_run(["git", "push", "origin", branch, "--force"], cwd=working, timeout=60)

        if rc == 0:
            return True, {
                "branch": branch,
                "repo": repo,
                "url": f"https://{repo.split('/')[0]}.github.io/{repo.split('/')[1]}",
                "message": msg,
            }
        else:
            return False, f"Push failed: {stderr[:200]}"

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def deploy_single_file(file_path, repo, branch="gh-pages"):
    """Deploy a single HTML file to Pages."""
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="web-deploy-file-"))
    dest = tmp / "index.html"
    import shutil
    shutil.copy(file_path, dest)
    result = deploy_to_pages(tmp, repo, branch)
    shutil.rmtree(tmp, ignore_errors=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=f"web-deploy-github v{VERSION}")
    sub = parser.add_subparsers(dest="action", help="Actions: deploy, status, list, build")

    # deploy
    deploy_parser = sub.add_parser("deploy", help="Deploy to GitHub Pages")
    deploy_parser.add_argument("--dir", help="Directory to deploy (build output)")
    deploy_parser.add_argument("--file", help="Single HTML file to deploy")
    deploy_parser.add_argument("--repo", required=True, help="GitHub repo (user/repo)")
    deploy_parser.add_argument("--branch", default="gh-pages", help="Deploy branch (default: gh-pages)")
    deploy_parser.add_argument("--auto-build", action="store_true", help="Auto-detect and run npm build")
    deploy_parser.add_argument("--message", "-m", help="Deploy message")

    # status
    status_parser = sub.add_parser("status", help="Check Pages deployment status")
    status_parser.add_argument("--repo", required=True, help="GitHub repo (user/repo)")

    # list
    list_parser = sub.add_parser("list", help="List recent deployments")
    list_parser.add_argument("--repo", required=True, help="GitHub repo (user/repo)")

    # build
    build_parser = sub.add_parser("build", help="Build npm project")
    build_parser.add_argument("--path", default=".", help="Project path")

    # Global flags
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    parser.add_argument("--version", action="store_true", help="Show version")

    args = parser.parse_args()

    if args.version:
        print(json.dumps({"skill": SKILL_NAME, "version": VERSION, "status": "live"}, indent=2))
        return

    # --json without action
    if args.json and not args.action:
        info = {
            "skill": SKILL_NAME,
            "version": VERSION,
            "status": "live",
            "features": ["deploy", "status", "list", "build"],
            "requires": ["git", "npm (for auto-build)", "gh CLI (for status/list)"],
        }
        print(json.dumps(info, indent=2))
        return

    # Actions
    if args.action == "status":
        result = check_pages_status(args.repo)
        output = {"action": "status", "repo": args.repo, "result": result}
        print(json.dumps(output, indent=2) if args.json else json.dumps(output, indent=2))

    elif args.action == "list":
        result = list_deployments(args.repo)
        output = {"action": "list", "repo": args.repo, "deployments": result}
        print(json.dumps(output, indent=2) if args.json else json.dumps(output, indent=2))

    elif args.action == "build":
        path = Path(args.path).resolve()
        ok, msg = build_npm_project(path)
        output = {"action": "build", "path": str(path), "success": ok, "message": msg}
        print(json.dumps(output, indent=2) if args.json else json.dumps(output, indent=2))
        if not ok:
            sys.exit(1)

    elif args.action == "deploy":
        if args.dry_run:
            source = args.dir or args.file or "."
            output = {
                "action": "deploy",
                "repo": args.repo,
                "branch": args.branch,
                "source": source,
                "dry_run": True,
            }
            print(json.dumps(output, indent=2))
            return

        # Determine source
        source_dir = None
        if args.file:
            source_path = Path(args.file)
            if not source_path.exists():
                print(json.dumps({"error": f"File not found: {args.file}"}, indent=2))
                sys.exit(1)
            ok, result = deploy_single_file(source_path, args.repo, args.branch)
        elif args.dir:
            source_dir = Path(args.dir)
        elif args.auto_build:
            path = Path(".").resolve()
            ok, msg = build_npm_project(path)
            if not ok:
                print(json.dumps({"error": msg}, indent=2))
                sys.exit(1)
            source_dir = find_build_dir(path)
            if not source_dir:
                print(json.dumps({"error": "Could not auto-detect build directory"}, indent=2))
                sys.exit(1)
        else:
            # Try auto-detect
            path = Path(".").resolve()
            source_dir = find_build_dir(path)
            if not source_dir:
                print(json.dumps({"error": "No build dir found. Use --dir or --file"}), indent=2)
                sys.exit(1)

        if source_dir and not args.file:
            ok, result = deploy_to_pages(source_dir, args.repo, args.branch, args.message)

        if ok:
            output = {"action": "deploy", "success": True, "result": result}
            print(json.dumps(output, indent=2))
        else:
            output = {"action": "deploy", "success": False, "error": result}
            print(json.dumps(output, indent=2))
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
