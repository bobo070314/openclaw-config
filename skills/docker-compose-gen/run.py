#!/usr/bin/env python3.
"""docker-compose-gen v0.2.0 — Generate docker-compose.yml from a service spec.

Usage:
  python run.py --services web,db,redis
  python run.py --template node-postgres
  python run.py --dry-run --json --version
"""

import argparse
import json
import sys

__version__ = "0.2.0"

TEMPLATES = {
    "node-postgres": {
        "version": "3.9",
        "services": {
            "web": {"build": ".", "ports": ["3000:3000"], "depends_on": ["db"], "environment": ["DATABASE_URL=postgresql://user:pass@db:5432/app"]},
            "db": {"image": "postgres:16-alpine", "ports": ["5432:5432"], "environment": ["POSTGRES_USER=user", "POSTGRES_PASSWORD=pass", "POSTGRES_DB=app"], "volumes": ["pgdata:/var/lib/postgresql/data"]},
        },
        "volumes": {"pgdata": None},
    },
    "python-fastapi": {
        "version": "3.9",
        "services": {
            "api": {"build": ".", "ports": ["8000:8000"], "depends_on": ["db", "redis"], "environment": ["DATABASE_URL=postgresql://user:pass@db:5432/app", "REDIS_URL=redis://redis:6379"]},
            "db": {"image": "postgres:16-alpine", "ports": ["5432:5432"], "environment": ["POSTGRES_USER=user", "POSTGRES_PASSWORD=pass", "POSTGRES_DB=app"], "volumes": ["pgdata:/var/lib/postgresql/data"]},
            "redis": {"image": "redis:7-alpine", "ports": ["6379:6379"]},
        },
        "volumes": {"pgdata": None},
    },
    "go-api": {
        "version": "3.9",
        "services": {
            "api": {"build": ".", "ports": ["8080:8080"], "depends_on": ["db"], "environment": ["DB_HOST=db", "DB_PORT=5432"]},
            "db": {"image": "postgres:16-alpine", "ports": ["5432:5432"], "environment": ["POSTGRES_USER=user", "POSTGRES_PASSWORD=pass", "POSTGRES_DB=app"], "volumes": ["pgdata:/var/lib/postgresql/data"]},
        },
        "volumes": {"pgdata": None},
    },
    "static-site": {
        "version": "3.9",
        "services": {
            "web": {"build": ".", "ports": ["80:80"]},
        },
    },
}


def generate_services(services: list[str]) -> dict:
    """Generate a docker-compose from a list of service names."""
    if isinstance(services, str):
        services = [s.strip() for s in services.split(",")]

    compose = {"version": "3.9", "services": {}, "volumes": {}}

    for svc in services:
        svc = svc.lower().strip()
        if svc in ("web", "app", "api"):
            compose["services"][svc] = {"build": ".", "ports": ["3000:3000"]}
        elif svc in ("db", "database", "postgres", "postgresql"):
            compose["services"]["db"] = {"image": "postgres:16-alpine", "ports": ["5432:5432"], "environment": ["POSTGRES_USER=app", "POSTGRES_PASSWORD=changeme", "POSTGRES_DB=app"], "volumes": ["pgdata:/var/lib/postgresql/data"]}
            compose["volumes"]["pgdata"] = None
        elif svc == "redis":
            compose["services"]["redis"] = {"image": "redis:7-alpine", "ports": ["6379:6379"]}
        elif svc == "nginx":
            compose["services"]["nginx"] = {"image": "nginx:alpine", "ports": ["80:80", "443:443"], "volumes": ["./nginx.conf:/etc/nginx/nginx.conf:ro"]}
        elif svc == "mongo":
            compose["services"]["mongo"] = {"image": "mongo:7", "ports": ["27017:27017"], "volumes": ["mongodata:/data/db"]}
            compose["volumes"]["mongodata"] = None

    return compose


def main():
    parser = argparse.ArgumentParser(description="Docker Compose Generator v0.2.0")
    parser.add_argument("--services", help="Comma-separated service names (web,db,redis)")
    parser.add_argument("--template", choices=list(TEMPLATES.keys()), help="Template name")
    parser.add_argument("--list-templates", action="store_true", help="Show available templates")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print(__version__)
        return

    if args.list_templates:
        for name, tmpl in TEMPLATES.items():
            svcs = list(tmpl["services"].keys())
            print(f"  {name}: {', '.join(svcs)}")
        return

    if args.dry_run:
        result = {"dry_run": True, "services": args.services, "template": args.template, "actions": ["validate", "compose", "output"]}
        print(json.dumps(result) if args.json else "🐳 Docker Compose Generator dry-run — ready")
        return

    if args.template:
        compose = TEMPLATES[args.template]
    elif args.services:
        compose = generate_services(args.services)
    else:
        parser.print_help()
        return

    output = json.dumps(compose, indent=2) if args.json else yaml_dump(compose)

    if args.json:
        print(output)
    elif args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"✅ Written docker-compose.yml → {args.output}")
    else:
        print(output)


def yaml_dump(compose: dict) -> str:
    """Minimal YAML dumper (no pyyaml dependency for simple outputs)."""
    lines = ['version: "3.9"', "", "services:"]
    for name, svc in compose.get("services", {}).items():
        lines.append(f"  {name}:")
        if "build" in svc:
            lines.append(f'    build: {svc["build"] if isinstance(svc["build"], str) else "."}')
        if "image" in svc:
            lines.append(f'    image: {svc["image"]}')
        if "ports" in svc:
            for p in svc["ports"]:
                lines.append(f'    ports: ["{p}"]')
        if "depends_on" in svc:
            lines.append(f"    depends_on: {json.dumps(svc['depends_on'])}")
        if "environment" in svc:
            lines.append("    environment:")
            for env in svc["environment"]:
                lines.append(f"      - {env}")
        if "volumes" in svc:
            lines.append("    volumes:")
            for v in svc["volumes"]:
                lines.append(f"      - {v}")
        lines.append("")

    if "volumes" in compose and compose["volumes"]:
        lines.append("volumes:")
        for vol_name, driver in compose["volumes"].items():
            lines.append(f"  {vol_name}:")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
