# workflow-automation-n8n

> 自动化工作流引擎 Skill — 基于 n8n 的工作流设计与执行

## 环境要求
- Docker 或 n8n 自托管
- n8n 支持 400+ 集成节点（HTTP, Email, Database, AI, Slack, GitHub 等）

## 核心概念
- **Workflow**：自动化流程（DAG）
- **Node**：单个操作步骤
- **Trigger**：触发节点（Webhook, Cron, Email, etc.）
- **Action**：执行节点（HTTP请求, 数据库操作, AI调用）
- **Credential**：认证凭据

## 常用工作流模板

### 1. Webhook → 数据处理 → 通知

```
[Webhook Trigger] → [Set/Filters] → [HTTP Request] → [Slack/Send Email]
```

### 2. 定时任务 → 数据同步

```
[Cron Trigger] → [Database Query] → [Transform] → [API Update]
```

### 3. AI + 自动化

```
[Webhook] → [HTTP Get Data] → [OpenAI Node] → [DB Insert] → [Email Alert]
```

## 关键操作

### HTTP Request 节点
```json
{
  "method": "POST",
  "url": "https://api.example.com/data",
  "authentication": "genericCredentialType",
  "sendQuery": true,
  "sendBody": true,
  "options": {}
}
```

### 数据转换
```javascript
// Function Node 代码
items.map(item => ({
  json: {
    id: item.json.id,
    processed_at: new Date().toISOString(),
    result: processData(item.json.raw)
  }
}));

function processData(raw) {
  // 自定义处理逻辑
  return raw.trim().toUpperCase();
}
```

### 条件分支
```json
{
  "conditions": {
    "string": [
      {
        "value1": "={{$json.status}}",
        "operation": "equal",
        "value2": "success"
      }
    ]
  }
}
```

## 部署方式

### Docker Compose
```yaml
version: '3'
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
    environment:
      - N8N_SECURE_COOKIE=false
      - WEBHOOK_URL=https://your-domain.com/

volumes:
  n8n_data:
```

### 导出/导入工作流
```bash
# 导出所有工作流
# 设置 → 下载工作流
# 或通过 API:
curl -X GET http://localhost:5678/rest/workflows \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 集成提醒
- **数据库**: PostgreSQL, MySQL, MongoDB, MariaDB
- **AI**: OpenAI, Anthropic, Ollama, Hugging Face
- **消息**: Slack, Discord, Telegram, Email (SMTP)
- **存储**: S3, Google Drive, Dropbox, OneDrive
- **开发**: GitHub, GitLab, Jira, Linear

## 最佳实践
- 多步骤复杂工作流拆成子工作流（Sub-workflow Node）
- 敏感凭证存 Credential，不硬编码
- 每步设 Error Handler 节点处理失败
- 日志开启：`N8N_LOG_LEVEL=debug`
- 生产部署加反向代理和 HTTPS

## 参考来源
- 项目：gh-enterprise-baseline/n8n
- 文档：https://docs.n8n.io
