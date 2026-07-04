# B-Line Runbook: Meta-Agent Evolution Engine

> **北极星**：先稳定进化，再开放自修复。

---

## 1. 指标定义

| 指标 | 来源 | 含义 |
|---|---|---|
| `pass_rate` | `data/runs/latest_eval.json` | 健康检查通过率，1.0 = 全绿 |
| `repeat_rate` | `meta_agent.analyze_patterns()` | 历史 hardcases 中相同 category 的重复占比 |
| `block` | `meta_agent.evolve_hardcases()` | 是否因重复率超标而暂停注入、执行压缩 |

状态日志：`data/runs/evolution_status.json`

---

## 2. 阈值动作

| 阈值 | 动作 |
|---|---|
| `repeat_rate < 20%` | 正常轮换注入 |
| `repeat_rate ≥ 20%` | 控制台 `⚠️` 告警，继续注入 |
| `repeat_rate ≥ 50%` | 🚫 **block**：暂停注入 → 执行去重压缩 → 恢复轮换 |

去重键：`(category, sha256(normalized_prompt))[:16]`

---

## 3. 故障处理

**场景：repeat_rate ≥ 50% 触发 block**

1. **停注入一轮** — engine 自动跳过生成步骤
2. **去重压缩** — 按 `category + prompt_hash` 保留首条，删除重复
3. **恢复** — 去重后重新计算 repeat_rate，低于 50% 自动恢复注入

**人工干预入口：**
- 查看状态：`Get-Content data/runs/evolution_status.json`
- 手动清库（仅测试环境）：`Remove-Item data/evals/hardcases.jsonl`
- 单跑：`python scripts/orchestrator.py`

---

## 4. 启动监控守护进程

```powershell
# 启动（后台运行，日志写入文件）
python scripts/monitor_daemon.py > logs/monitor.log 2>&1

# 停止
# 找到 PID 后 Ctrl+C，或：
# Get-Process | Where-Object { $_.CommandLine -like '*monitor_daemon*' } | Stop-Process
```

Daemon 行为：
- 每 1800 秒（30 分钟）读取 `data/runs/evolution_status.json`
- 输出 Runbook 模板格式报告到 stdout
- 异常检测：repeat_rate ≥ 20%（⚠️）, ≥ 50%（🚫）, blocked=true（🚫）
- 健康检查：evolution_status.json 超过 120 分钟未更新则标记 STALE

---

## 5. 每 30 分钟上报模板

```
pass_rate: <值>
repeat_rate: <值>% [⚠️ / 🚫 / ✅]
injected: <本轮注入数> / total: <累计数>
```

示例：
```
pass_rate: 1.0
repeat_rate: 0.0% ✅
injected: 0 / total: 4
```
