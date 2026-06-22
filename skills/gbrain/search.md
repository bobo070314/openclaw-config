---
name: gbrain-search
description: gbrain 模块：搜索（语义 + 关键词混合）
---

# gbrain-search 模块

搜索是知识库的核心价值。gbrain 实现了三层递进式搜索：

```
用户查询 → 1. FTS5 全文搜索（关键词精确匹配）
         → 2. 语义搜索（向量余弦相似度）
         → 3. 混合排序（加权融合结果）
```

## 搜索模式

| 模式 | 命令 | 适用场景 |
|:-----|:-----|:---------|
| 全文搜索 | `search --mode text --query "关键词"` | 精确匹配术语、文件名、代码函数名 |
| 语义搜索 | `search --mode semantic --query "问题描述"` | 概念理解、找相关知识点 |
| 混合搜索 | `search --query "自然语言"` | **默认**，兼顾精确和模糊 |
| 图谱搜索 | `search --mode graph --query "实体名"` | 实体间关系探查 |

## 搜索质量

gbrain 的语义搜索质量取决于嵌入质量：
- **最佳**: 使用 dashscope text-embedding-v3（1024维，¥0.7/百万token）
- **中等**: OpenRouter text-embedding-3-small（512维，约 $0.02/百万token）
- **兜底**: 内置 TF-IDF 向量（无需网络，质量一般但永远可用）

## 输出格式

每项结果包含：
```
┌─────────────────────────────────────────┐
│ 得分: 0.92 | 类型: 文档段落             │
│ 来源: docs/api-guide.pdf (第2页)        │
│ 知识库: tech-docs                      │
│                                         │
│ 摘要: "API 认证使用 Bearer Token..."    │
│ 标签: [api, auth, security]             │
└─────────────────────────────────────────┘
```

## 跨知识库搜索

用户没有指定知识库时，自动搜索所有知识库：

```bash
node lib/search-all.js --query "<查询>" --limit 10
```
