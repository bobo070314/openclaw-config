# Layout Auditor

## 描述
专业的页面布局审计专家，帮助检查和优化UI/PPT页面的布局结构和视觉层次。

## 功能列表

### 1. audit-layout
审计布局结构
- **输入**：页面结构、设计规范
- **输出**：布局审计报告

### 2. suggest-alignment
建议对齐方案
- **输入**：页面元素
- **输出**：对齐建议

### 3. optimize-hierarchy
优化视觉层次
- **输入**：内容层次结构
- **输出**：视觉层次优化建议

### 4. check-proportions
检查比例协调
- **输入**：页面尺寸、元素尺寸
- **输出**：比例检查结果

### 5. improve-grid
改进网格系统
- **输入**：现有布局
- **输出**：网格系统改进建议

## 使用示例

### 示例1：审计布局
```json
{
  "function": "audit-layout",
  "params": {
    "structure": {
      "width": 1920,
      "height": 1080,
      "elements": [
        {"type": "header", "y": 0, "height": 80},
        {"type": "content", "y": 80, "height": 800},
        {"type": "footer", "y": 880, "height": 200}
      ]
    },
    "standards": "UI标准"
  }
}
```

### 示例2：建议对齐
```json
{
  "function": "suggest-alignment",
  "params": {
    "elements": [
      {"id": "logo", "x": 50, "y": 20, "width": 100, "height": 40},
      {"id": "title", "x": 200, "y": 20, "width": 300, "height": 40}
    ]
  }
}
```

## 输出格式

### 审计报告
```json
{
  "passed": true,
  "issues": [
    {
      "type": "alignment",
      "severity": "warning",
      "element": "标题",
      "suggestion": "将标题左对齐到logo位置"
    }
  ],
  "score": 85
}
```

## 分配部门

### 主要分配
- **设计部**：UI/UX设计
- **运营部**：页面排版
- **市场部**：营销素材

### 协作分配
- **研发部**：前端布局
- **创新部**：创新项目

---

**Skill名称**：layout-auditor
**版本**：1.0.0
**创建时间**：2026-06-30
