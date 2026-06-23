# 企业微信 Channel 接入方案

## 方案概览

OpenClaw 国际版没有原生企微 Channel Provider（它更偏国际化平台，企微是微信生态特有）。
接入企业微信需要三层：

### 架构
```
企业微信 App → 企微 API Server → OpenClaw Webhook Inbound
                                    ↓
                              AI 处理消息
                                    ↓
OpenClaw → 企微 API (message/send) → 企微用户收到回复
```

### 接入步骤

#### 1. 创建企微自建应用
- 登录企业微信管理后台 https://work.weixin.qq.com/wework_admin/frame#apps
- 创建自建应用，获取：CorpID、AgentID、Secret
- 配置应用回调URL（指向你的公网 OpenClaw 地址）

#### 2. 配置环境变量
```bash
# Windows
setx WECOM_CORPID "your_corpid"
setx WECOM_CORPSECRET "your_corpsecret"  
setx WECOM_AGENTID "1000002"
setx WECOM_TOKEN "your_token"      # 回调验证
setx WECOM_ENCODING_AES_KEY "your_key"  # 消息加解密
```

#### 3. 启用 wecomcli 技能
```bash
# 测试连接
python skills/wecomcli-setup/run.py check

# 查看诊断
python skills/wecomcli-setup/run.py diagnose

# 发送第一条消息
python skills/wecomcli-msg/run.py send --to "@all" --text "OpenClaw 已上线 🚀"
```

#### 4. 企微回调接收（Webhook）
由于 OpenClaw 没有原生企微 Channel，需要部署一个轻量 Python Webhook 桥接：
- 接收企微回调消息
- 转发给 OpenClaw API
- 将 OpenClaw 回复送回企微

#### 5. 快捷方案：用第三方桥接
- **ClawdBot** / **QClaw** 已实现企微 Channel（它们的 electron 版本内置了企微接入）
- 中国用户推荐直接用 QClaw（端口 18789），企微/微信/钉钉即插即用

## 当前状态
- ✅ wecomcli-* 8 个技能全部可实现 API 调用（只需配置 corpid/secret）
- ✅ wecom-weisheng-scrm 微盛SCRM完整技能就绪
- ⚠️ 企微消息双向收发需要额外 Webhook 桥接层
- 💡 推荐方案：QClaw（18789）作为企微消息入口，OpenClaw（18791）作为国际能力平台

## 快速开始
配置好 WECOM_CORPID / WECOM_CORPSECRET / WECOM_AGENTID 后：
```bash
# 1. 初始化
python skills/wecomcli-setup/run.py init --corpid "$CORPID" --secret "$SECRET" --agentid "$AGENTID"

# 2. 检查连接
python skills/wecomcli-setup/run.py check

# 3. 发送测试消息
python skills/wecomcli-msg/run.py send --to "@all" --text "OpenClaw 准备就绪"
```
