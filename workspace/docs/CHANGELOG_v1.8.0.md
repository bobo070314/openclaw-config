# CHANGELOG v1.8.0

> **发布日期**: 2026-07-05（预期）
> **前置版本**: v1.7.2-bline-monitor-daemon
> **启用代码**: v1.8.0-auto-fixer-ready (pre-production) → v1.8.0-release (after Go)

---

## 新增功能

### Meta-Agent Self-Evolution Engine

| 特性 | 文件 | 说明 |
|---|---|---|
| 去重注入 | `scripts/meta_agent.py` | 基于 `(category, sha256(normalized_prompt)[:16])` 去重，避免重复 Hardcase |
| 分类轮换 | `scripts/meta_agent.py` | 4 类轮换：self_evolution → edge_case → stress_test → rbac_attack |
| 重复率告警 | `scripts/meta_agent.py` | repeat_rate ≥ 20% 告警，≥ 50% 阻断注入 |
| 状态日志 | `data/runs/evolution_status.json` | 每轮记录 pass_rate、repeat_rate、injected_count、blocked |

### B-Line Observation

| 特性 | 文件 | 说明 |
|---|---|---|
| 监控 Daemon | `scripts/monitor_daemon.py` | 30 分钟周期自动上报，1800s 循环 |
| 运行手册 | `docs/B_LINE_RUNBOOK.md` | 启动/停止/故障处理标准化文档 |

### Auto-Fix Engine (v1.8.0 核心)

| 特性 | 文件 | 说明 |
|---|---|---|
| 失败归因 | `scripts/auto_fixer.py` — `analyze_failures()` | 正则模糊匹配 fail_reason，支持 10+ 实战变体 |
| 策略选择 | `scripts/auto_fixer.py` — `select_strategy()` | 按占比选择 S1/S2/S3/NONE |
| S1 文件补全 | `scripts/auto_fixer.py` — `S1_TEMPLATES` | 预置 agent_chain.yaml + README.deliver.md 模板 |
| S2 配置修正 | `scripts/auto_fixer.py` — `S2_TEMPLATES` | agent_chain.yaml 恢复配置 |
| S3 权限恢复 | `scripts/auto_fixer.py` — `S3_TEMPLATES` | agent_chain.yaml 含 default_roles 恢复 |
| 回滚判定 | `scripts/auto_fixer.py` — `should_rollback()` | post_repair < pre_repair → 回滚 |
| 审计日志 | `scripts/auto_fixer.py` — `log_fix_attempt()` | 每次修复写入 violations.jsonl |

### 灰度策略

P0 → P1 → P2 → P3，详见 RFC-001-meta-autofix.md §7。

---

## 文档补充

| 文档 | 说明 |
|---|---|
| `docs/RFC-001-meta-autofix.md` | 技术设计 RFC |
| `docs/auto_fixer_usage.md` | 使用指南 |
| `docs/v1.8.0_prefab_validation.md` | 预生产验证报告（50/50 测试通过） |
| `docs/v1.8.0_go_nogo_checklist.md` | 评估检查表 |
| `docs/v1.8.0_launch_runbook.md` | 上线流程 |
| `docs/v1.8.0_release_announcement.md` | 上线公告 + 话术 |
| `docs/v1.8.0_feedback_template.md` | 用户反馈模板 |
| `docs/v1.8.0_incident_response.md` | 应急手册 |
| `docs/v1.8.0_copy_alignment_check.md` | 话术对齐校验 |
| `docs/A_line_D2_followup.md` | A 线追打话术 |
| `scripts/d2_reminder.py` | D2 自动提醒脚本 |
| `scripts/v1.8.0_assess.py` | Go/No-Go 自动评估脚本 |
| `scripts/auto_fixer_demo.py` | 10 秒 demos脚本 |
| `demos/auto_fixer_demo_script.txt` | 短视频脚本 |
| `demos/D2_kit.zip` | 追打附件包 |

---

## 版本对比

| 版本 | pass_rate | repeat_rate | injected_count | 修复能力 |
|---|---|---|---|---|
| v1.7.2（基线） | 1.0 | 0% | 4 | 仅回滚 |
| v1.8.0（合入后） | ≥ 1.0 | < 50% | 动态增长 | 归因 + 修复 + 验证 + 回滚 |
