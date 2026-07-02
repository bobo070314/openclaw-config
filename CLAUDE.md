# CLAUDE.md - Boss OpenClaw 项目指令

## 项目概述
Five-Story Building OpenClaw 系统，管理 IGP 引擎 v5/v6、Family-Corp Teams（16个子系统）。

## 核心命令
```powershell
# 启动网关
$env:OPENCLAW_CONFIG_PATH = 'openclaw-minimal.json'
node.exe openclaw\openclaw.mjs gateway --port 18900
```

```powershell
# 心跳检测
python family-corp-teams/v5/v6/api/igp_heartbeat.py
```

```powershell
# 关闭网关
taskkill /F /IM node.exe
```

## Agent 配置
- main: deepseek/deepseek-v4-flash (主力对话)
- coding: zhipu/glm-4-flash-250315 (代码主力)
- reasoning: tencent/hunyuan-lite (推理)
- chat: deepseek/deepseek-v4-flash (日常)

## 模型配置
/model deepseek/deepseek-v4-flash
CALIBER_MODEL=deepseek/deepseek-v4-flash

```json
{
  "model": "deepseek/deepseek-v4-flash",
  "temperature": 0.7,
  "maxTokens": 4096
}
```

## 目录结构
- /family-corp-teams/v5/chromosomes/a2a/development.json
- /family-corp-teams/v5/chromosomes/a2a/digest.json
- /family-corp-teams/v5/chromosomes/a2a/fission.json
- /family-corp-teams/v5/chromosomes/a2a/mutation.json
- /family-corp-teams/v5/chromosomes/a2a/upgrade.json
- /family-corp-teams/v5/silicon_memory_pkg/episodic.json
- /family-corp-teams/v5/silicon_memory_pkg/procedural.json
- /family-corp-teams/v5/silicon_memory_pkg/semantic.json
- /family-corp-teams/v5/absorb/docagent/v5_job_engine.py
- /family-corp-teams/v5/v6/api/igp_heartbeat.py

## 技能目录
skills/ — 85+ 个技能
