---
name: subconscious-daemon
version: "0.2.0"
description: "24/7 background sentinel — monitors CPU, memory, disk, logs, Git, and prompts for anomalies"
enabled: true
category: infrastructure
tags: [daemon, monitoring, sentinel, security, background]
---

# 🧠 subconscious-daemon

24/7 后台守护进程。眼睛永远睁着，替你站岗。

## 功能

| 监控项 | 阈值 | 动作 |
|-------|------|------|
| CPU | >85% | 记录告警 |
| Memory | >90% | 记录告警 |
| Disk | >95% | 记录告警 |
| Logs | ERROR/FATAL | 收集并告警 |
| Git | .env泄露/二进制文件 | 告警 |
| Prompts | 对抗模式检测 | 标记 |

## 用法

```bash
python subconscious-daemon/run.py              # 一次性检查
python subconscious-daemon/run.py --daemon     # 后台循环运行
python subconscious-daemon/run.py --interval 30  # 每30秒检查
python subconscious-daemon/run.py --json       # JSON输出
python subconscious-daemon/run.py --dry-run    # 不保存状态
```

## 集成

- 告警日志写入 `skills/.daemon/logs/daemon_YYYY-MM-DD.jsonl`
- 状态持久化到 `skills/.daemon/state.json`
- 可对接 WeCom/企微 推送告警
