## 染色体3: Skills市场部 - 吸收报告

### 1. SKILL.md 标准格式

根据搜索结果，SKILL.md 是一种开放标准，用于教授 AI 编码代理新能力。它是一个包含 YAML 前置信息和 Markdown 指令的文件。技能是目录中包含一个名为 `SKILL.md` 的文件，该文件使用 YAML 前置信息进行元数据和 Markdown 指令。

#### SKILL.md 文件结构
- **name**: 技能名称
- **description**: 说明该技能应在何时激活
- **instructions**: AI 代理在激活技能时遵循的指令
- **triggers**: 触发技能的条件（例如，用户请求“打开网站”、“填写表单”等）

### 2. 插件生态

#### Claude Code 插件系统
Claude Code 插件系统基于 Model Context Protocol (MCP)，它允许插件与外部服务和 API 集成。MCP 提供了结构化的工具访问，最佳适用于本地工具和自定义服务器。

#### MCP 服务器
MCP 服务器可以是本地的或远程的。本地服务器使用 stdio，而远程服务器使用 Streamable HTTP。MCP 服务器可以包装单个 API（如 Slack MCP 服务器）、一类 API（所有 HRIS 系统）或内部系统（公司的数据库）。

### 3. MCP 生态指南

#### MCP 客户端
MCP 客户端是 AI 代理连接到 MCP 服务器并调用其工具的地方。主要客户端包括 IDE 基于的编码代理：Cursor、Cline（VS Code 扩展）、Windsurf 和 VS Code 的原生代理模式。Claude Desktop 是最广为人知的，但工程团队日常使用 MCP 的通常是他们的 IDE。

#### MCP 服务器
MCP 服务器是暴露工具的地方。开发者需要定义服务器能做什么，实现处理程序，并通过 stdio（用于本地使用）或 HTTP（用于远程/托管使用）公开它。MCP SDK 使构建基本服务器成为几小时的工作。

#### MCP 基础设施
MCP 基础设施涉及谁运行 MCP 服务器，如何管理 OAuth 令牌，以及代理如何与底层服务进行身份验证。这包括托管平台（如 Composio、Pipedream、Knit）。

### 4. MCP 服务器选择

#### 开发者工具
GitHub、Linear、Jira、Notion、Slack 等有良好的官方或接近官方的 MCP 服务器。对于这些类别，使用现有的服务器是最佳选择。

#### 业务数据
HR、薪酬和 ATS 等需要连接到 Workday、BambooHR、Rippling、Greenhouse、Lever、ADP 和 Gusto 等系统。这些系统需要单独的 OAuth 集成，不同的字段命名约定和持续维护。

#### 内部数据系统
如果您的公司有内部数据库、内部 API 或专有数据存储，则自托管是合理的。没有托管平台会拥有您的内部模式，您不应该将内部数据通过第三方代理发送。

### 5. 如何构建自己的 MCP 服务器

当您有一个内部系统、专有数据源或没有托管服务器覆盖的 API 时，构建自己的 MCP 服务器是直接的过程。官方 TypeScript SDK 是最成熟的选项。

#### 安装 SDK
```bash
npm install @modelcontextprotocol/sdk
```

#### 示例代码
```javascript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
 ListToolsRequestSchema,
 CallToolRequestSchema
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
 { name: "internal-hr-server", version: "1.0.0" },
 { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
 tools: [
 {
 name: "get_employee",
 description: "Fetch an employee record by their internal ID",
 inputSchema: {
 type: "object",
 properties: {
 employee_id: {
 type: "string",
 description: "The employee's internal system ID"
 }
 },
 required: ["employee_id"]
 }
 }
 ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
 if (request.params.name === "get_employee") {
 const { employee_id } = request.params.arguments as { employee_id: string };

 // Replace with your actual data source call
 const employee = await fetchFromInternalHRSystem(employee_id);

 return {
 content: [{ type: "text", text: JSON.stringify(employee, null, 2) }]
 };
 }

 throw new Error(`Unknown tool: ${request.params.name}`);
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

### 6. MCP 安全考虑

#### 工具中毒
MCP 服务器暴露工具描述，这些描述可能包含隐藏的指令，导致代理行为偏离。Mitigation：将工具描述视为不受信任的输入，实施过滤层以检查描述中的指令模式。

#### 供应链风险
公共注册表中的 MCP 服务器未经审核。一个流行的社区 MCP 服务器请求文件系统访问和网络访问是一个特权进程，在开发者的机器上运行。服务器的代码由陌生人编写，版本变化没有正式的安全审查。

#### 超过权限的服务器
MCP 服务器应仅具有完成其功能所需的最小权限。审计每个工具的 inputSchema 和底层 API 权限，不仅在设置时，而且在服务器更新时。

### 7. 结论

SKILL.md 格式和 MCP 生态系统为 AI 编码代理提供了强大的工具和灵活性。通过理解这些标准和生态系统，可以有效地扩展和定制 AI 代理的能力。