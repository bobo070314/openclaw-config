---
name: owl-vision
version: 1.0.0
author: OpenClaw-Foreign
description: Owl Vision
permissions: []
---

# Owl Vision

Local vision model for screen understanding. Runs fully offline via Moondream 2B.
Zero cloud API calls. Zero data leakage.

## Capabilities
- Screenshot analysis: describe UI, detect errors, extract text
- Six-column layout recognition (6-col architecture)
- Window / dialog / button identification
- Crash screen detection (causal-reasoner trigger)

## Usage
```bash
python run.py "What is on the screen?"
python run.py "Is there an error message?" --image path/to/screenshot.png
python run.py --json "Describe the UI layout"
```

## Dependencies
- `pip install moondream` (first run auto-installs)
- Model auto-downloaded on first use (moondream-2b-int8, ~1.5GB)
- CPU-compatible; no GPU required
- `pillow` for screenshot capture

## Integration
- `subconscious-daemon` hooks into this for auto-screenshot + analysis
- Detected errors -> `causal-reasoner` for root cause
- `adversarial-guard` screens visual injection attempts
