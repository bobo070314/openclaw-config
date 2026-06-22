# gbrain Phase 2 — 本地模型 & IDE 集成快速入门

本文提供手动安装 Ollama 和配置 IDE 集成的步骤。

---

## 1️⃣ 安装 Ollama

### 方式一：一键安装 (Windows)

```powershell
# 从官网下载安装
winget install Ollama.Ollama

# 或手动下载
# https://ollama.com/download/OllamaSetup.exe
```

### 方式二：Docker (可选)

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### 安装后

Ollama 会自动注册为 Windows 服务。推荐下载的模型：

```bash
# 嵌入模型（必装，gbrain 向量搜索用）
ollama pull nomic-embed-text

# 对话模型（推荐）
ollama pull qwen2.5:7b

# 代码模型（推荐）
ollama pull deepseek-coder:6.7b

# 轻量推理
ollama pull deepseek-r1:7b
```

### 验证安装

```bash
ollama list
# 应显示已下载的模型列表

curl http://localhost:11434/api/tags
# 应返回 JSON 格式的模型列表
```

---

## 2️⃣ 配置 gbrain 使用 Ollama

### 方式一：手动调用嵌入

```bash
node skills/gbrain/lib/ollama.js check
node skills/gbrain/lib/ollama.js embed "你好世界"
node skills/gbrain/lib/ollama.js chat qwen2.5:7b "什么是知识库？"
```

### 方式二：在 gbrain 存储层集成

编辑 `skills/gbrain/lib/storage.js`，在 `addDocument` 方法中增加：

```javascript
if (global.useOllamaEmbed) {
  const ollama = require('./ollama');
  const embResult = await ollama.embed('nomic-embed-text', content);
  this._costore.vectors[docId] = embResult.embedding;
}
```

---

## 3️⃣ VS Code / Cursor 集成

### 查看已安装的编辑器

```bash
node skills/gbrain/lib/ide.js detect
```

### 索引项目代码到 gbrain

```bash
node skills/gbrain/lib/ide.js index code "D:\你的项目路径"
```

### 在命令行搜索

```bash
node skills/gbrain/lib/ide.js search code "数据库查询"
```

### 安装 VS Code 扩展

等待后续开发：扩展将实现右键菜单「添加到 gbrain」和命令面板搜索。

---

## 4️⃣ 状态检查

```bash
# 检查系统环境
node skills/gbrain/lib/ollama.js check
node skills/gbrain/lib/ide.js detect
node -e "const s=require('./skills/gbrain/lib/storage'); new s.AutoLearn().listKBs().then(r=>console.log('知识库:', r))"
```
