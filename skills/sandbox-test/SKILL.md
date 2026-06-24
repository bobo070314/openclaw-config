---
name: sandbox-test
version: 0.2.0
author: OpenClaw-Foreign
description: sandbox-test — A deliberately destructive skill to test sandbox isolation.
permissions: []
---

# sandbox-test

sandbox-test — A deliberately destructive skill to test sandbox isolation.
This should NOT be able to harm the host filesystem.

## 使用方法

```bash
python run.py [参数]
```

## 参数说明

- `--destructive`: Run destructive tests

## 注意事项

- 符合 OpenClaw skill v0.2.0 规范
- 禁止执行破坏性操作
