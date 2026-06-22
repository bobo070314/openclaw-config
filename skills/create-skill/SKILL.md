---
name: create-skill
description: 技能工厂，Context Snapshot自举，一键生成SKILL.md+_meta.json+run.sh+run.bat
version: 0.2.0
status: implemented
category: meta
---

# create-skill — 技能工厂

## 定位
从需求描述一键生成完整的 OpenClaw 技能四件套：SKILL.md + _meta.json + run.sh + run.bat。支持 Context Snapshot 自举——自动扫描当前项目环境提取技术栈。

## 触发条件
- "创建一个新技能"
- "add a new skill"
- "新建 xxx 技能"

## 工作流

1. **需求分析** — 从用户描述中提取技能名称、类别、核心功能
2. **Context Snapshot** — 扫描 workspace 提取：
   - 项目类型（Node/Python/Go）
   - 端口占用
   - 依赖版本
   - 环境变量
3. **生成 SKILL.md** — YAML frontmatter + 完整 Markdown body
4. **生成 _meta.json** — 包含 name/version/status/category
5. **生成 run.sh/bat** — 跨平台启动脚本
6. **注册到 openclaw.json** — 自动更新 skills.entries

## 输出产物
```
skills/{name}/
├── SKILL.md      # 核心文档（frontmatter + body）
├── _meta.json    # 元数据
├── run.sh        # Linux/Mac 启动
└── run.bat       # Windows 启动
```

## 关键约束
- 幂等：目录已存在则跳过，不覆盖
- 前端技术栈默认 Tailwind
- Windows 路径用反斜杠

## 依赖
- Python 3.8+
- 纯标准库（无额外依赖）
