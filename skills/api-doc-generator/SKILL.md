---
name: api-doc-generator
version: 0.2.0
author: OpenClaw-Foreign
description: api-doc-generator v0.2.0 — Auto-generate API docs from source code.
permissions: []
---

# api-doc-generator

api-doc-generator v0.2.0 — Auto-generate API docs from source code.

Supports OpenAPI 3.0 and Markdown output from Python/Node.js/Go source.

Usage:
  python run.py --path ./src --format openapi
  python run.py --path ./routes --format markdown --output api.md
  python run.py --dry-run --json --version

## 使用方法

```bash
python run.py [参数]
```

## 参数说明

- `--path`: Source code directory
- `--format`: Output format
- `--output`: Output file path
- `--title`: API title
- `--dry-run`: 
- `--json`: 
- `--version`: 

## 注意事项

- 符合 OpenClaw skill v0.2.0 规范
- 禁止执行破坏性操作
