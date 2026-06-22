---
name: code-navigator
description: 符号级代码导航，识别函数/类/接口/导出/导入，支持模糊搜索
version: 0.2.0
status: implemented
category: dev
---

# code-navigator — 符号级代码导航

## 定位
在项目中定位任何符号（函数、类、接口、导出、导入），支持精确匹配和模糊搜索。为 `infra-diagram-as-code` 和 `frontend-code-review` 提供底层符号提取能力。

## 触发条件
- "找到 xxx 函数在哪里定义"
- "搜索 xxx 类"
- "这个 interface 在哪儿用的"
- "查找所有 API endpoint"

## 工作流

1. **符号扫描**
   - Python: 扫描 `def`、`class`、`@app.get|post`
   - TypeScript/JS: 扫描 `function`、`class`、`interface`、`type`、`export`
   - Go: 扫描 `func`、`type`、`struct`、`interface`

2. **符号分类**
   - API Endpoints: `@app.get|post|put|delete` / `app.get|post|put|delete`
   - Data Models: SQLAlchemy / Prisma / Drizzle schema definitions
   - Middleware: `app.use` / `@app.middleware` / decorators

3. **交叉引用**
   - 追踪 import → usage 关系
   - 识别哪些文件使用了某个符号

## 命令示例
```bash
# 搜索 API endpoint 定义
grep -rn "@app\.(get|post|put|delete|patch)" --include="*.py"

# 搜索函数定义
grep -rn "^def \|^async def " --include="*.py"

# 搜索 TypeScript 导出
grep -rn "export (const|function|class|interface|type)" --include="*.ts"
```

## 关键约束
- 不分析 node_modules / .next / dist
- 输出包含文件路径 + 行号 + 上下文
- 与 `infra-diagram-as-code` 链式集成
