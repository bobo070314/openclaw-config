#!/bin/bash
# add-setting-env v0.2.0 — delegates to Python
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python "$SCRIPT_DIR/env_validator.py" "$@"
