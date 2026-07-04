# ⚔️ IGP V4 全面战争总动员报告 (2026-06-30 23:40)

## 一、当前态势

| 指标 | IGP v3 | 行业基线 | 差距 | 等级 |
|------|:------:|:--------:|:----:|:----:|
| 综合评分 | **4.0/10** | **7.5/10** | **-3.5** | 🚨 全面落后 |
| MCP协议 | 1/10 | 9/10 | -8 | 🔴 致命 |
 | Skills生态 | 0/10 | 9/10 | -9 | 🔴 致命 |
| 进化PK机制 | **9/10** | 2/10 | +7 | 🟢 独有优势 |

## 二、动员令

**IGP V4 全面战争总动员令**
**指挥官: 董事会（老板）**
**等级: MAXIMUM_ALERT**

### 作战指令
- **all_departments**: 即日起，所有部门KPI考核增加'外部吸收贡献度'指标。每吸收一个外部项目到IGP体系加10分。
- **研发团队(核心)**: 成立V4突击队。消化吸收后直接产出v4代码。优先级：MCP兼容 > Skills系统 > Provider抽象 > Plan/Act安全模式。
- **战略投资部**: 启动外部猎头模式。对GitHub Top项目关键贡献者生成邀请函。目标：MCP协议核心贡献者、OpenCode架构师、Cline安全专家。
- **AI部门**: 评估DashScope Qwen vs 外部模型差距。给出Provider抽象层设计方案。
- **Frontend/Backend/Infra**: 为v4模块创建新目录upgrade-v4/。三人一组分别负责MCP Client/Server/Skills解析。

### 预期战果
- 吸收前: IGP avg 4.0/10, 行业 avg 7.5/10, 差距-3.5
- P0吸收后: IGP avg 6.5/10, 行业 avg 7.5/10, 差距-1.0
- 全量吸收后: IGP avg 8.5/10, 行业 avg 7.5/10, 反超+1.0
- 核心理念: 不追低处。嫁接PK/进化优势到标准生态。IGP = 会自我进化的企业架构Agent军团

## 三、外部吸收目标

### 优先级P0
- [N/A⭐] MCP Python SDK
  - 吸收方法: 作为submodule依赖引入。编写MCP Client适配层。
  - 负责: infrastructure-team1 + ai-team1
- [26900⭐] VoltAgent/awesome-agent-skills
  - 吸收方法: 克隆仓库，批量解析SKILL.md格式。编写skills目录扫描器。
  - 负责: frontend-team2 + ai-team2
- [N/A⭐] A2A Protocol Spec
  - 吸收方法: 研究Spec，编写Agent Card发现机制。短期只做Client读。
  - 负责: backend-team3 + ai-team3

### 优先级P1
- [N/A⭐] Scout subagent (OpenCode)
  - 吸收方法: 理解Scout设计哲学（外部文档搜索+上下文注入），复刻到IGP。
  - 负责: ai-team2
- [N/A⭐] Cline Checkpoints
  - 吸收方法: 理解git-based checkpoints机制，实现Plan/Act安全审批流。
  - 负责: backend-team1 + quality-team2
- [163000⭐] Everything Claude Code
  - 吸收方法: 全套Agent配置/规则/Skills/插件体系参考。
  - 负责: content-team1 + frontend-team1

### 优先级P2
- [N/A⭐] Augment Code Review
  - 吸收方法: 理解ticket-to-pr + 自动review的Agent流水线设计。
  - 负责: quality-team1 + pmo-team2
- [N/A⭐] SWE-agent (AgentCI)
  - 吸收方法: 研究自修复测试流水线的Agent实现。
  - 负责: quality-team3 + ai-team3


## 四、专家猎头清单

- **MCP Spec**: IGP需要MCP协议领域的专家来指导桥接设计
  → 搜索: MCP spec core contributor, python-sdk maintainer
- **OpenCode**: IGP需要借鉴Scout subagent和background agents设计
  → 搜索: OpenCode architect, AI SDK provider model designer
- **Cline**: Plan/Act双模式设计 - 我们最需要的安全执行模式
  → 搜索: Cline checkpoints designer, Plan/Act workflow
- **Agent Skills Spec**: SKILL.md标准制定者，帮助我们将IGP知识转为Skills包
  → 搜索: Skills over MCP working group, SKILL.md spec author

## 五、v4模块研发清单（核心）

| 编号 | 模块 | 吸收来源 | 负责团队 | 产出 |
|:----:|------|----------|----------|------|
| v4-01 | igp_mcp_client.py | MCP Python SDK + 官方spec | infrastructure-team1 + ai-team1 | 消费任何MCP工具 + 导出IGP功能为MCP Server |
| v4-02 | igp_skills_loader.py | VoltAgent/awesome-agent-skills + SKILL.md spec | ai-team2 + frontend-team2 | Agent能力从hardcode变成可安装的Skills包 |
| v4-03 | igp_provider_router.py | OpenCode AI SDK + Cline provider 设计 | ai-team3 + backend-team3 | IGP不再限于qwen，多个模型按需路由 |
| v4-04 | igp_plan_act.py | Cline Plan/Act 模式 | backend-team1 + quality-team2 | 避免Agent直接修改文件，安全等级提升 |
| v4-05 | igp_a2a_bridge.py | A2A Spec + a2aproject/A2A | backend-team2 + ai-team1 | IGP内部Agent通过标准协议通信 |
| v4-06 | igp_code_review.py | Augment Code Review + Codex auto review | quality-team1 + frontend-team1 | PR全自动审查闭环 |
| v4-07 | igp_agent_ci.py | SWE-agent + test_runner.py v2 | quality-team3 + ai-team3 | Agent输出自动验证 |

## 六、研发核心理念

> **不追低处。不跟OpenCode比provider数量、不跟Codex比Terminal-Bench。**
> **利用我们的独特优势(PK/进化/KPI/虚拟企业架构)，将其嫁接到标准生态(MCP+Skills+A2A)上。**
> **IGP的定位：会自我进化的企业架构Agent军团。不是编码工具，是数字生命体。**

---

*本报告时间: 2026-06-30 23:40 CST*
*作战状态: 已完成全量扫描和动员部署，等待董事会指令开始v4模块研发*