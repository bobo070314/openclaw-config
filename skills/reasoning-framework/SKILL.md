---
name: reasoning-framework
description: 三层推理框架：分解→执行→验证。封装 Sequential Thinking MCP 供复杂任务使用。依赖 MCP server `sequential-think`。
---

# Skill: 推理规划框架 (reasoning-framework)

## 问题
复杂任务容易一跳出结论，漏步骤、漏验证、忘记渐进式执行。

## 方案
**三层推理引擎**：将 Sequential Thinking MCP 封装为可复用的推理协议。任何复杂任务都走：
1. **分解**（Decompose）— 拆成 3-8 个步骤
2. **执行**（Execute）— 按步骤逐一落工具
3. **验证**（Verify）— 检查结果质量

## 依赖
- MCP Server: `sequential-think`（已安装，probe 通过）

## 使用说明

当遇到复杂任务时（如 GitHub 分析、日志排错、多步数据收集），使用 `sequentialthinking_tools` 记录每一步的推理，路径如下：

### Step 1: 分解
```
sequentialthinking_tools(
  thought: "明确任务目标并分解为子任务"
  thought_number: 1
  total_thoughts: <预估总步数>
  next_thought_needed: true
  available_tools: [<当前可用工具列表>]
  recommended_tools: [{tool_name, confidence, rationale}]
  remaining_steps: ["Step 2: ...", "Step 3: ..."]
)
```

### Step 2-N: 执行
每执行一个工具调用后，记录该步骤的结论：
```
sequentialthinking_tools(
  thought: "<执行结果/发现>"
  thought_number: <N>
  total_thoughts: <总步数>
  next_thought_needed: <true/false>
)
```

### 最后一步: 验证
```
sequentialthinking_tools(
  thought: "<完整结论，验证结果>"
  thought_number: <N>
  total_thoughts: <N>
  next_thought_needed: false
)
```

### 复盘与分支
- 卡住了？ `is_revision: true, revises_thought: <N>`
- 需要平行路线？`branch_from_thought: <N>, branch_id: "alt-a"`
- 后续探索查看历史？`get_thinking_history(session_id: "<会话ID>")`

## 应用场景

| 场景 | 预估步数 | 需配合的工具 |
|------|---------|------------|
| GitHub 项目画像分析 | 4-6 | github API, MCP tools |
| 代码 review + 重构 | 5-8 | read, edit, code-runner |
| 日志排错 | 3-5 | read, web-scraper, tavily |
| 跨项目调研 | 5-7 | web_search, read, git |
| 技能包装 | 4-6 | skill_workshop, read, write |

## 模板（可复用）

- `session_id`: 推理步骤 ID，英文小写+连字符（`debug-login-issue`）
- `available_tools`: 从当前 session 的 tools 列表取
- `recommended_tools`: 每一步推荐 1-2 个最佳工具，附 confidence

## 注意事项
- 简单问题（1 步能答）不需要用，避免过度开销
- `thought_number` 递增，`total_thoughts` 可随时用 `needs_more_thoughts: true` 加码
- 注意区分 MCP 的 `sequentialthinking_tools` 和 OpenClaw 内置工具
