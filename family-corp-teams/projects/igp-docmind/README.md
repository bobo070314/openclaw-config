# IGP DocMind — 本地PDF解析引擎

从PaddleOCR吸收的核心理念：

| 吸收来源 | IGP实现 |
|---------|--------|
| PP-StructureV3 PDF→Markdown | PDF文本提取→结构化输出 |
| 表格检测 | 字符坐标推断 |
| JSON输出LLM就绪 | 标准JSON格式 |
| 轻量化设计 | 0依赖纯Python |

状态: 演示模式（主动能 2026-07-01 17:51 启动）

## 使用

```python
from docmind import DocMind
engine = DocMind()
result = engine.process('my_document.pdf')
```
