# IGP Ghost 幽灵哨兵 — 最佳实践 v2

## 研发记录
- **时间**: 2026-07-01 09:25 → 09:31
- **迭代**: v1(检测) → v2(检测+自愈+报警)
- **团队**: frontend-team1 → IGP Ghost Team
- **Token消耗**: 0（纯本地）

## 解决的核心问题
1. 系统环境一有变化就断链，没人知道
2. 子部门挂了没人重建
3. Python编码/PowerShell兼容性没人巡逻

## 模块架构
```
ghost.py
├─ 检测层
│  ├─ python_env     Python编码就绪性
│  ├─ powershell     PowerShell兼容性
│  ├─ subagents      12部门存活检查
│  ├─ heartbeat      IGP心跳可运行性
│  └─ disk           磁盘空间(>1GB)
├─ 自愈层
│  ├─ set console codepage
│  ├─ 重建缺失的部门目录
│  ├─ 重建 memory 目录
│  └─ 重新检查subagents
└─ 报警层
   ├─ ghost_alert.json (memory/)
   └─ D2A格式消息 → headquarters/_ghost_report.json
```

## 部署方法
```powershell
$env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'; python projects/igp-ghost/ghost.py
```

## 回馈升级
- ✅ 已写入 V4 研发反馈: `upgrade-v4/_rd_feedback.json`
- ✅ 报警系统与 D2A Agent 协议兼容
- ✅ 输出到 memory/ 供看门狗读取

## 下次升级方向
- v3: 定时巡逻（用 cron 跑）
- v4: 自动修 igp_heartbeat 等核心脚本
- v5: 发现新工单时自动发 D2A 通知
