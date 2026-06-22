---
name: gbrain-notes
description: gbrain 模块：笔记管理（创建/编辑/搜索/组织）
---

# gbrain-notes 模块

笔记系统提供轻量级个人信息管理，类似 Notion 极简版 + 知识库深度融合。

## 笔记 vs 知识库条目

| | 笔记 (notes) | 知识库条目 (kb entries) |
|:--|:------------|:----------------------|
| 目的 | 个人写/记 | 外部资料归档 |
| 来源 | 用户手动写 | 文件导入/网页收藏/代码索引 |
| 编辑 | 可随时编辑 | 只读（需重新索引） |
| 标签 | 用户自定义 | AI 自动标注 |
| 搜索 | 全文 + 语义 | 全文 + 语义 + 图谱 |

## 操作命令

### 创建笔记

```bash
node lib/note.js create --kb <知识库> --title "<标题>" --content "<内容>" --tags tag1,tag2
```

### 搜索笔记

```bash
node lib/note.js search --query "<关键词>"
```

### 列出笔记

```bash
node lib/note.js list --kb <知识库> --limit 20
```

### 编辑笔记

```bash
node lib/note.js edit --id <note_id> --content "<新内容>"
```

## 笔记关联

笔记自动关联到知识库中的相关文档条目。当你在笔记中引用某个概念时，系统可以自动推荐知识库中的相关段落（RAG 增强写作）。
