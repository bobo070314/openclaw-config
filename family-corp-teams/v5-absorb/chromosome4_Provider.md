# 染色体4: Provider路由部 - 吸收报告

## 1. OpenCode 提供商列表 (2026)

OpenCode 支持 **75+ LLM 提供商**，包括：
- OpenCode Zen
- OpenCode Go
- Amazon Bedrock
- Azure
- Baseten
- Cerebras
- Cloudflare AI Gateway
- Fireworks AI
- Moonshot AI
- OVHcloud AI Endpoints
- Together AI
- Venice AI
- Vercel AI Gateway
- Z.AI

这些提供商可以通过 `/connect` 命令添加到 OpenCode 配置中。

## 2. Cline 提供商抽象模型路由器 (2026)

Cline 的设计哲学是模型无关性，允许用户通过提供商、聚合器或本地模型路由任务。Cline 可以与以下路由器集成：
- Bifrost（由 Maxim AI 开发的开源 AI 网关）
- Braintrust（提供基于质量的模型选择）
- OpenRouter（通过单个 API 访问多种语言模型）

这些路由器可以优化成本、速度和隐私。

## 3. AI 模型定价比较 (2026)

| 模型 | 输入价格 (每百万 tokens) | 输出价格 (每百万 tokens) | 上下文长度 | 备注 |
|------|------------------------|------------------------|------------|------|
| GPT-5.5 | $5 | $30 | 1M | 顶级编码模型 |
| Claude Opus 4.8 | $5 | $25 | 1M | 顶级编码模型 |
| Gemini 3.1 Pro | $2 | $12 | 1M | 最佳价值 |
| DeepSeek V4 Flash | $0.14 | $0.28 | 1M | 最便宜的 LLM API |
| Qwen3.7 Max | $7.50 | $7.50 | 1M | 与 GLM-5.2 竞争 |
| GLM-5.2 | $4.40 | $4.40 | 1M | MIT 开源 |

## 4. 结论

OpenCode 支持广泛的 LLM 提供商，并且 Cline 提供了灵活的模型路由解决方案。在定价方面，DeepSeek V4 Flash 是最经济的选择，而 GPT-5.5 和 Claude Opus 4.8 在编码任务中表现最佳。