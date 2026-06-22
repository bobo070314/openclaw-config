---
name: infra-diagram-as-code
description: >
  Architecture diagram as code — reverse-engineers project structure
  from code and config, generates C4 architecture diagrams (Context,
  Container, Component, Code) and Mermaid diagrams. Extracts data
  from code-navigator (symbol dependencies) and deployment-automation
  (infrastructure topology). Use when user says "draw architecture",
  "generate diagram", "C4 model", "system architecture", "Mermaid chart".
version: 0.2.0
status: implemented
category: devsecops
---

# Infrastructure Diagram as Code

## 定位
从代码和配置反向提取架构关系，生成 C4（Context / Container / Component / Code）和 Mermaid 架构图。将活的代码库变成可读、可维护的架构文档。数据源：`code-navigator`（符号依赖）+ `deployment-automation`（基础设施拓扑）。

## 触发条件
- 用户说"draw architecture" / "generate diagram" / "C4 model"
- "system architecture" / "Mermaid chart" / "架构图"
- 新成员入职需要系统全景图
- 代码审查需要组件依赖关系图

## 工作流
1. **数据提取** — 调用 `code-navigator` 获取符号依赖关系 + 从 docker-compose/Dockerfile 解析服务拓扑
2. **关系建模** — 构建服务→组件→代码三层关系图
3. **图表生成** — 输出 C4 模型（Context/Container/Component/Code）或 Mermaid 语法
4. **导出** — 支持 Markdown 嵌入（Mermaid）和独立 SVG（PlantUML 渲染）

## 关键约束
- C4 模型严格四层：Context→Container→Component→Code
- Mermaid 输出可直接嵌入 GitHub Markdown
- 不修改任何源码，仅读取和分析
- 依赖关系按调用频率和响应尺寸标注
