# database-orm-prisma

> 数据库 ORM 操作专家 Skill — 基于 Prisma ORM 的数据库操作指南

## 环境要求
- Node.js 18+
- Prisma CLI（`npx prisma`）
- 支持 PostgreSQL, MySQL, SQLite, SQL Server, MongoDB (预览)

## 使用场景
- 数据库 schema 设计与迁移
- CRUD 操作
- 关联查询与聚合
- 事务与批量操作
- 数据库 Seed 数据填充

## 操作指南

### 1. schema 创建

```
npx prisma init
```

### 2. 常用 CRUD 模板

```prisma
// schema.prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
}
```

### 3. 核心操作

```typescript
// 创建
const user = await prisma.user.create({
  data: { email: 'test@test.com', name: 'Test' }
})

// 查询（含关联）
const users = await prisma.user.findMany({
  where: { email: { contains: 'test' } },
  include: { posts: true }
})

// 更新
await prisma.user.update({
  where: { id: 'xxx' },
  data: { name: 'New Name' }
})

// 删除
await prisma.user.delete({ where: { id: 'xxx' } })

// 事务
await prisma.$transaction([
  prisma.user.update(...),
  prisma.post.create(...)
])

// 聚合
const total = await prisma.user.count()
const avg = await prisma.post.aggregate({ _avg: { likes: true } })
```

### 4. 迁移管理

```bash
# 创建迁移
npx prisma migrate dev --name init

# 应用迁移（生产）
npx prisma migrate deploy

# 查看状态
npx prisma migrate status

# 重置数据库
npx prisma migrate reset
```

### 5. 生成客户端

```bash
npx prisma generate
```

## 最佳实践
- 始终用 `@unique` 标记唯一字段
- 关联查询用 `select` 代替 `include` 以提升性能（只取需要字段）
- 批量操作用 `createMany`/`updateMany` 代替循环
- 迁移文件 `prisma/migrations/` 要提交到 Git
- 生产环境用 `migrate deploy` 而不是 `migrate dev`

## 参考来源
- 项目：gh-enterprise-baseline/prisma
- 文档：https://www.prisma.io/docs
