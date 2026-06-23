---
name: token-saver
description: Command output smart compressor — saves 60-90% tokens on long output
version: 0.1.0
category: optimization
enabled: true
---

# token-saver v0.1.0

Intercepts long command outputs, keeps head+tail+sample, replaces the middle with stats.

## Usage
```bash
python skills/token-saver/run.py git log --oneline -100
python skills/token-saver/run.py npm audit
```

## Integration
Wrap any subprocess call:
```python
subprocess.run(["python", "skills/token-saver/run.py", "original", "command", "args"])
```
