---
name: pk-executor
description: "IGP pk-executor skill"
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

# Pk Executor Skill
# PK Executor Skill

## Description
执行部门PK的Agent Skill

## Metadata
- version: 1.0
- author: IGP Team
- category: operations
- tags: [pk, execution, department]

## Instructions
1. 接收PK任务指令
2. 解析任务参数（部门A, 部门B, 评估标准）
3. 执行PK流程
4. 生成PK结果报告

## Usage
/execute-pk [departmentA] [departmentB] [criteria]