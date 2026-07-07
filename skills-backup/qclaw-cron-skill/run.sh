#!/bin/bash
# OpenClaw skill runner
cd "$(dirname "$0")"
exec python run.py "$@"
