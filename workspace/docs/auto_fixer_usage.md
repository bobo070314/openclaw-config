# auto_fixer.py — Usage Guide

> **对应**: RFC-001-meta-autofix.md · v1.8.0
> **状态**: 候选代码（P0 — 仅分析，不执行）
> **接入条件**: 等待 v1.8.0 Go/No-Go 决策

---

## 文件位置

```
scripts/auto_fixer.py
```

未接入 `orchestrator.py`，纯独立文件。

---

## 核心函数

| 函数 | 输入 | 输出 | 用途 |
|---|---|---|---|
| `analyze_failures(eval_data)` | `latest_eval.json` dict 或 None | 失败归类 + 计数 | 读取 eval 报告，正则匹配 fail_reason |
| `select_strategy(analysis)` | `analyze_failures()` 的输出 | 策略 `S1/S2/S3/NONE` + confidence | 按失败类别占比选最优策略 |
| `apply_repair(strategy, target)` | `"S1"/"S2"/"S3"`, 文件名 | 模板文件路径或 None | 写入修复模板到 `configs/` |
| `should_rollback(pre, post)` | 修复前 pass_rate, 修复后 pass_rate | rollback: bool + 原因 | 修复恶化则触发回滚 |
| `log_fix_attempt(plan, result)` | 策略 plan + 执行结果 | 追加一行到 violations.jsonl | 审计日志 |

---

## 修复策略

| 策略 | 触发条件 | 模板源 | 写入位置 |
|---|---|---|---|
| S1 — 文件补全 | fail_reason 匹配 `(file\|missing\|no\s+such)` | S1_TEMPLATES | `configs/agent_chain.yaml` 或 `README.deliver.md` |
| S2 — 配置修正 | fail_reason 匹配 `(config\|invalid\|bad\|syntax\|parse)` 且未匹配 RBAC | S2_TEMPLATES | `configs/agent_chain.yaml` |
| S3 — RBAC 恢复 | fail_reason 匹配 `(rbac\|permission\|access\|denied\|forbidden\|unauthorized)` | S3_TEMPLATES | `configs/agent_chain.yaml`（含 default_roles） |

**匹配优先级**: FileMissing > RBACViolation > ConfigError > Unknown

---

## 模板扩展

模板字典定义在 `S1_TEMPLATES` / `S2_TEMPLATES` / `S3_TEMPLATES`（文件末尾）。添加新模板只需在这个字典里增加条目，`apply_repair()` 自动适配。

---

## P0 运行

```bash
cd D:\bobo\openclaw-foreign\workspace
python scripts/auto_fixer.py
```

输出 `status: ANALYZED` + analysis + plan。**不写入配置文件**，只写审计日志标记为 `analyzed_only`。

---

## 与 orchestrator 的集成点

未来合入时，在 `orchestrator.py` 的 rollback 之后、evolve 之前插入：

```python
from scripts.auto_fixer import analyze_failures, select_strategy, apply_repair, should_rollback

fix_result = apply_strategy(eval_data)
if fix_result and not should_rollback(pre_rate, post_rate)["rollback"]:
    # 修复成功，继续 pipeline
else:
    # 触发 auto_rollback.ps1
```
