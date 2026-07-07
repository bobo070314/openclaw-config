# PPT Animation Smart

## 描述
专业的PPT动画专家，帮助用户创建流畅、专业的动画效果，提升演示体验。

## 功能列表

### 1. suggest-animation
建议动画效果
- **输入**：页面内容、演示场景
- **输出**：推荐动画方案（进入、强调、退出动画）

### 2. create-transition
创建切换效果
- **输入**：页面类型、过渡风格
- **输出**：切换效果建议

### 3. optimize-timing
优化动画时间
- **输入**：动画序列
- **输出**：优化后的时间安排

### 4. consistency-check
动画一致性检查
- **输入**：多页PPT动画
- **输出**：一致性检查结果

### 5. remove-redundancy
移除冗余动画
- **输入**：现有动画序列
- **输出**：简化后的动画方案

## 使用示例

### 示例1：建议动画
```json
{
  "function": "suggest-animation",
  "params": {
    "content": "标题+要点列表+图片",
    "scenario": "正式商务演示"
  }
}
```

### 示例2：创建切换
```json
{
  "function": "create-transition",
  "params": {
    "pageType": "数据页",
    "style": "简洁专业"
  }
}
```

### 示例3：优化时间
```json
{
  "function": "optimize-timing",
  "params": {
    "animations": [
      {"type": "fade", "duration": 0.5},
      {"type": "slide", "duration": 1.0},
      {"type": "zoom", "duration": 0.8}
    ]
  }
}
```

## 输出格式

### 动画方案
```json
{
  "entrance": {
    "title": "fade",
    "duration": 0.5,
    "delay": 0
  },
  "emphasis": [
    {
      "type": "pulse",
      "duration": 0.5,
      "delay": 0.5
    }
  ],
  "exit": {
    "type": "fade",
    "duration": 0.3,
    "delay": 0
  }
}
```

### 切换效果
```json
{
  "effect": "fade",
  "duration": 0.5,
  "direction": "from-right",
  "type": "slide"
}
```

## 分配部门

### 主要分配
- **设计部**：设计作品PPT
- **市场部**：营销材料PPT
- **创新部**：创新项目PPT

### 协作分配
- **销售部**：销售演示PPT
- **文化部**：文化宣传PPT
- **公关部**：公关材料PPT

## 限制条件

1. **专业度优先**：动画效果必须专业，避免过度花哨
2. **流畅性优先**：动画时间必须流畅，避免卡顿
3. **一致性优先**：多页PPT动画风格必须一致
4. **场景适配**：根据演示场景选择合适的动画效果

## 最佳实践

1. **进入动画**：标题用fade，要点用slide，图片用zoom
2. **强调动画**：重要数据用pulse，关键要点用bounce
3. **退出动画**：用fade或slide，避免用复杂的退出效果
4. **切换效果**：用fade或slide，避免用3D切换

## 常见问题

**Q: 如何选择动画效果？**
A: 正式商务演示用fade/slide，创意演示用zoom/rotate，避免用复杂的3D效果。

**Q: 如何优化动画时间？**
A: 进入动画0.5秒，强调动画0.5秒，退出动画0.3秒，切换动画0.5秒。

**Q: 如何确保动画一致性？**
A: 统一使用相同的进入/退出动画，强调动画类型一致，切换效果一致。

---

**Skill名称**：ppt-animation-smart
**版本**：1.0.0
**创建时间**：2026-06-30
**创建人**：龙家科技集团-设计部
