# Performance Optimizer

## 描述
专业的代码性能优化专家，帮助用户发现和修复性能瓶颈。

## 功能列表

### 1. analyze-performance
分析性能——分析代码的性能瓶颈
- **输入**：源代码
- **输出**：性能分析报告

### 2. optimize-loop
优化循环——优化循环性能
- **输入**：循环代码
- **输出**：优化后的代码

### 3. optimize-query
优化查询——优化数据库查询性能
- **输入**：查询语句
- **输出**：优化后的查询

### 4. reduce-memory
减少内存——减少内存使用
- **输入**：代码
- **输出**：内存优化建议

### 5. suggest-caching
建议缓存——推荐缓存策略
- **输入**：代码、数据特征
- **输出**：缓存策略建议

## 使用示例

### 示例1：分析性能
```json
{
  "function": "analyze-performance",
  "params": {
    "source": "for(let i=0;i<items.length;i++){...}",
    "language": "javascript"
  }
}
```

### 示例2：优化循环
```json
{
  "function": "optimize-loop",
  "params": {
    "loopCode": "for(let i=0;i<data.length;i++){ process(data[i]); }",
    "optimization": "并行处理"
  }
}
```

### 示例3：优化查询
```json
{
  "function": "optimize-query",
  "params": {
    "query": "SELECT * FROM orders WHERE status = 'pending'",
    "optimization": "添加索引"
  }
}
```

## 输出格式

### 性能分析
```json
{
  "bottlenecks": [
    {
      "type": "loop",
      "line": 10,
      "complexity": "O(n²)",
      "impact": "高"
    }
  ],
  "recommendations": [
    "将嵌套循环改为哈希表查询",
    "添加缓存减少重复计算"
  ],
  "estimatedGain": "50-80%"
}
```

### 优化后的代码
```json
{
  "original": "for(let i=0;i<items.length;i++){...}",
  "optimized": "const map = new Map(items.map(...))",
  "improvement": "O(n²) → O(n)"
}
```

## 分配部门

### 主要分配
- **研发部**：代码优化
- **IT部**：系统优化
- **数据部**：数据处理优化

### 协作分配
- **运营部**：运营效率
- **质管部**：质量评估
- **财务部**：成本评估

## 限制条件

1. **正确性优先**：优化不能改变功能
2. **可读性优先**：优化不能影响可读性
3. **渐进优化**：优先优化瓶颈
4. **经验证**：优化必须经过验证

## 最佳实践

1. **先分析后优化**：先找到瓶颈再优化
2. **优先瓶颈**：优先优化最大的瓶颈
3. **保持可读**：优化不影响代码可读性
4. **验证效果**：优化后验证效果

## 常见问题

**Q: 如何进行性能优化？**
A: 分析→定位瓶颈→优化→验证效果。

**Q: 优化的优先级是什么？**
A: 用户体验优先，IO开销优先，循环计算优先。

**Q: 如何避免过度优化？**
A: 只优化导致性能问题的代码，不优化无关代码。

---

**Skill名称**：performance-optimizer
**版本**：1.0.0
**创建时间**：2026-06-30
**创建人**：龙家科技集团-研发部
