# gbrain 多渠道发布

gbrain 知识库可通过多种渠道使用，无需进入终端。

## 📱 可用渠道

| 渠道 | 状态 | 说明 |
|:-----|:----:|:------|
| **Web 管理后台** | ✅ 已部署 | `http://localhost:3001` — 完整管理界面 |
| **REST API** | ✅ 已部署 | 端口 3001，支持搜索/添加/统计 |
| **MCP Server** | ✅ 已配置 | `gbrain` + `sandbox` 注册在 `mcp.servers` |
| **VS Code** | ✅ 可用 | `node ide.js` 直接索引项目 |
| **Cursor** | ✅ 可用 | 同 IDE 桥 |
| **CLI** | ✅ 可用 | `node commands/{kb,index,search,note,graph}.js` |
| **WebSocket** | ⬜ 待建 | 实时更新通知 |
| **微信小程序** | ⬜ 待部署 | 代码在 fullstack/miniapp/ |
| **Telegram Bot** | ⬜ 待建 | 知识库搜索机器人 |
| **Chrome 扩展** | ⬜ 待建 | 网页收藏到知识库 |

## 🚀 快速部署

```bash
# 1. 启动 REST API 服务器
cd skills/gbrain/fullstack
node server/index.js
# → 访问 http://localhost:3001

# 2. 索引当前项目到知识库
node lib/ide.js index project-knowledge D:\my-project

# 3. 安装 Ollama + 下载嵌入模型
ollama pull nomic-embed-text
ollama pull qwen2.5:7b

# 4. Web UI 独立使用
start skills/gbrain/gbrain.html
```

## 🔌 OpenClaw 集成

通过 MCP 自动暴露工具：

```bash
# 列出可用的 MCP 工具
openclaw mcp list

# gbrain 提供:
#   gbrain_search, gbrain_add, gbrain_stats
#   gbrain_list, gbrain_delete
# sandbox 提供:
#   sandbox_exec, sandbox_test
```

## 🔮 规划中

- Ollama 本地嵌入引擎（完全离线替代远程 LLM API）
- 知识库 RSS 订阅（自动抓取网页）
- 定时备份到 GitHub
- 知识库公共分享链接
- 浏览器扩展一键收藏
