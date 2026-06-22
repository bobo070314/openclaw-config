---
name: add-setting-env
description: 环境变量验证器，.env vs .env.example差异检测+敏感值脱敏+覆盖率统计
version: 0.2.0
status: implemented
category: dev
---

# add-setting-env — 环境变量验证器

## 定位
对比 `.env` 和 `.env.example`，检测缺失/多余的变量，统计覆盖率，敏感值脱敏。

## 触发条件
- "检查环境变量"
- "验证 .env 配置"
- "env 对比"
- "check environment variables"

## 工作流

1. **文件发现** — 搜索 `.env` 和 `.env.example`
2. **变量提取** — 解析 key=value（不读取真实值）
3. **差异检测**
   - `missing`: .env.example 有但 .env 没有 → ⚠️
   - `extra`: .env 有但 .env.example 没有 → ℹ️
   - `matched`: 两边都有 → ✅
4. **覆盖率计算** — `matched / total_in_example × 100%`
5. **脱敏输出** — 敏感值只显示 `***`

## 敏感 key 识别
```
API_KEY, SECRET, TOKEN, PASSWORD, PASSWD, ACCESS_KEY,
PRIVATE_KEY, AUTH_SECRET, DB_PASSWORD, REDIS_PASSWORD
```

## 关键约束
- 绝不读取 .env 的真实值（仅提取 key）
- 密码/Token 脱敏输出
- 支持注释行跳过（`#` 开头）
- 输出 Markdown 表格格式
