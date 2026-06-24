---
name: config-diff
version: 0.2.0
author: OpenClaw-Foreign
description: config-diff v0.2.0 — Compare config files across environments.
permissions: []
---

# config-diff

config-diff v0.2.0 — Compare config files across environments.

Usage:
  python run.py --file .env --against .env.example
  python run.py --file docker-compose.yml --against docker-compose.prod.yml
  python run.py --dry-run --json --version

## 使用方法

```bash
python run.py [参数]
```

## 参数说明

- `--file`: Primary config file
- `--against`: Config to compare against
- `--dry-run`: 
- `--json`: 
- `--version`: 

## 注意事项

- 符合 OpenClaw skill v0.2.0 规范
- 禁止执行破坏性操作
