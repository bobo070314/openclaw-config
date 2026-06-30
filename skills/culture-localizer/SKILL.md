# Culture Localizer

## 描述
专业的文化本地化专家，帮助用户将AI输出适配不同的文化背景和区域习惯。

## 功能列表

### 1. detect-culture
检测文化背景——分析文本中的文化偏向
- **输入**：文本
- **输出**：文化背景分析结果

### 2. localize-content
本地化内容——将文本适配目标文化
- **输入**：文本、目标文化
- **输出**：本地化后的文本

### 3. adapt-idioms
适配成语习惯——将不符合目标文化的表达替换为本地表达
- **输入**：文本、目标文化
- **输出**：适配后的文本

### 4. adjust-date-format
调整日期格式——根据区域习惯调整日期格式
- **输入**：日期、目标区域
- **输出**：适配后的日期格式

### 5. validate-localization
验证本地化——检查文本是否符合目标文化习惯
- **输入**：文本、目标文化
- **输出**：验证结果

## 使用示例

### 示例1：检测文化背景
```json
{
  "function": "detect-culture",
  "params": {
    "text": "This is a game-changer in the industry."
  }
}
```

### 示例2：本地化内容
```json
{
  "function": "localize-content",
  "params": {
    "text": "This product is a game-changer.",
    "targetCulture": "zh-CN"
  }
}
```

### 示例3：适配成语习惯
```json
{
  "function": "adapt-idioms",
  "params": {
    "text": "It's raining cats and dogs.",
    "targetCulture": "zh-CN"
  }
}
```

## 输出格式

### 文化背景分析
```json
{
  "detectedCulture": "en-US",
  "culturalElements": [
    {"type": "idiom", "value": "game-changer", "notes": "英语表达"},
    {"type": "reference", "value": "industry standard", "notes": "行业术语"}
  ],
  "targetCultures": ["zh-CN", "zh-TW", "ja-JP"]
}
```

### 本地化后的文本
```json
{
  "original": "This product is a game-changer.",
  "localized": "这款产品将颠覆行业格局。",
  "changes": [
    "将'game-changer'本地化为'颠覆行业格局'",
    "添加了中文惯用的'将'字"
  ]
}
```

## 分配部门

### 主要分配
- **市场部**：国际市场推广
- **公关部**：国际公关
- **销售部**：国际销售

### 协作分配
- **内容创作部**：多语种内容
- **客服部**：多语种客服
- **文化部**：跨文化交流

## 限制条件

1. **保留原意**：必须保留原文的核心意思
2. **文化适配**：必须适配目标文化
3. **符合习惯**：必须符合目标区域的语言习惯
4. **适度本地化**：本地化不能过度，保留必要的外来文化元素

## 最佳实践

1. **先分析文化背景**：使用detect-culture分析原文文化偏向
2. **再适配目标文化**：使用localize-content适配目标文化
3. **再适配成语习惯**：使用adapt-idioms适配目标成语习惯
4. **最后验证**：使用validate-localization验证

## 常见问题

**Q: 如何处理跨文化表达？**
A: 将原文中的成语、典故、俗语替换为目标文化中的对应表达。

**Q: 如何处理日期格式？**
A: 中国使用"YYYY年M月D日"，美国使用"MM/DD/YYYY"，欧洲使用"DD/MM/YYYY"。

**Q: 如何处理数字格式？**
A: 中国和美国使用逗号分隔千位，欧洲使用空格分隔千位。

---

**Skill名称**：culture-localizer
**版本**：1.0.0
**创建时间**：2026-06-30
**创建人**：龙家科技集团-市场部
