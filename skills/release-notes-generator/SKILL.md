---
name: release-notes-generator
description: >
  Auto-generates GitHub Release Notes from git log. Parses commits
  following Conventional Commits spec, classifies changes (feat, fix,
  chore, docs, refactor, perf, test, ci, build), groups by category,
  and outputs a ready-to-publish Markdown release note with changelog,
  contributors, and stats. Use when user says "generate release notes",
  "create changelog", "release note", "version changelog", "what changed".
version: 0.2.0
status: implemented
category: meta
---

# Release Notes Generator

## 定位
从 git log 自动生成 GitHub Release Note。遵循 Conventional Commits 规范解析提交，按类型分组（feat/fix/chore/docs/refactor/perf/test/ci/build），输出可直接发布的 Markdown 发布说明，含更新日志、贡献者和统计信息。

## 触发条件
- 用户说"生成 release note" / "generate changelog" / "release note"
- "version changelog" / "what changed since ..."
- 版本发布前需要一个干净的发布说明

## 工作流
1. **提交提取** — `git log` 获取两个 tag 之间（或最近 N 个）的所有提交
2. **规范解析** — 按 Conventional Commits 解析 type(scope): message 格式
3. **类别分组** — feat → 新功能、fix → 修复、perf → 性能、refactor → 重构等
4. **统计生成** — 提交总数、贡献者数、变更文件数
5. **Markdown 输出** — 格式化的 Release Note，含 Breaking Changes 警告

## 关键约束
- 严格遵循 Conventional Commits 规范解析
- Breaking Changes（`!` 或 `BREAKING CHANGE:` footer）需醒目标注
- 支持自定义范围（from-tag..to-tag 或最近 N 个版本）
- 不做 git push 或任何写操作，仅生成文本
