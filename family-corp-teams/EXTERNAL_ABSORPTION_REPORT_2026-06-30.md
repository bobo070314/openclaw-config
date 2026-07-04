# IGP 外部生态吸收报告 (2026-06-30 23:33)

**IGP平均分: 4.0/10 vs 行业基线: 7.5/10**
**差距: -3.5 分**

---

## 一、行业Top Agent排行榜 (2026-06-18)

| 排名 | Agent | Stars | SWE-bench V | Term-Bench | 突出特性 |
|------|-------|------:|:-----------:|:----------:|---------|
| Codex CLI + GPT-5.5 | 90K | 88.7% | 83.4% (#1) | 5种表面/MCP/Skills |
| Claude Code + Opus 4.8 | 131K | 88.6% | 78.9% | Agent View//goal/Plugin |
| Gemini CLI + 3.1 Pro | 105K | 80.6% | 70.7% | 1000次/天免费 |
| OpenCode (自选模型) | 172K⭐ | 模型决定 | 模型决定 | 75+ providers/Scout/MIT |
| Cline (自选模型) | 63K | 模型决定 | 模型决定 | Plan-Act双模/Checkpoints |
| Goose (自选模型) | 48K | 模型决定 | 模型决定 | Linux Foundation/70+MCP |

---

## 二、IGP v3 逐维差距分析

| 维度 | IGP | 行业 | 差距 | 行动 |
|------|:---:|:----:|:----:|------|
| MCP协议支持 | 🔴 1 | 9 | 8 | MUST: 升级为MCP Client，消费外部MCP服务器 |
| Agent Skills生态 | 🔴 0 | 9 | 9 | MUST: 实现SKILL.md解析器 + 技能市场 |
| A2A协议支持 | 🔴 0 | 7 | 7 | MUST: 实现A2A Client/Server |
| LLM Provider灵活度 | 🟡 4 | 9 | 5 | SHOULD: 抽象Provider层，支持多模型路由 |
| 沙箱安全执行 | 🟡 5 | 8 | 3 | SHOULD: Plan/Act双模式 + 安全审批流 |
| 代码库上下文理解 | 🟢 6 | 9 | 3 | COULD: RAG升级 + Skills分层加载 |
| 代码审查 | 🔴 2 | 8 | 6 | COULD: 创建CodeReview Agent（Skills格式） |
| 自动测试生成 | 🟡 5 | 7 | 2 | SHOULD: 测试Agent接入AgentCI |
| 自动化流水线 | 🟢 6 | 9 | 3 | SHOULD: PR+CI+Review全闭环 |
| PK/进化/淘汰机制 | 🟢 9 | 2 | -7 | KEEP & ENHANCE: 嫁接到Skills生态上 |
| 工单/Goal系统 | 🟢 7 | 4 | -3 | FIX & ENHANCE: 修Goal bug + 集成Skills |
| Agent数量(生态) | 🟡 3 | 9 | 6 | MUST: Agent技能解耦成可安装的Skills包 |

| **平均** | **4.0** | **7.5** | **-3.5** | |

---

## 三、差异化优势（我们独有的）

- ✅ **PK竞争/淘汰再生机制 — 行业里唯一一个让Agent之间内卷的体系**
- ✅ **42个Team结构 + 14部门 + 参谋部 — 行业没有类似的虚拟企业架构**
- ✅ **KPI+Token成本闭环 — 行业全都不关注每个Agent消耗了多少token**
- ✅ **开车门(Goal自动触发) — 行业需要手动输入，我们是'你说一句我全自动'**

### 三个致命空白（必须补）
- ❌ **MCP协议兼容 — 0分，必须补上**
- ❌ **Agent Skills生态 — 0分，最大空白**
- ❌ **A2A协议 — 0分，但可以短期不补**

---

## 四、吸收计划（按优先级）

| 优先级 | 行动 | 投入 | 收益 |
|:-----:|------|:---:|:----:|
| P0 | **MCP协议兼容**：igp_mcp_bridge → 兼容MCP Client + 导出MCP Server | ~4h | 立即接入1200+ MCP服务器生态 |
| P0 | **Agent Skills系统**：SKILL.md解析器 + 技能目录 + 自动加载 | ~6h | Agent能力从hardcode变成可安装包 |
| P1 | **Plan/Act双模式** + Checkpoints安全点 | ~3h | 避免Agent乱改代码 |
| P1 | **Provider抽象层**：多模型路由（保留qwen但增加降级） | ~2h | 不再限于DashScope |
| P2 | **代码审查Agent**：PR提交后自动审查 | ~3h | 质量保障 |
| P2 | **AgentCI流水线**：测试+审查+PR全自动 | ~4h | 完成编码闭环 |
| P3 | **A2A协议**：Agent-to-Agent标准通信 | ~8h | 长期差异化 |

### 预估效果：MCP + Skills实现后，差距从-3.8缩小到-1.0 → 反超行业
