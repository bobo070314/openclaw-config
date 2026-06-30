# Bug Tracer

## 描述
专业的Bug追踪和调试专家，帮助用户快速定位和修复代码中的Bug。

## 功能列表

### 1. analyze-error
分析错误——分析错误信息和堆栈跟踪
- **输入**：错误信息、堆栈跟踪
- **输出**：错误分析结果

### 2. trace-bug
追踪Bug——追踪Bug的根因
- **输入**：源代码、错误描述
- **输出**：Bug追踪报告

### 3. suggest-fix
建议修复——提供修复建议和代码
- **输入**：Bug描述、源代码
- **输出**：修复建议和代码

### 4. reproduce-bug
复现Bug——提供Bug复现步骤
- **输入**：Bug描述
- **输出**：复现步骤

### 5. predict-bugs
预测Bug——预测代码中可能出现的Bug
- **输入**：源代码
- **输出**：潜在Bug列表

## 使用示例

### 示例1：分析错误
```json
{
  "function": "analyze-error",
  "params": {
    "error": "TypeError: Cannot read property 'map' of undefined",
    "stack": "at Object.render (App.js:10:5)",
    "code": "const items = data.items.map(...)"
  }
}
```

### 示例2：追踪Bug
```json
{
  "function": "trace-bug",
  "params": {
    "source": "完整的源代码",
    "bugDescription": "用户登录后页面一直loading"
  }
}
```

### 示例3：建议修复
```json
{
  "function": "suggest-fix",
  "params": {
    "source": "function getData() { return api.fetch('/data'); }",
    "bug": "数据未正确加载"
  }
}
```

## 输出格式

### 错误分析
```json
{
  "errorType": "TypeError",
  "rootCause": "data变量未初始化",
  "affectedLine": 10,
  "reproSteps": [
    "1. 打开页面",
    "2. 等待API响应",
    "3. data.items.map执行失败"
  ],
  "fixSuggestion": "添加初始化代码：data = data || []"
}
```

### Bug追踪报告
```json
{
  "bugId": "BUG-001",
  "severity": "high",
  "affectedComponent": "UserService",
  "rootCause": "API返回数据格式变更",
  "fixCode": "更新数据解析逻辑",
  "estimatedFixTime": "2小时"
}
```

## 分配部门

### 主要分配
- **研发部**：Bug修复
- **IT部**：系统维护
- **测试部**：Bug验证

### 协作分配
- **质管部**：质量跟踪
- **客服部**：Bug报告收集
- **运营部**：影响评估

## 限制条件

1. **准确性优先**：定位必须准确
2. **复现优先**：能复现的Bug才能修复
3. **根因分析**：必须分析根因
4. **修复验证**：修复后必须验证

## 最佳实践

1. **复现优先**：先复现再定位
2. **根因分析**：找到根因而不是治标
3. **最小修复**：最小化修改范围
4. **及时修复**：高优先级Bug优先处理

## 常见问题

**Q: 如何快速定位Bug？**
A: 复现Bug→分析错误信息→追踪代码路径→定位根因。

**Q: 如何处理不能复现的Bug？**
A: 记录所有线索，增加日志，分析潜在原因。

**Q: 如何验证Bug已修复？**
A: 使用原始步骤复现，确认问题不再出现。

---

**Skill名称**：bug-tracer
**版本**：1.0.0
**创建时间**：2026-06-30
**创建人**：龙家科技集团-研发部
