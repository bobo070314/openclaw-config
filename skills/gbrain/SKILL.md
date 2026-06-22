---
name: gbrain
description: >-
  🌍 AI 知识大脑 — 国际版独占的本地 RAG 知识库系统。
  支持文件索引、语义搜索、知识图谱、笔记管理等。
  当用户提到知识库、资料库、笔记、收藏、"记下来"、"存起来"、"搜索一下知识"时，
  或需要持久化记忆、文件管理、代码仓库索引时触发。
  比腾讯 IMA 知识库更强大：本地运行、无限存储、毫秒级检索、支持代码索引、支持多模态。
homepage: https://github.com/openclaw
metadata:
  openclaw:
    emoji: '🧠'
    primaryEnv: 'GBRAIN_ROOT'
---

# 🧠 gbrain — 全球知识大脑

> 🔒 **国际版独占** — 知识库数据使用 AES-256-CBC 加密存储，仅国际版环境可解密。
> 国际版独占的本地 RAG 知识库系统，比腾讯 IMA 更强大。
> **完全离线运行 | 零 API 费用 | 无限存储 | 毫秒级检索**

## 🔐 独占锁定

gbrain 采用**三层独占锁定机制**，确保国内版无法访问知识库数据：

| 层 | 机制 | 说明 |
|:--|:-----|:-----|
| 1️⃣ 环境指纹 | 运行时检测 | 端口 18791 + 配置路径 + IDENTITY.md 联合校验 |
| 2️⃣ 数据加密 | AES-256-CBC | store.json 文件使用密钥派生后加密存储 |
| 3️⃣ 入口守卫 | 构造函数拦截 | Storage 类实例化时自动触发环境校验 |

退出令牌（指纹水印）: `GBRAINA1F77167`

## 能力总览

| 能力 | 描述 | IMA | gbrain |
|:-----|:-----|:---:|:------:|
| 文件上传索引 | PDF、DOCX、TXT、MD → 向量化 | ✅ | ✅ **更强** |
| 语义搜索 | 关键词 + 向量混合搜索 | ✅ | ✅ 毫秒级本地 |
| 网页收藏 | URL → 知识库 | ✅ | ✅ |
| 笔记管理 | 创建/编辑/搜索笔记 | ✅ | ✅ |
| 代码索引 | 仓库结构 + 代码语义搜索 | ❌ | ✅ **独占** |
| 知识图谱 | 实体关联可视化 | ❌ | ✅ **独占** |
| 全文搜索 | SQLite FTS5 全文检索 | ❌ | ✅ **独占** |
| 多知识库 | 隔离空间 | ❌ | ✅ **独占** |
| 离线运行 | 无需联网 | ❌ | ✅ **独占** |
| 零费用 | 无 API 配额 | ❌ | ✅ **独占** |
| 自动标签 | AI 自动分类 | ❌ | ✅ **独占** |

## 数据存储

所有数据存储在 `D:\bobo\openclaw-foreign\state\gbrain\` 下：

```
state/gbrain/
├── <kb_name>/          # 每个知识库一个目录
│   ├── data.db         # SQLite 主库 (含 FTS5 全文索引)
│   ├── vectors.bin     # 向量索引 (FAISS 或二进制)
│   └── files/          # 原始文件副本
├── config.json         # 全局配置
└── embeddings/         # 本地嵌入模型缓存
```

## 技术栈

- **存储**: `better-sqlite3` + FTS5 全文索引
- **向量检索**: 内置余弦相似度计算（无需 FAISS 依赖）
- **嵌入**: 通过 Node.js 调用已配置的 LLM 模型做嵌入推理
- **文件解析**: docx/pdf/txt/md 技能（与已有技能联动）

## 快速开始

用户说 "创建知识库" → 创建并提示名称
用户说 "添加到知识库" → 自动索引文件/网页
用户说 "搜索知识库" → 语义搜索 + 全文搜索返回结果
用户说 "记笔记" → 创建/编辑笔记

## 安全规则

1. **所有数据本地存储**，绝不上传到任何第三方服务
2. **不记录文件内容到对话中**（只返回摘要和定位），除非用户明确要求查看
3. **敏感文件路径不泄露**

## 模块

- `index.md` — 文档索引（文件/网页/代码）
- `search.md` — 搜索（语义 + 关键词）
- `notes.md` — 笔记管理
- `knowledge-graph.md` — 知识图谱

## 🔌 MCP 服务

gbrain 现在提供两个 MCP Server，其他应用可通过 stdio JSON-RPC 调用：

### gbrain 知识库 MCP

```json
{
  "mcp": {
    "servers": {
      "gbrain": {
        "command": "node",
        "args": ["skills/gbrain/mcp-server.js"],
        "env": { "GBRAIN_ROOT": "D:\\bobo\\openclaw-foreign\\state\\gbrain" }
      }
    }
  }
}
```

提供工具：
- `gbrain_search(kbName, query, limit)` — 搜索
- `gbrain_add(kbName, title, content, tags)` — 添加文档
- `gbrain_stats(kbName)` — 统计
- `gbrain_list()` — 列出所有知识库
- `gbrain_delete(kbName, docId)` — 删除文档

### 代码执行沙箱 MCP

```json
{
  "mcp": {
    "servers": {
      "sandbox": {
        "command": "node",
        "args": ["skills/gbrain/lib/sandbox.js", "-c"]
      }
    }
  }
}
```

### 全栈 REST API

Express 服务器（端口 3001）：

```bash
cd skills/gbrain/fullstack
node server/index.js
```

| 端点 | 说明 |
|:-----|:------|
| GET /api/status | 系统状态 + 知识库列表 |
| GET /api/kb/:name/search?q= | 搜索 |
| POST /api/kb/:name/add | 添加文档 |
| GET /api/kb/:name/stats | 统计 |
| GET / | Web 管理后台 |

## 自主学习

gbrain 具备**自主进化能力**。当你提问时遇到知识库未收录的概念，它会：

1. 🔍 感知知识缺口（查询命中率 < 0.3 触发）
2. 🌐 自动搜索 web + GitHub Trending
3. 📥 提取精华存入 `auto-learn` 知识库
4. 📈 下次类似问题：命中率提升

```bash
node skills/gbrain/lib/learn.js --query "概念名"    # 按需学习
node skills/gbrain/lib/learn.js --auto              # 全自动扫描
```

## 🤖 Ollama 集成 (可选)

gbrain 支持通过本地 Ollama 实例获取嵌入和推理，完全离线运行。

```bash
# 检查 Ollama 状态
node skills/gbrain/lib/ollama.js check

# 连接已有的 Ollama，自动使用 nomic-embed-text 做嵌入
node skills/gbrain/lib/ollama.js embed "文本内容"

# 对话
node skills/gbrain/lib/ollama.js chat qwen2.5:7b "你好"

# 推荐适合当前任务的模型
node skills/gbrain/lib/ollama.js recommend code
```

环境变量: `OLLAMA_HOST=http://localhost:11434`（默认）

推荐嵌入模型: `ollama pull nomic-embed-text`（274MB，轻量）

## 💻 IDE 集成

gbrain 可直接连接到 VS Code / Cursor / Windsurf 编辑器：

```bash
# 检测当前打开的编辑器
node skills/gbrain/lib/ide.js detect

# 扫描编辑器中的项目结构
node skills/gbrain/lib/ide.js scan D:\projects\my-app 3

# 索引编辑器项目代码到 gbrain 知识库
node skills/gbrain/lib/ide.js index code D:\projects\my-app

# 在编辑器中搜索知识库
node skills/gbrain/lib/ide.js search code "React hook"
```

### 功能
- 自动检测编辑器（VS Code / Cursor / Windsurf）
- 索引项目代码（按函数/类分块，忽略 node_modules、dist 等）
- 打开文件 → 语义搜索 gbrain 知识库
- 创建/写入项目文件
- guard 锁保护

### 触发链

```
用户提问 → 知识库搜索 → 命中率低(<0.3)
                        ↓
              感知知识缺口 → GitHub Trending API
                        ↓
              提取核心要点 → 存入 auto-learn
                        ↓
              下次相同问题 → 命中率提升
```

## 🧩 IDE 集成

gbrain 可直接从编辑器提取代码到知识库：

```bash
# 检测当前编辑器
node lib/ide.js detect

# 扫描项目结构
node lib/ide.js scan D:\path\to\project

# 索引整个项目到知识库
node lib/ide.js index code D:\path\to\project

# 在 editor 内部搜索知识库
node lib/ide.js search code "查询词"
```

支持的编辑器：VS Code、Cursor、Windsurf。
索引时会自动跳过 node_modules、.git、dist 等目录。
大文件按函数/类分块索引，保留行号引用。

## 🤖 Ollama 本地模型

gbrain 支持通过本地 Ollama 使用开源 LLM，无需网络和 API Key：

```bash
# 检查 Ollama 状态
node lib/ollama.js check

# 列出已下载模型
node lib/ollama.js list

# 对话
node lib/ollama.js chat qwen2.5:7b "你的问题"

# 获取嵌入（文档向量化）
node lib/ollama.js embed "要向量化的文本"

# 查看推荐模型
node lib/ollama.js recommend
```

环境变量：`OLLAMA_HOST=http://localhost:11434`（可自定义）
