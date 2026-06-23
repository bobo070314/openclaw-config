---
name: create-pr
description: GitHub Pull Request 创建 - 自动生成PR描述、关联Issue、添加Reviewer和标签
version: 1.0.0
status: active
category: devsecops
tags: [github, pr, git]
---

# create-pr

## Overview
GitHub Pull Request 创建 - 自动生成PR描述、关联Issue、添加Reviewer和标签

## Category
devsecops

## When to Use
Trigger this skill when the user requests operations related to create pr.

## Workflow

### Pre-flight
1. Verify prerequisites are met (dependencies, credentials, environment)
2. Check configuration via `create-pr-setup` or equivalent if available
3. Validate user input parameters

### Execution
1. Parse and validate the user's request
2. Execute the core operation using appropriate tools:
   - **exec**: Run CLI commands, scripts, or API calls
   - **web_fetch**: Call REST APIs when applicable
   - **browser**: Handle web-based flows when needed
3. Handle errors gracefully with clear messages

### Post-execution
1. Format results for readability
2. Report success/failure with actionable next steps
3. Log operations if tracking is enabled

## Key Constraints
- Always validate inputs before execution
- Handle authentication/authorization errors explicitly
- Respect rate limits and API quotas
- Provide Chinese-language output by default (可切换英文)
- Never expose secrets or tokens in output

## Examples

### Example 1: Basic Operation
```
User: 用 create-pr 执行基本操作
Assistant: [调用 exec 执行相应命令，返回格式化结果]
```

### Example 2: Error Handling
```
User: 用 create-pr 操作一个不存在的资源
Assistant: [返回明确的错误信息，建议下一步操作]
```

## Dependencies
- OpenClaw runtime >= 1.0
- Category-specific external tools (see individual commands)

## Related Skills
- Check `skills-audit` for available skill registry
- Check category peers under `devsecops`
