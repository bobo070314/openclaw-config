# backend-supabase-operations

> Supabase 后端服务专家 Skill — 数据库/认证/存储/实时订阅操作指南

## 环境要求
- Supabase 项目（cloud 或 self-hosted）
- Supabase JS Client: `npm install @supabase/supabase-js`
- 环境变量: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`

## 核心模块

### 1. 数据库操作（PostgreSQL + Row Level Security）

```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_ANON_KEY!
)

// 查询
const { data, error } = await supabase
  .from('users')
  .select('*')
  .eq('status', 'active')
  .order('created_at', { ascending: false })
  .limit(10)

// 关联查询
const { data: posts } = await supabase
  .from('posts')
  .select(`
    id,
    title,
    author:users(id, name)
  `)

// 插入
const { data, error } = await supabase
  .from('todos')
  .insert({ title: 'Hello', user_id: userId })
  .select()

// 更新
await supabase
  .from('todos')
  .update({ completed: true })
  .eq('id', todoId)

// 删除
await supabase
  .from('todos')
  .delete()
  .eq('id', todoId)

// RPC 调用
const { data } = await supabase.rpc('increment', { row_x: 1 })
```

### 2. 认证系统

```typescript
// 邮箱注册
const { data, error } = await supabase.auth.signUp({
  email: 'user@test.com',
  password: 'securePass123'
})

// 登录
const { data } = await supabase.auth.signInWithPassword({
  email: 'user@test.com',
  password: 'securePass123'
})

// OAuth
await supabase.auth.signInWithOAuth({ provider: 'github' })

// 会话管理
const { data: { session } } = await supabase.auth.getSession()
const user = session?.user

// 登出
await supabase.auth.signOut()

// 密码重置
await supabase.auth.resetPasswordForEmail('user@test.com')

// 用户管理（服务端）
// 需要用 service_role_key
await supabaseAdmin.auth.admin.createUser({ email, password })
await supabaseAdmin.auth.admin.deleteUser(userId)
```

### 3. 存储管理

```typescript
// 上传文件
const { data, error } = await supabase.storage
  .from('avatars')
  .upload('public/user1.jpg', file, {
    cacheControl: '3600',
    upsert: false
  })

// 下载
const { data } = await supabase.storage
  .from('avatars')
  .download('public/user1.jpg')

// 获取公开URL
const { data: { publicUrl } } = supabase.storage
  .from('avatars')
  .getPublicUrl('public/user1.jpg')

// 删除
await supabase.storage
  .from('avatars')
  .remove(['public/user1.jpg'])

// 创建Bucket
await supabaseAdmin.storage.createBucket('documents', {
  public: false,
  allowedMimeTypes: ['application/pdf'],
  fileSizeLimit: 10485760
})
```

### 4. 实时订阅

```typescript
// 监听数据库变化
const channel = supabase
  .channel('todos-changes')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'todos',
      filter: `user_id=eq.${userId}`
    },
    (payload) => {
      console.log('Change received!', payload)
    }
  )
  .subscribe()

// 取消订阅
supabase.removeChannel(channel)
```

### 5. SQL 边缘函数

```typescript
// Database Functions 是 PostgreSQL 函数
// 创建（Supabase SQL Editor 中执行）
`
CREATE OR REPLACE FUNCTION increment(x int)
RETURNS int AS $$
  SELECT x + 1;
$$ LANGUAGE SQL;
`

// 调用
const { data } = await supabase.rpc('increment', { x: 42 })
```

### 6. Row Level Security (RLS)

```sql
-- 启用 RLS
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;

-- 用户只能看自己的数据
CREATE POLICY "Users can view own todos"
ON todos FOR SELECT
USING (auth.uid() = user_id);

-- 用户只能插入自己的数据
CREATE POLICY "Users can insert own todos"
ON todos FOR INSERT
WITH CHECK (auth.uid() = user_id);
```

## 最佳实践
- 客户端始终用 `anon_key` + RLS 控制权限
- `service_role_key` 仅在服务端/后台使用（绕过 RLS）
- 大型数据集加 `.limit()` 和 `.range(from, to)` 分页
- 实时订阅数不要超过 200 concurrent connections
- 存储文件用 `upsert: false` 避免意外覆盖
- SQL 函数使用 `SECURITY DEFINER` 时注意权限

## 参考来源
- 项目：gh-enterprise-baseline/supabase
- 文档：https://supabase.com/docs
