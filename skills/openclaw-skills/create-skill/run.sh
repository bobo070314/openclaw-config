#!/bin/bash
# create-skill v0.2.0 — delegates to Python
# Usage: ./run.sh <skill-name> <description> [target-dir]
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python "$SCRIPT_DIR/create_skill.py" "$@"
