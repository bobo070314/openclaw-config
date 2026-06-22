---
name: agent-testing
description: 多框架测试运行器，自动检测pytest/vitest/jest/cargo/go测试框架并执行
version: 0.2.0
status: implemented
category: dev
---

# agent-testing — 多框架测试运行器

## 定位
自动检测项目使用的测试框架（pytest/vitest/jest/cargo/go test），执行测试并汇总 pass/fail/skip 统计。

**已验证项目：lobe-chat/prisma/stripe/temporal/trpc — 框架检测全部正确。**

## 触发条件
- "跑测试"
- "运行单元测试"
- "run tests"
- "测试覆盖率"

## 支持的框架

| 框架 | 检测方式 | 执行命令 |
|------|----------|----------|
| pytest | `pytest.ini` / `pyproject.toml` / `conftest.py` | `pytest -v` |
| vitest | `vitest.config.*` | `npx vitest run` |
| jest | `jest.config.*` / `"jest"` in package.json | `npx jest` |
| cargo-test | `Cargo.toml` | `cargo test` |
| go-test | `go.mod` + `*_test.go` | `go test ./...` |

## 工作流
1. **框架检测** — 扫描项目根目录检测测试框架
2. **运行测试** — 执行对应框架的测试命令
3. **结果统计** — 汇总 pass/fail/skip + 耗时
4. **输出报告** — 分级展示 + 失败详情

## 关键约束
- Windows 兼容：不使用 bash 特定语法
- 超时保护：单次测试运行 ≤ 300s
- 失败详情附带文件路径 + 行号
