# RFC-001: Meta-Agent Auto-Fix (v1.8.0)

> **状态**: DRAFT · 2026-07-04
> **北极星**: 先稳定进化，再开放自修复
> **依赖**: v1.7.2-bline-monitor-daemon (B-Line observation window)

---

## 1. 问题陈述

当前 Meta-Agent (`scripts/meta_agent.py`) 具备：
- 去重注入新 Hardcase ✅
- 分类轮换（4 类）✅
- 重复率告警/阻断 ✅
- 状态日志化 ✅

**缺失能力：** 当 pass_rate < 0.5 触发回滚时，系统仅执行回滚，但**不分析失败原因，也不修复根因**。

即：系统能感知自己病了，知道吃后悔药，但不知道自己为什么病。

---

## 2. 设计目标

### 2.1 核心能力

| 能力 | 说明 |
|---|---|
| **失败归因** | 读取 latest_eval.json 中 checks[].status 为 fail 的条目及其 fail_reason 字段，定位是文件缺失、语法错误还是 RBAC 拦截 |
| **修复策略选择** | 基于归因结果，从 3 种修复策略中选择最优方案 |
| **修复执行** | 自动执行修复（生成缺失文件 / 修正配置 / 恢复 RBAC 规则） |
| **验证闭环** | 修复后重新触发 eval，确认 pass_rate ≥ 1.0 才算修复成功 |
| **回滚自救** | 修复后 eval 仍失败（post_repair_pass_rate < pre_repair_pass_rate），自动回滚到修复前状态，避免连环崩溃 |

### 2.2 非目标

- ❌ 不修复用户业务逻辑（如客户自己的脚本）
- ❌ 不自动升级依赖版本（Python 包等）
- ❌ 不删除用户数据（只增不删）

---

## 3. 架构设计

### 3.1 新增组件

```
scripts/
├── meta_agent.py        # (现有) 进化引擎 — 注入 Hardcase
├── auto_fixer.py        # (新增) 自修复引擎 — 分析失败 & 执行修复
└── orchestrator.py      # (修改) 调用链中加入 auto_fixer
```

### 3.2 状态流转

```
[orchestrator run]
       │
       ▼
  run_health_checks()
       │
       ▼
  generate_eval_report()
       │
       ▼
  pass_rate < 0.5? ───YES───→  auto_rollback.ps1 (现有)
       │                              │
       NO                              ▼
       │                       auto_fixer.analyze()
       ▼                              │
  meta_agent.evolve()         失败 → 归类 → 选策略
       │                              │
       ▼                              ▼
  [done]                        auto_fixer.fix()
                                    │
                                    ▼
                              re-run eval
                                    │
                          pass_rate ≥ 1.0? ──YES──→ [done]
                                    │
                                    NO
                                    ▼
                              auto_rollback (回退自救)
```

### 3.3 修复策略

| 策略 | 触发条件 | 动作 |
|---|---|---|
| **S1: 文件补全** | check 报 `FileNotFoundError` | 用预置模板生成缺失文件 |
| **S2: 配置修正** | check 报 `YAML/JSON 解析错误` | 读取备份配置，用 diff 定位错误行，修正后重写 |
| **S3: RBAC 恢复** | check 报 `RBAC 拦截` / violations 日志违规 | 回退上一轮对 RBAC 的修改，刷新 coder 许可列表 |

---

## 4. auto_fixer.py 接口设计

```python
# files: auto_fixer.py

class AutoFixer:
    def analyze(self, eval_path: str) -> FixPlan:
        """
        读取 latest_eval.json，分析失败 checks，返回修复计划.
        FixPlan 包含: strategy (S1/S2/S3), target_file, confidence (0-1)
        """

    def fix(self, plan: FixPlan) -> bool:
        """
        执行修复计划.
        返回 True = 修复完成 (待验证), False = 修复失败, 需要回滚.
        """

    def verify(self) -> dict:
        """
        重新跑 eval，返回 latest_eval.json.
        外部调用方检查 pass_rate.
        """
```

---

## 5. 安全边界

| 边界 | 规则 |
|---|---|
| **修改范围限制** | 只允许修改: `configs/*.yaml`, `scripts/*.py` (用户脚本只读) |
| **修复次数上限** | 单轮 orchestrator 调用中最多执行 **2 次** 修复尝试，超过则回滚 + 告警 |
| **脏数据隔离** | 修复前自动备份修改目标文件到 `data/backups/{timestamp}/` |
| **人工接管入口** | 修复过程中一旦检测到 `data/runs/MANUAL_OVERRIDE` 文件存在，立即终止所有自动修复 |

---

## 6. 与现有系统的集成点

| 系统 | 变化 |
|---|---|
| `scripts/orchestrator.py` | 在 Step 3 (rollback) 之后、Step 4 (meta-agent evolve) 之前插入 fix 逻辑 |
| `scripts/meta_agent.py` | 无变化（独立进化，不与 fix 耦合） |
| `scripts/auto_rollback.ps1` | 无变化（fix 失败时仍调用该脚本兜底） |
| `data/runs/evolution_status.json` | 扩展字段：新增 `last_fix_plan`, `fix_attempts`, `fix_result` |
| `data/runs/violations.jsonl` | 修复动作本身也写入审计日志（谁修的、改了啥、结果如何） |

---

## 7. 灰度策略 (Phase-in)

| Phase | 范围 | 判定条件 | 时长 |
|---|---|---|---|
| **P0** | 仅日志分析不执行 | pass_rate < 0.5 时分析 + 上报 FixPlan，不执行 fix | 当前 24h 观察窗 |
| **P1** | 文件补全 (S1) | S1 修复 confidence ≥ 0.8 | 观察窗后 48h |
| **P2** | 配置修正 (S2) | P1 稳定运行 48h 无回滚 | 48h |
| **P3** | RBAC 恢复 (S3) | P2 稳定 + 人工确认 | 72h |

**当前所处阶段: P0** — 只分析不上手。

---

## 8. 开放问题

1. **修复冲突**：如果 meta_agent 的 evolve_hardcases() 刚注入了新 case，auto_fixer 紧接着去修 config，两者会不会冲突？ → 答：不会，因为 fix 在 evolve 之前执行（已在流转图中体现）。
2. **多实例并发**：当前设计假定单实例运行。多实例场景（stress_test hardcase）需额外加锁。 → 暂不处理，v1.8.0 保持单实例。
3. **修复日志量**：每次 fix 写入 violations.jsonl + evolution_status.json，长期运行可能膨胀。 → 暂不加轮转，v1.9 考虑日志轮转。

### 已关闭

1. **修复动作是否写入 violations.jsonl？** → **是。** 修复动作本身视为一次系统操作，写入 violations.jsonl 审计日志（字段：actor: auto_fixer, action: fix_apply, target: fix_plan.strategy, result: success/failure）。
