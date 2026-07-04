# 🧬 IGP V5 Skills Catalog

_8条染色体, 38个独立模块 | 纯标准库 | 0外部依赖_

## #1 MCP生态部

- **入口**: `python chromosomes/chromosome1/infra/run.py`
- **模块数量**: 6

| 模块 | 功能 | 大小 |
|------|------|------|
| fastmcp_export.py | Auto-generated FastMCP Server from IGP Skills | 1131B |
| igp_mcp_pk.py | MCP PK ranking module | 1789B |
| igp_mcp_v5_client.py | IGP V5 MCP Client - 连接任何MCP Server | 2579B |
| igp_mcp_v5_server.py | IGP V5 MCP Server 导出器 - 把IGP Skills 导出为 MCP Server | 2003B |
| mcp_v2_upgrade.py | IGP V5 MCP生态部 v2 — FastMCP兼容 + MCP服务器自动发现 | 11188B |
| run.py | (无文档) | 877B |

## #2 A2A联邦部

- **入口**: `python chromosomes/chromosome2/infra/run.py`
- **模块数量**: 5

| 模块 | 功能 | 大小 |
|------|------|------|
| a2a_agent_card.py | Agent身份/能力/端点描述 | 1106B |
| a2a_discovery.py | Agent发现服务实现 | 1757B |
| a2a_task_protocol.py | A2A任务协议消息结构 | 1924B |
| a2a_v2_upgrade.py | IGP V5 A2A联邦部 v2 — 完整Agent间协议 + 联邦发现 + 任务委派 | 9777B |
| run.py | (无文档) | 1200B |

## #3 Skills市场部

- **入口**: `python chromosomes/chromosome3/infra/run.py`
- **模块数量**: 4

| 模块 | 功能 | 大小 |
|------|------|------|
| run.py | (无文档) | 639B |
| skill_market.py | (无文档) | 1001B |
| skill_package.py | (无文档) | 1171B |
| skill_pk_rank.py | (无文档) | 987B |

## #4 Provider路由部

- **入口**: `python chromosomes/chromosome4/infra/run.py`
- **模块数量**: 4

| 模块 | 功能 | 大小 |
|------|------|------|
| provider_abstraction.py | (无文档) | 1030B |
| provider_pk.py | (无文档) | 1463B |
| provider_router.py | (无文档) | 1071B |
| run.py | (无文档) | 1452B |

## #5 安全Guardian部

- **入口**: `python chromosomes/chromosome5/infra/run.py`
- **模块数量**: 4

| 模块 | 功能 | 大小 |
|------|------|------|
| guardian_act.py | Guardian Act Module - Approval Execution | 1150B |
| guardian_plan.py | Plan阶段：只读分析，不执行任何修改 | 2371B |
| guardian_policy.py | Guardian Policy Engine - Security Strategies | 1400B |
| run.py | Guardian Verification Script | 1325B |

## #6 商业协议部

- **入口**: `python chromosomes/chromosome6/infra/run_v2.py`
- **模块数量**: 7

| 模块 | 功能 | 大小 |
|------|------|------|
| acp_client.py | (无文档) | 1587B |
| agent_commerce.py | (无文档) | 2109B |
| agent_commerce_v2.py | IGP V5 商业协议部 v2 —— 接入真实支付/电商API | 6871B |
| commerce_pk.py | (无文档) | 1831B |
| commerce_pk_v2.py | IGP V5 商业协议部 v2 — 收入追踪 + PK排名 | 3824B |
| run.py | (无文档) | 746B |
| run_v2.py | 商业协议部 v2 验证 —— 真实支付API + 商业PK | 3252B |

## #7 Agent OS层

- **入口**: `python chromosomes/chromosome7/infra/run.py`
- **模块数量**: 4

| 模块 | 功能 | 大小 |
|------|------|------|
| agent_os_kernel.py | (无文档) | 3622B |
| agent_os_scheduler.py | (无文档) | 1405B |
| agent_os_shell.py | (无文档) | 2858B |
| run.py | chromosome7 Agent OS 无交互验证 | 1471B |

## #8 AP2支付协议

- **入口**: `python chromosomes/chromosome8/infra/run.py`
- **模块数量**: 4

| 模块 | 功能 | 大小 |
|------|------|------|
| ap2_payment_gateway.py | (无文档) | 2029B |
| ap2_protocol.py | (无文档) | 3332B |
| ap2_wallet.py | (无文档) | 2561B |
| run.py | (无文档) | 1487B |

