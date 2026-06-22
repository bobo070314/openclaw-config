---
name: frontend-code-review
description: ESLint增强前端代码审查，符号交叉引用+修复建议+质量评分
version: 0.2.0
status: implemented
category: dev
---

# frontend-code-review — 前端代码审查

## 定位
对 React/Next.js/Vue 前端代码做 ESLint 增强审查，包含符号交叉引用分析、修复建议和质量评分。

## 触发条件
- "审查前端代码"
- "前端代码规范检查"
- "check frontend code quality"

## 审查维度

| 维度 | 检查内容 |
|------|----------|
| 组件规范 | 组件命名、props 类型、导出方式 |
| React Hooks | 依赖数组完整性、useEffect 清理 |
| 性能 | 不必要的 re-render、缺少 memo/useMemo |
| 可访问性 | aria 属性、语义化 HTML、键盘导航 |
| 样式 | CSS-in-JS 规范、Tailwind class 顺序 |
| 状态管理 | zustand/store 使用规范 |

## 工作流
1. **ESLint 扫描** — 基于项目 eslint 配置运行
2. **符号交叉引用** — 调 `code-navigator` 分析组件依赖
3. **手动规则** — ESLint 之外的 AI 审查规则
4. **评分** — 0-100 质量评分 + 分维度打分
5. **修复建议** — 每条问题附带修复代码

## 关键约束
- 读取项目现有的 eslint 配置，不覆盖
- 修复建议可执行（完整的代码片段）
- 质量评分配置透明（权重可调）
