---
name: pr-creator
description: "IGP pr-creator skill"
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

# Pr Creator Skill
# PR Creator Skill

## Description
创建PR的Agent Skill

## Metadata
- version: 1.0
- author: IGP Team
- category: development
- tags: [pr, creation, git]

## Instructions
1. 接收PR创建指令
2. 解析PR参数（源分支, 目标分支, 提交信息）
3. 执行PR创建流程
4. 生成PR链接和状态报告

## Usage
/create-pr [sourceBranch] [targetBranch] [commitMessage]