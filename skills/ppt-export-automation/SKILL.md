# PPT Export Automation

## 描述
专业的PPT导出自动化专家，帮助用户批量导出、转换和分发PPT文件。

## 功能列表

### 1. batch-export
批量导出PPT
- **输入**：PPT文件列表、导出格式
- **输出**：批量导出结果（成功/失败列表）

### 2. format-conversion
格式转换
- **输入**：PPT文件、目标格式
- **输出**：转换后的文件

### 3. optimize-file-size
优化文件大小
- **输入**：PPT文件
- **输出**：优化后的文件（大小对比）

### 4. quality-check
质量检查
- **输入**：导出的PPT文件
- **输出**：质量检查结果（分辨率、字体、图片等）

### 5. auto-distribute
自动分发
- **输入**：PPT文件、分发目标
- **输出**：分发结果

## 使用示例

### 示例1：批量导出
```json
{
  "function": "batch-export",
  "params": {
    "files": [
      {"path": "report1.pptx", "format": "pdf"},
      {"path": "report2.pptx", "format": "pdf"}
    ],
    "options": {
      "compress": true,
      "quality": "high"
    }
  }
}
```

### 示例2：格式转换
```json
{
  "function": "format-conversion",
  "params": {
    "input": "presentation.pptx",
    "outputFormat": "pdf",
    "options": {
      "optimize": true,
      "password": null
    }
  }
}
```

### 示例3：优化文件大小
```json
{
  "function": "optimize-file-size",
  "params": {
    "input": "large.pptx",
    "options": {
      "compressImages": true,
      "removeUnusedFonts": true,
      "reduceQuality": 0.8
    }
  }
}
```

## 输出格式

### 批量导出结果
```json
{
  "total": 2,
  "success": [
    {
      "input": "report1.pptx",
      "output": "report1.pdf",
      "size": "2.5MB",
      "status": "success"
    }
  ],
  "failed": [
    {
      "input": "report2.pptx",
      "error": "Conversion failed",
      "status": "failed"
    }
  ]
}
```

### 质量检查结果
```json
{
  "resolution": "1920x1080",
  "fonts": ["Arial", "Times New Roman"],
  "images": 15,
  "totalSize": "3.2MB",
  "warnings": [
    "Image resolution below 1920x1080",
    "Unused font found"
  ]
}
```

## 分配部门

### 主要分配
- **运营部**：运营报告批量导出
- **人力部**：培训材料批量导出
- **数据部**：数据分析报告批量导出

### 协作分配
- **市场部**：营销材料批量导出
- **销售部**：销售演示批量导出
- **财务部**：财务报告批量导出

## 限制条件

1. **格式支持**：支持PPTX、PDF、PPT、图片（PNG/JPG/WEBP）等格式
2. **批量限制**：单次批量导出不超过100个文件
3. **质量要求**：导出质量不低于原始质量
4. **文件安全**：确保文件导出过程安全，不泄露敏感信息

## 最佳实践

1. **批量导出**：使用batch-export函数，设置compress=true优化文件大小
2. **格式转换**：使用format-conversion函数，根据需求选择目标格式
3. **文件优化**：使用optimize-file-size函数，压缩图片、移除未用字体
4. **质量检查**：使用quality-check函数，确保导出质量符合要求

## 常见问题

**Q: 如何批量导出PPT为PDF？**
A: 使用batch-export函数，设置format="pdf"，compress=true，quality="high"。

**Q: 如何优化PPT文件大小？**
A: 使用optimize-file-size函数，设置compressImages=true，removeUnusedFonts=true，reduceQuality=0.8。

**Q: 如何检查导出文件质量？**
A: 使用quality-check函数，检查分辨率、字体、图片数量、文件大小等。

---

**Skill名称**：ppt-export-automation
**版本**：1.0.0
**创建时间**：2026-06-30
**创建人**：龙家科技集团-运营部
