# dingtalk-workspace-cli

> 钉钉 Workspace CLI 操作指南 — AI Agent 一站式办公自动化

## 环境要求
- Node.js 18+
- 安装：`npm install -g @dingtalk/workspace-cli`
- GitHub: https://github.com/open-dingtalk

## 核心能力
首批开放的8大能力：AI表格、日历、日志、待办、机器人、通讯录、DING消息、考勤

### 1. DING消息（通知）
```bash
# 发送DING消息
dws ding send --title "紧急通知" --content "下午3点开会" --userIds "userid1,userid2"

# 通知到群
dws ding send --title "群通知" --content "见附件" --groupId "chat_id"

# 消息支持：文本、Markdown、链接、ActionCard
```

### 2. 待办管理
```bash
# 创建待办
dws todo create --title "完成报告" --dueTime "2026-07-05T18:00:00" --userIds "userid1"

# 查询待办
dws todo list --status "incomplete"

# 更新状态
dws todo update --taskId "xxx" --status "completed"
```

### 3. 日历管理
```bash
# 创建日程
dws calendar create --summary "项目评审" --startTime "2026-07-01T10:00:00" --endTime "2026-07-01T11:00:00"

# 查看日历来
dws calendar list --startTime "2026-07-01T00:00:00" --endTime "2026-07-31T23:59:59"
```

### 4. 日志汇报
```bash
# 写日报
dws log create --template "日报" --content "今日完成：项目开发..."

# 查看团队日志
dws log list --template "周报" --creator "userid1"
```

### 5. 通讯录
```bash
# 查询用户
dws contact getUser --userid "userid1"

# 查询部门
dws contact listDept --deptId "dept_id"
```

### 6. 考勤
```bash
# 查询打卡记录
dws attendance list --userIds "userid1,userid2" --date "2026-07-01"

# 查询请假审批
dws attendance getLeave --processInstanceId "xxx"
```

### 7. AI表格
```bash
# 创建工作表
dws sheet create --name "项目跟踪表" --fields "任务名称,负责人,状态,截止日期"

# 添加记录
dws sheet addRecord --sheetId "xxx" --data '{"任务名称":"开发完成","状态":"进行中"}'
```

### 8. 机器人管理
```bash
# 发送机器人消息
dws robot send --webhook "https://oapi.dingtalk.com/robot/send" --content "消息内容"

# 消息类型：text, markdown, link, actionCard, feedCard
```

## Agent 调用示例
```text
用户：在钉钉帮我创建一个日程，明天下午3点到4点，主题是"项目评审"

Agent执行：
dws calendar create -summary "项目评审" -startTime "2026-07-02T15:00:00" -endTime "2026-07-02T16:00:00"
```

## 鉴权配置
```bash
# 初始化
dws config init --appKey "dingxxx" --appSecret "xxx"

# 查看当前配置
dws config list
```

## 最佳实践
- DING消息适合紧急通知，群消息适合日常推送
- 日志模板提前在钉钉管理后台创建好
- 待办支持设置提醒时间（remindTime）
- 考勤数据按日查，大批量走批量接口

## 参考来源
- GitHub: https://github.com/open-dingtalk
- 文档: https://open.dingtalk.com
