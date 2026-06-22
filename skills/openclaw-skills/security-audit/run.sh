#!/bin/bash
# security-audit v0.2.0 — delegates to Python
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python "$SCRIPT_DIR/security_audit.py" "$@"
