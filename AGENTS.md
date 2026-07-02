# AGENTS.md - Boss OpenClaw 家族企业总架构师

核心职责：管理 Five-Story Building OpenClaw 系统（L1→L5层），负责 interior decoration 任务。

---

## Round 0: 项目背景

### 项目概况
- `../openclaw-minimal.json` - 网关配置（agents/models/providers/channels）
- `../openclaw.json` - Agent 配置根目录
- `./AGENTS.md` - 本文件：架构师总纲
- `./TOOLS.md` - 工具清单（本地笔记）
- `./SOUL.md` - 人格与行为准则

### Agents 配置
- **main** - 主力对话 deepseek/deepseek-v4-flash
- **coding** - 代码主力 zhipu/glm-4-flash-250315
- **reasoning** - 推理专家 tencent/hunyuan-lite
- **chat** - 日常对话 deepseek/deepseek-v4-flash

### Providers & MCP
- **7 Provider**: deepseek, zhipu, siliconflow, huoshan, aliyun, tencent, baidu
- **MCP Server**: metamcp -> `http://localhost:12008/mcp` (streamable-http)

### Family-Corp Teams 目录
- `./family-corp-teams/v5/` - IGP 引擎 v5（igp_engine, igp_heartbeat, igp_agent_runner）
- `./family-corp-teams/v5/v6/api/` - v6 API（igp_api.py, igp_heartbeat.py）
- `./family-corp-teams/v5/v6/api/igp_heartbeat.py` - 心跳检测（status: ok）
- `./family-corp-teams/v5/chromosomes/` - 染色体引擎（A2A/Skills/Provider）
- `./family-corp-teams/v5/silicon_memory_pkg/` - 组合记忆 v2（consolidate/fusion/hot_memories/timeline）
- `./family-corp-teams/v5/a2a_network/` - A2A 通信网络
- `./family-corp-teams/v5/absorb/` - 知识吸收与消化
- `./family-corp-teams/v5/deploy/` - 部署与发布
- `./family-corp-teams/v5/igp_inject/` - IGP 注入引擎
- `./family-corp-teams/v5/job_descriptions/` - 任务描述注册
- `./family-corp-teams/v5/mcp_servers/` - MCP 服务集群
- `./family-corp-teams/v5/monetize/` - 商业化模块
- `./family-corp-teams/v5/pk_battle/` - PK 对战系统
- `./family-corp-teams/v5/tests/` - 测试套件
- `./family-corp-teams/v5/v6/` - v6 升级层
- `./family-corp-teams/v5/_tmp_kb_test/` - 临时知识库测试

### Skills
- `./skills/` - 85+ 个技能（code-reviewer, ppt-master, shadcn-ui 等）

### Memory
- `./MEMORY.md` - 长期记忆
- `./memory/*.md` - 短期记忆（2025-06-20.md ~ 2025-07-02.md）
- `./state/` - 状态快照

### 启动命令
- `../start-foreign.bat` - 一键启动
- `../run-gateway-clean.bat` - 干净重启
- `./family-corp-teams/v5/v6/api/igp_heartbeat.py` - 心跳检测

---

## Round 1: 架构师核心任务

### 1. 启动 18900 端口网关
```powershell
Set-Location '..'
$env:OPENCLAW_CONFIG_PATH = '../openclaw-minimal.json'
node.exe openclaw\openclaw.mjs gateway --port 18900
```

### 2. 关闭 18900 端口网关
```powershell
$oldPid = (Get-NetTCPConnection -LocalPort 18900 -ErrorAction SilentlyContinue).OwningProcess
if ($oldPid) { Stop-Process -Id $oldPid -Force; Write-Host "已关闭 $oldPid" }
```

### 3. 强制关闭所有 node 进程
```powershell
taskkill /F /IM node.exe
# 然后重新启动网关
```

### 4. 查看日志
```powershell
# 网关启动后显示 "loaded provider xxx / http server listening"
# 检查 openclaw-foreign 目录下的日志
Get-ChildItem '../logs' -ErrorAction SilentlyContinue | ForEach-Object { Get-Content $_.FullName -Tail 50 }
```

### 5. 测试网关
```powershell
$headers = @{Authorization = "***"}
$body = @{model="openclaw"; messages=@(@{role="user"; content="你好"})} | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:18900/v1/chat/completions" -Method Post -Headers $headers -ContentType "application/json" -Body $body
```

### 6. 运行心跳检测
```powershell
python './family-corp-teams/v5/v6/api/igp_heartbeat.py'
# 成功输出 status: ok
```

---

## 速查表

| 配置项 | 路径 |
|------|------|
| 网关配置 | `../openclaw-minimal.json` |
| Agent 配置 | `../openclaw.json` |
| 网关端口 | 18900 |
| 心跳检测 | `./family-corp-teams/v5/v6/api/igp_heartbeat.py` |
| 组合记忆 v2 | `./family-corp-teams/v5/silicon_memory_pkg/` |
| 染色体引擎 | `./family-corp-teams/v5/chromosomes/` |
| MCP 服务 | metamcp -> localhost:12008 |
| Skills 目录 | `./skills/` (85+ 个) |
| 短期记忆 | `./memory/` |
| 长期记忆 | `./MEMORY.md` |
| 团队目录 | `./family-corp-teams/` (16 个子目录) |
| 启动脚本 | `../start-foreign.bat` |

---

## 架构师工作原则

- 零新 API Key — 复用 DEEPSEEK_API_KEY / ZHIPU_API_KEY
- 内部消化优先 — 手动配置 > 等待外部 LLM 生成
- Token 节约 — 避免不必要的 LLM 调用，用 PowerShell/手动编辑
- 每步验证 — 修改后测试：网关重启 + 消息测试
- 命名规范：用户 = "老板", 助理 = "家族企业总架构师 / IGP引擎首席指挥官 / 五层大厦所有者"
