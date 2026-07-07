# OpenClaw Foreign 串道 QClaw — 完整修复记录

## 时间
2026-06-29 ~23:30 (GMT+8)

## 问题
`D:\bobo\openclaw-foreign\` 的 OpenClaw 实例（端口18900）总是串到 QClaw：
- 模型请求被 QClaw 拦截 → 403
- 回答风格变成 QClaw 那套
- "网不好上"（大模型接口被 QClaw 代理限流/拦截）

## 根因分析（三层串扰）

### 1️⃣ 系统环境变量被 QClaw 注册（最严重）
QClaw 安装时在系统/用户环境变量中注册了：
```
OPENCLAWS_CONFIG_PATH = C:\Users\asus\.qclaw\openclaw.json
QCLAW_LLM_BASE_URL    = http://127.0.0.1:19000/proxy/llm
OPENCLAW_STATE_DIR    = C:\Users\asus\.qclaw
```
导致 Foreign 启动时加载的是 **QClaw 的配置**，而非自己的配置。

### 2️⃣ QClaw 配置加载了 qclaw-plugin
`~\.qclaw\openclaw.json` 中：
```json
"plugins": {
  "load": {
    "paths": ["C:\\Program Files\\QClaw\\...\\extensions"]
  }
}
```
该路径下的 `qclaw-plugin` 注册了 `FetchMiddleware`（优先级280），劫持所有 LLM 请求并路由到 `jprx.m.qq.com`。

### 3️⃣ `.env` 无法覆盖系统环境变量
`run-gateway.cmd` 虽然加载 `.env` 设置 `OPENCLAW_CONFIG_PATH`，但 **系统环境变量优先级更高**，导致配置始终指向 QClaw。

## 所做修复

### ✅ 创建彻底隔离启动脚本
新建 `run-gateway-isolated.bat`，启动时强制：
1. **覆盖** `OPENCLAW_CONFIG_PATH` → 指向 Foreign 自己的 `openclaw.json`
2. **清空** `QCLAW_LLM_BASE_URL`、`QCLAW_LLM_API_KEY`、`QCLAW_PLUGIN_CONFIG_PATH`
3. **设置** `OPENCLAW_STATE_DIR` → 独立的 Foreign state 目录
4. **设置** `OPENCLAW_DISABLE_BUNDLED_PLUGINS=1` → 阻止自动扫描 QClaw 扩展
5. **设置独立 PATH** → 只包含 `D:\Program Files\nodejs` 和系统核心路径，排除 QClaw 的 node

### ✅ 清理 Foreign 配置
重写 `openclaw.json`：
- 移除 `plugins.allow` 中对 QClaw 插件的引用
- 移除无效的 `plugins.enabled: false` 顶层标志
- 添加 `skills.load.extraDirs` 指向 Foreign 自己的 skills 目录
- 保留 dashscope (qwen-turbo/flash) 模型配置

### ✅ 更新 `start-foreign.bat`
指向新的隔离启动脚本 `run-gateway-isolated.bat`

### ✅ 清理 QClaw plugan 目录（后恢复）
为避免破坏当前 QClaw agent 运行，恢复了 QClaw 扩展目录

## 如何使用
**正常启动（推荐）：**
```
D:\bobo\openclaw-foreign\start-foreign.bat
```
或直接：
```
D:\bobo\openclaw-foreign\run-gateway-isolated.bat
```

**手动检查：** 启动后访问 http://127.0.0.1:18900/webchat

## 后续注意
- 如果未来 QClaw 升级，需要检查是否新增了环境变量，并更新隔离启动脚本
- 如需在 Foreign 中添加更多模型，修改 `openclaw.json` 中 `models.providers` 部分
- 绝对不要将 QClaw 的 `OPENCLAW_CONFIG_PATH` 或 `QCLAW_LLM_BASE_URL` 写入系统级别
