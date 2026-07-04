# IGP v3.0 升级计划 — 从管理层到全栈Agent军团的跃迁

## 目标

```
当前：我们 2.0  vs  行业顶 7.0
目标：我们 8.5  vs  行业顶 7.0  (反超！)
```

## 缺什么（8个维度 × 具体方案）

### 1️⃣ Issue→自动修复→PR闭环 (2→10)
- **集成 Open/SWE-agent**：GitHub issue 输入 → 自动分析 → 生成 patch → 创建 PR
- **实现方式**：通过 OpenHands Agent Canvas 在 Docker 沙箱中执行
- **依赖**：Docker Desktop（需要安装）+ GitHub token

### 2️⃣ 多文件协同重构 (1→9)
- **集成 Claude Code / OpenCode**：读取整个代码库上下文，跨文件修改
- **实现方式**：IGP 部门接到任务 → 派发给 Claude Code CLI → 执行多文件变更 → 验证
- **依赖**：ANTHROPIC_API_KEY

### 3️⃣ MCP协议支持 (0→8)
- **集成 Model Context Protocol (MCP)**：让 agent 可以连接文件系统、Git、数据库等工具
- **实现方式**：运行 MCP servers（filesystem/git/memory）+ IGP 通过 MCP SDK 调用
- **依赖**：Python MCP SDK (pip install mcp)

### 4️⃣ 自动测试生成 (1→9)
- **集成 pytest/cov + LLM 测试生成**：代码变更后自动生成并运行测试
- **实现方式**：pytest 作为底座 + OpenAI/DeepSeek 生成测试用例
- **依赖**：pytest + 对应模型的 API key

### 5️⃣ 代码库深度理解 (2→9)
- **集成 Vector RAG pipeline**：代码索引 → chunk → embedding → 语义检索
- **实现方式**：每15分钟自动索引代码库，agent 通过 RAG 获取全局上下文
- **依赖**：embedding 模型 API

### 6️⃣ 架构级变更 (1→8)
- **集成 Sequential Thinking MCP**：复杂架构变更先推理再执行
- **实现方式**：IGP 架构变更流程 → 先调用 Sequential Thinking 规划 → 再调用 agent 执行
- **依赖**：Sequential Thinking MCP server

### 7️⃣ 沙箱安全执行 (0→6)
- **集成 Docker 沙箱**：所有 agent 代码执行在隔离环境中运行
- **实现方式**：每个 agent 分配独立 Docker container，项目文件 bind mount
- **依赖**：Docker Desktop

### 8️⃣ 自动化流水线 (3→9)
- **集成 GitHub Actions / 本地流水线**：commit → test → deploy 全自动化
- **实现方式**：IGP 生成 PR → 自动触发 CI → 验证通过后 merge + deploy
- **依赖**：GitHub Actions / 本地 runner

## 技术栈决策

| 组件 | 选择 | 理由 |
|------|------|------|
| Agent 框架 | LangGraph + Open SWE | 最成熟的开放式 agent 编排 |
| 沙箱 | Docker Desktop | Windows 支持最好 |
| MCP | Python MCP SDK | 与现有 Python 栈一致 |
| 代码索引 | tree-sitter + 本地 embedding | 离线可用，性能好 |
| 测试框架 | pytest | 最通用 |
| LLM API | DeepSeek (已有 key) + OpenAI (备用) | 降低 token 成本 |
| CI 流水线 | GitHub Actions | 零成本 |

## 执行顺序

### Phase 1: 基础设施 (先于一切)
1. ✅ Docker Desktop 安装确认/安装
2. ✅ pip install langgraph mcp pytest tree-sitter
3. ✅ 配置所有 API keys (环境变量统一管理)
4. ✅ 创建 IGP Agent 沙箱目录结构

### Phase 2: 核心实现 (1天)
1. IGP Agent Runner — 每个14部门对应一个 agent 实例
2. MCP Server 集成 — 文件系统/Git/Shell 工具
3. Open SWE 集成 — issue→PR 管道
4. 测试生成模块 — 代码变更 → 自动生成测试

### Phase 3: 进阶能力 (2天)
1. Sequential Thinking — 复杂架构变更的推理层
2. Vector RAG — 代码库索引 + 语义搜索
3. Docker 沙箱 — 安全执行隔离
4. CI/CD 集成 — 自动化流水线

### Phase 4: 组织层集成 (1天)
1. IGP 目标 → Agent 任务 → 执行 → 结果回写 KPI
2. 14个部门 vs 14个 agent 一对一路由
3. PK 机制升级为真实 benchmark 比较
