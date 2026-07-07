# feishu-lark-cli-operations

> 飞书 CLI 操作指南 — 基于 @larksuite/cli 的企业办公自动化

## 环境要求
- Node.js 18+
- 安装飞书 CLI：`npx @larksuite/cli@latest install`
- 飞书开发者账号（开放平台）

## 核心能力
飞书 CLI 覆盖 **12个业务域**，200+命令，2500+ Raw API，专为Agent设计

### 1. 消息与群组
```bash
# 发送文本消息
lark send message text --content "消息内容" --receive_id "user_id"

# 发送卡片消息
lark send message card --file "./card.json" --receive_id "user_id"

# 获取消息列表
lark get message list --container_id "chat_id" --page_size 20

# 获取群组列表
lark get chat list --page_size 50
```

### 2. 云文档
```bash
# 创建文档
lark create document --title "项目报告" --folder_token "xxx"
lark create sheet --title "销售数据"
lark create docx --title "周报模板"

# 编辑文档
lark edit document --token "xxx" --content "新的内容"
```

### 3. 多维表格
```bash
# 创建多维表格
lark create base --title "项目管理"

# 添加记录
lark add base record --app_token "xxx" --table_id "tblxxx" --fields '{"name":"张三"}'

# 查询记录
lark get base records --app_token "xxx" --table_id "tblxxx"
```

### 4. 日历与会议
```bash
# 创建日程
lark create calendar event --summary "项目评审" --start_time "2026-07-01T10:00:00" --end_time "2026-07-01T11:00:00"

# 创建会议
lark create meeting --topic "周会" --start_time "2026-07-01T10:00:00" --duration 60
```

### 5. 通讯录与待办
```bash
# 查找用户
lark get user --user_id "xxx"

# 创建待办
lark create task --summary "完成报告" --due_at "2026-07-10T00:00:00"
```

## AI Agent Skills（24个内置）
飞书CLI内置Agent Skills，让AI清楚：
- 什么场景用什么命令
- 怎么鉴权
- 怎么处理错误
- 如何避免乱操作

## 鉴权
```bash
# 设置访问令牌
lark config set --app_id "xxx" --app_secret "xxx"
```

## 最佳实践
- 先获取access_token再发请求
- 消息优先使用卡片消息（更丰富的交互）
- 多维表格适合管理结构化数据（项目/任务/CRM）
- 云文档优先用docx格式（支持富文本）

## 参考来源
- GitHub: https://github.com/larksuite/cli
- 文档: https://open.feishu.cn
