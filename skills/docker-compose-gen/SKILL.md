---
name: docker-compose-gen
version: 0.2.0
author: OpenClaw-Foreign
description: docker-compose-gen v0.2.0 — Generate docker-compose.yml from a service spec.
permissions: []
---

# docker-compose-gen

docker-compose-gen v0.2.0 — Generate docker-compose.yml from a service spec.

Usage:
  python run.py --services web,db,redis
  python run.py --template node-postgres
  python run.py --dry-run --json --version

## 使用方法

```bash
python run.py [参数]
```

## 参数说明

- `--services`: Comma-separated service names (web,db,redis)
- `--template`: Template name
- `--list-templates`: Show available templates
- `--output`: Output file path
- `--dry-run`: 
- `--json`: 
- `--version`: 

## 注意事项

- 符合 OpenClaw skill v0.2.0 规范
- 禁止执行破坏性操作
