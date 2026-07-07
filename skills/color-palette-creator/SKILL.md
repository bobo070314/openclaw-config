# Color Palette Creator

## 描述
专业的配色方案创建专家，帮助用户创建和谐美观的配色方案。

## 功能列表

### 1. generate-palette
生成配色——从基础色生成完整配色方案
- **输入**：基础色、风格
- **输出**：配色方案

### 2. generate-gradient
生成渐变——生成渐变方案
- **输入**：起始色、结束色
- **输出**：渐变方案

### 3. check-contrast
检查对比度——检查颜色对比度
- **输入**：前景色、背景色
- **输出**：对比度检查结果

### 4. suggest-accessibility
建议可访问性——确保配色符合无障碍标准
- **输入**：配色方案
- **输出**：无障碍检查结果

### 5. export-palette
导出配色——导出配色方案到多种格式
- **输入**：配色方案、目标格式
- **输出**：导出的配色文件

## 使用示例

### 示例1：生成配色
```json
{
  "function": "generate-palette",
  "params": {
    "baseColor": "#0056b3",
    "style": "现代商务"
  }
}
```

### 示例2：生成渐变
```json
{
  "function": "generate-gradient",
  "params": {
    "startColor": "#0056b3",
    "endColor": "#00d4ff",
    "direction": "to-right"
  }
}
```

### 示例3：检查对比度
```json
{
  "function": "check-contrast",
  "params": {
    "foreground": "#333333",
    "background": "#ffffff"
  }
}
```

## 输出格式

### 配色方案
```json
{
  "baseColor": "#0056b3",
  "style": "现代商务",
  "palette": {
    "primary": {
      "50": "#e3f2fd",
      "100": "#bbdefb",
      "200": "#90caf9",
      "300": "#64b5f6",
      "400": "#42a5f5",
      "500": "#2196f3",
      "600": "#1e88e5",
      "700": "#1976d2",
      "800": "#1565c0",
      "900": "#0d47a1"
    },
    "secondary": ["#f0f4f8", "#e2e8f0"],
    "accent": "#ff6b6b",
    "neutral": ["#333333", "#666666", "#999999"],
    "background": ["#ffffff", "#f8f9fa", "#f0f4f8"]
  }
}
```

### 对比度检查
```json
{
  "foreground": "#333333",
  "background": "#ffffff",
  "contrastRatio": 12.0,
  "wcagAA": true,
  "wcagAAA": true
}
```

## 分配部门

### 主要分配
- **设计部**：设计配色
- **市场部**：品牌配色
- **文化部**：品牌形象

### 协作分配
- **研发部**：前端开发
- **公关部**：品牌宣传
- **运营部**：运营设计

## 限制条件

1. **和谐性**：配色必须和谐美观
2. **无障碍**：必须符合WCAG无障碍标准
3. **一致性**：必须与品牌色一致
4. **场景适配**：必须适配使用场景

## 最佳实践

1. **品牌优先**：优先使用品牌色
2. **无障碍检查**：对比度必须满足WCAG AA标准
3. **场景适配**：根据不同场景选择配色
4. **导出工具**：使用export-palette导出工具

## 常见问题

**Q: 如何选择配色方案？**
A: 从品牌色开始，使用生成配色功能，调整到满意为止。

**Q: 如何检查对比度？**
A: 使用check-contrast函数，确保对比度≥4.5:1（WCAG AA）。

**Q: 如何导出配色？**
A: 使用export-palette函数，支持JSON、CSS、SCSS等格式。

---

**Skill名称**：color-palette-creator
**版本**：1.0.0
**创建时间**：2026-06-30
**创建人**：龙家科技集团-设计部
