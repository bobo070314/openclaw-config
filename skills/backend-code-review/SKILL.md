---
name: backend-code-review
description: >
  Python backend code review + security audit. Runs pylint/flake8 linting,
  AST-based Django/FastAPI pattern detection (views, ORM queries, routers,
  dependency injection), and 10-category security scan (SQL injection,
  N+1 queries, hardcoded secrets, unsafe deserialization, eval/exec,
  command injection, DEBUG=True, ALLOWED_HOSTS wildcard, CSRF bypass).
  Generates markdown report with risk levels (HIGH/MEDIUM/LOW) and fix
  examples. Use when user says "review backend", "audit Python code",
  "security scan", "check Django/FastAPI", "backend code review".
version: 0.2.0
status: implemented
category: dev
---

# Backend Code Review & Security Audit

## 定位
Python 后端代码三层审查引擎。Lint 检查 + AST 框架检测 + 10 条安全规则扫描，覆盖 SQL 注入、N+1 查询、硬编码密钥、不安全反序列化、eval/exec、命令注入、生产配置错误等。输出 Markdown 报告 + 风险分级 + 修复示例。

## 触发条件
- 用户说"review backend" / "audit Python code" / "security scan"
- "check Django/FastAPI project" / "find vulnerabilities"
- 部署前安全审计 / PR 质量门禁

## 工作流
1. **Lint 层** — pylint（主）或 flake8（回退），JSON 解析输出
2. **AST 框架检测** — 识别 Django views、FastAPI endpoints、ORM 查询模式、路由注册
3. **安全扫描** — 10 条规则逐行正则匹配，附风险等级和行号
4. **报告生成** — 风险分级 + 修复示例，支持 markdown/text/json 输出

## 10 条安全规则

| Rule ID | Name | Risk |
|---------|------|------|
| SEC-001 | SQL Injection — raw SQL with f-string/format/%s | 🔴 HIGH |
| SEC-002 | SQL Injection — Django .raw()/.extra() with interpolated values | 🔴 HIGH |
| SEC-003 | Potential N+1 query — ORM in loop without prefetch | 🟡 MEDIUM |
| SEC-004 | Hardcoded secret (password/token/key/API key) | 🔴 HIGH |
| SEC-005 | Unsafe deserialization — pickle.loads/yaml.load | 🔴 HIGH |
| SEC-006 | Dynamic code execution — eval()/exec()/compile() | 🔴 HIGH |
| SEC-007 | DEBUG=True — production misconfiguration | 🟡 MEDIUM |
| SEC-008 | ALLOWED_HOSTS=['*'] — Django wildcard | 🟡 MEDIUM |
| SEC-009 | Command injection — os.system/subprocess shell=True | 🔴 HIGH |
| SEC-010 | Missing CSRF protection — @csrf_exempt | 🟡 MEDIUM |

## 关键约束
- 退出码 0 = 无 HIGH 级别发现，1 = 有 HIGH 级别
- 支持单文件（--file）和目录扫描（--src）双模式
- 配合 code-navigator 获取符号定义上下文
