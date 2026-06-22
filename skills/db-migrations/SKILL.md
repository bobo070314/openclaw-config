---
name: db-migrations
description: Prisma跨平台迁移脚本，查环境变量+密码脱敏+生成迁移+部署
version: 0.2.0
status: implemented
category: dev
---

# db-migrations — 数据库迁移

## 定位
Prisma 数据库迁移的跨平台 Python 脚本。检查 DATABASE_URL 环境变量、执行迁移、密码脱敏输出。

## 触发条件
- "数据库迁移"
- "运行 prisma migrate"
- "同步数据库 schema"

## 工作流

1. **环境检查**
   - 验证 `DATABASE_URL` 是否存在
   - 密码脱敏：`postgresql://user:***@host:5432/db`
   - 检查 Prisma CLI 是否可用

2. **迁移生成**
   ```bash
   npx prisma migrate dev --name {name}
   ```

3. **部署**
   ```bash
   npx prisma migrate deploy
   ```

4. **状态验证**
   ```bash
   npx prisma migrate status
   ```

## 关键约束
- 跨平台：Python 实现（不依赖 bash）
- 安全：密码/连接串脱敏输出
- 幂等：多次运行不重复迁移
- 错误处理：连接失败给出明确的修复建议
