---
name: gbrain-index
description: gbrain 模块：文档索引（文件、网页、代码仓库）
---

# gbrain-index 模块

文档索引是知识库的核心入口。将各种来源的内容解析、分块、嵌入、存储。

## 索引流程

```
源文件 → 读取 + 解析 → 分块(chunking) → 生成嵌入 → 写入 SQLite + 向量索引
```

## 分块策略

| 文档类型 | 分块策略 | 块大小 | 重叠 |
|:---------|:---------|:------:|:----:|
| TXT/MD 文本 | 按段落 + 语义边界 | 512 token | 64 token |
| PDF | 按页面 + 段落 | 512 token | 64 token |
| DOCX | 按段落 | 512 token | 64 token |
| 代码文件 | 按函数/类定义 | 256 token | 32 token |
| 网页 (URL) | 按章节标题 | 512 token | 64 token |

## 支撑库

gbrain 使用以下 Node.js 依赖（自动安装）：

```bash
cd D:\bobo\openclaw-foreign
npm install better-sqlite3 --no-optional 2>&1 | tail -3
```

## 嵌入生成

使用配置中的 LLM 提供商做嵌入：

### 方案 A：用 API 模型（如 dashscope 的 text-embedding-v3）

```bash
CREDS=$(cat "$GBRAIN_ROOT/config.json" | node -e "process.stdin.resume();let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{const c=JSON.parse(d);console.log(c.apiKey||'')})")
curl -s -X POST "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding" \
  -H "Authorization: Bearer $CREDS" \
  -H "Content-Type: application/json" \
  -d '{"model":"text-embedding-v3","input":"<TEXT>","parameters":{"dimension":1024}}'
```

### 方案 B：用本地 js 嵌入（无依赖，轻量）

`lib/embed.js` 中内置了一个简化词向量计算器（Bag-of-words + TF-IDF 加权），用于首次使用无需任何依赖。

### 方案 C：用 OpenRouter 嵌入 API

```bash
curl -s "https://openrouter.ai/api/v1/embeddings" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"text-embedding-3-small","input":"<TEXT>"}'
```

## 具体操作

### 索引单个文件

```bash
node lib/index-file.js --kb <知识库名> --file <文件路径>
```

### 索引整个目录

```bash
node lib/index-dir.js --kb <知识库名> --dir <目录路径> --recursive
```

### 收藏网页

```bash
node lib/index-url.js --kb <知识库名> --url <URL>
```

### 索引代码仓库

```bash
node lib/index-code.js --kb <知识库名> --repo <Git仓库路径>
```

这个命令会自动：
1. 识别 git 仓库结构
2. 按语言过滤（忽略 node_modules、.git、dist 等）
3. 每个函数/类提取为独立块
4. 保持文件路径关联
