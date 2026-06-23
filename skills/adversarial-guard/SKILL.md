---
name: adversarial-guard
version: "0.2.0"
description: "Prompt injection firewall — L1 regex + L2 structural + L3 intent classifier"
enabled: true
category: security
tags: [security, firewall, prompt-injection, adversarial]
---

# 🛡️ adversarial-guard

三层防御的 Prompt injection 防火墙。

## 防御层级
| 层级 | 机制 | 拦截能力 |
|------|------|----------|
| L1 | 正则模式匹配 | 已知注入/DAN/Drop Table/rm -rf |
| L2 | 结构分析 | Base64混淆、Unicode混淆、Token泄露 |
| L3 | 意图分类 | prompt_leak/role_override/command_injection/data_exfil/jailbreak |

## 用法
```bash
python adversarial-guard/run.py --check "text"        # 扫描
python adversarial-guard/run.py --inject-test         # 自测
python adversarial-guard/run.py --json --check "text" # JSON
```
