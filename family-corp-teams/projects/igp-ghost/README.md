# IGP Ghost — 幽灵哨兵

**标语**: 不占 token 的全本地系统监控哨兵

**灵感**: 今天踩的坑：chcp 65001 不兼容、inline Python 炸、PowerShell吃引号、子部门跑一半挂掉

**价值**: 用纯 Python 写一个系统监控脚本，0 token 运行，检测 OpenClaw 环境健康度

**技术栈**: Python 3.14 标准库（无任何第三方依赖）

**团队**: frontend-team1(Next.js) → 改名 IGP Ghost Team

**目标**: 一个 .py 文件，能检测：CPU/内存/Python编码/PowerShell兼容性/网络连通性

**输出目录**: D:\bobo\openclaw-foreign\workspace\family-corp-teams\projects\igp-ghost\

---

## 启动时间
IGP Ghost — 幽灵哨兵 于 2026-07-01 09:25 由研发部自主发起
这是 IGP 第一条"没外部吸收就自己造"的创新项目

## 计划
1. Phase 1: 系统环境检测（CPU/内存/Python编码/PowerShell）
2. Phase 2: OpenClaw 健康检测（心跳/Goal/子部门存活）
3. Phase 3: 报警机制（发现异常→输出JSON→看门狗读取）
