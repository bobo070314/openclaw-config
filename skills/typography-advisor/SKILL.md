# Typography Advisor

## 描述
专业的字体排版顾问，帮助用户选择和使用最佳字体组合，确保排版质量。

## 功能列表

### 1. suggest-fonts
建议字体——根据场景推荐字体组合
- **输入**：场景、风格
- **输出**：字体推荐

### 2. set-hierarchy
设置层级——设置字体层级系统
- **输入**：字体、层级要求
- **输出**：字体层级

### 3. calculate-readability
计算可读性——分析文本的可读性
- **输入**：字体、字号、行距
- **输出**：可读性分析

### 4. optimize-line-height
优化行距——优化行距和间距
- **输入**：字号、字体
- **输出**：行距建议

### 5. export-typography
导出排版——导出排版设置
- **输入**：排版设置
- **输出**：CSS样式

## 使用示例

### 示例1：建议字体
```json
{
  "function": "suggest-fonts",
  "params": {
    "scenario": "商务网站",
    "style": "现代简洁"
  }
}
```

### 示例2：设置层级
```json
{
  "function": "set-hierarchy",
  "params": {
    "fonts": {"heading": "Inter", "body": "Noto Sans SC"},
    "levels": ["h1", "h2", "h3", "body", "small"]
  }
}
```

### 示例3：优化行距
```json
{
  "function": "optimize-line-height",
  "params": {
    "fontSize": 16,
    "fontFamily": "Noto Sans SC"
  }
}
```

## 输出格式

### 字体推荐
```json
{
  "scenario": "商务网站",
  "style": "现代简洁",
  "recommendation": {
    "heading": {
      "fontFamily": "Inter",
      "fallback": "sans-serif",
      "weights": [400, 600, 700]
    },
    "body": {
      "fontFamily": "Noto Sans SC",
      "fallback": "sans-serif",
      "weights": [300, 400, 500]
    }
  }
}
```

### 层级系统
```json
{
  "h1": {"size": 32, "lineHeight": 1.3, "weight": 700},
  "h2": {"size": 24, "lineHeight": 1.35, "weight": 600},
  "h3": {"size": 20, "lineHeight": 1.4, "weight": 600},
  "body": {"size": 16, "lineHeight": 1.6, "weight": 400},
  "small": {"size": 14, "lineHeight": 1.5, "weight": 400}
}
```

## 分配部门

### 主要分配
- **设计部**：界面排版
- **市场部**：营销材料排版
- **内容创作部**：内容排版

### 协作分配
- **研发部**：前端实现
- **文化部**：品牌形象
- **培训部**：培训材料排版

## 限制条件

1. **字体兼容性**：推荐字体必须兼容主流浏览器
2. **可读性优先**：可读性比美观更重要
3. **风格统一**：全程使用一致的字体层级
4. **中西方兼容**：中文和英文使用不同字体

## 最佳实践

1. **字体组合**：标题用无衬线体，正文用易读字体
2. **层级系统**：明确h1-h6、body、small等层级
3. **行距优化**：正文行距1.5-1.8倍字号
4. **中英文适配**：中文用中文字体，英文用英文字体

## 常见问题

**Q: 如何选择字体组合？**
A: 标题用粗体现代字体，正文用易读经典字体，确保中英文兼容。

**Q: 如何设置字体层级？**
A: h1=32px, h2=24px, h3=20px, body=16px, small=14px。

**Q: 如何优化可读性？**
A: 选择合适的行距（1.5-1.8倍字号），确保对比度足够。

---

**Skill名称**：typography-advisor
**版本**：1.0.0
**创建时间**：2026-06-30
**创建人**：龙家科技集团-设计部
