---
name: test-runner
description: "IGP test-runner skill"
license: MIT
compatibility:
 - igp-v4
 - claude-code
 - cursor
 - codex
metadata:
 author: IGP v4
 version: 1.0.0
 tags:
  - general
allowed-tools:
 - read
 - write
 - exec
 - web_search
---

# Test Runner Skill
# Test Runner Skill

## Description
运行测试套件的Agent Skill

## Metadata
- version: 1.0
- author: IGP Team
- category: development
- tags: [test, automation, suite]

## Instructions
1. 接收测试任务指令
2. 解析测试参数（项目路径, 测试类型）
3. 执行测试流程
4. 生成测试结果报告

## Usage
/run-tests [projectPath] [testType]