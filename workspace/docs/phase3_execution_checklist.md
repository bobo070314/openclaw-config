# Phase 3 执行清单 — 拍板后 1 小时行动

**拍板时间**: 2026-07-05 10:04 UTC
**执行窗口**: 拍板后 60 分钟内

---

## □ 第 1 步：导入 F-005 ~ F-050 故障类型（~10min）

```bash
# 从 openclaw-silicon-base 拉取故障模板
cd D:\bobo\openclaw-foreign\workspace
python scripts/auto_fixer.py --import-faults silicon-body-fixer/docs/specs/v2.0_fault_request_template_hoshine.yaml
```

**验收**: `data/runs/violations.jsonl` 中有新故障类型记录

---

## □ 第 2 步：对接合盛 MES 测试环境（~15min）

1. 确认合盛 MES 接口地址（HTTP POST → `mes_inbound/`）
2. 复制 `v2.0_fault_request_template_hoshine.yaml` 到 `mes_inbound/`
3. 运行 `auto_fixer_demo.py` 验证对接
4. 检查 `[NOTIFY]` 日志是否有新告警

**验收**: 合盛 MES 测试环境能收到模拟故障

---

## □ 第 3 步：启用 S1 文件修复（~10min）

```python
# 在 orchestrator.py 中取消注释以下代码
# from scripts.auto_fixer import run_fix_pipeline
# run_fix_pipeline()
```

**验收**: 运行一次 eval，确认 pass_rate = 1.0

---

## □ 第 4 步：灰度发布 S2/S3（~15min）

1. 先运行 `should_rollback()` 确认无退化
2. 从 P0（分析 only）切到 P1（S1 执行）
3. 观察 30 分钟，确认 repeat_rate < 20%
4. 切到 P2（S2 启用）
5. 观察 30 分钟，确认无 regress
6. 切到 P3（S3 启用）

**验收**: 每阶段续报 6 项全绿

---

## □ 第 5 步：通知 A 线客户（~10min）

- 张工：发 WeChat 消息（已存档）
- 李总：发 WeChat 消息
- 刘老板：发 WeChat 消息
- 2h 后发邮件给全部 3 人

**验收**: 3 条 WeChat + 1 封邮件全部发出

---

## 回滚触发条件（任一满足即回退到 Auto-Fixer-Ready）

| 条件 | 阈值 | 动作 |
|---|---|---|
| pass_rate < 1.0 | 连续 2 轮 | `git checkout v1.8.0-auto-fixer-ready` |
| repeat_rate ≥ 50% | 单轮触发 | 暂停 S2/S3，回退到 P0 |
| block_count > 0 | 任何 | 立即停止注入，回退到纯观测模式 |
| 合盛 MES 对接报错 | 任何 | 切换到 mock 模式，人工排查 |

---

**审批**

| 角色 | 执行人 | 签字 |
|---|---|---|
| 技术执行 | ________ | ________ |
| 质量审核 | ________ | ________ |
