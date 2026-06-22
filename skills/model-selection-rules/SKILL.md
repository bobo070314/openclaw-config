---
name: model-selection-rules
description: 模型选择与降级策略。定义主模型、fallback 链、network-unreachable 检测和 Chinese API 优先逻辑。
---

# Skill: 模型选择规则 (model-selection-rules)

## 当前配置

| 优先级 | 模型 | 说明 |
|--------|------|------|
| 🥇 primary | `deepseek/deepseek-v4-pro` | 主力模型，推理能力强 |
| 🥈 fallback #1 | `moonshot/kimi-k2.6` | 国内直达，备选主力 |
| 🥉 fallback #2 | `deepseek/deepseek-v4-flash` | 同系列降级，更快 |
| #3 | `google/gemini-3.5-flash` | Google 系，**网络不可达时跳过** |
| #4 | `doubao/doubao-seed-2-0-lite-260428` | 字节豆包，国内直达 |
| #5 | `zhipu/glm-4-flash` | 智谱，国内直达 |
| #6 | `siliconflow/Qwen/Qwen3-8B` | SiliconFlow 通义，国内直达 |
| #7 | `dashscope/qwen-flash` | 阿里 DashScope，国内直达 |
| #8 | `siliconflow/deepseek-ai/DeepSeek-V4-Flash` | 同上模型不同 provider |
| #9 | `google/gemini-2.5-flash` | Google 旧版，**网络不可达时跳过** |
| #10 | `google/gemma-4-31b-it` | Google 系，**网络不可达时跳过** |
| 💀 | `noFallback` | 终止标志：全部不通则报错 |

## 降级规则

1. **模型不可用 → 自动 fallback 到下一个**
   - 429 rate limit、401 auth error、timeout、model not found
   - Gateway 内置 fallback 链，无需手动切换

2. **网络不可达 → 跳过 Google 系**
   - `google/*` 系列在中国大陆可能不可达
   - 当 `web_search`/`web_fetch` 失败时，优先走国内模型

3. **免费优先**
   - `siliconflow/Qwen/Qwen3-8B`（第 6 位）— 免费额度充足，长对话推荐
   - `dashscope/qwen-flash`（第 7 位）— 阿里免费额度
   - `deepseek/deepseek-v4-flash`（第 2 位）— 高速低成本

4. **Embedding 专用模型**
   - 仅用 `dashscope/text-embedding-v3`（已配入 agents.defaults.memorySearch）
   - 不与对话模型争配额

## 什么情况下需要人为干预

| 场景 | 操作 |
|------|------|
| 所有 fallback 全挂 | 检查网络/API Key 状态 |
| memory search 索引消失 | 检查 DashScope 配额 |
| 推理质量明显下降 | 临时切 fallback #1（moonshot/kimi-k2.6） |
