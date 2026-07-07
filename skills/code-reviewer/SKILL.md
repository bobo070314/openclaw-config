# Code Reviewer

## 描述
专业的代码审查专家，帮助用户进行代码质量审查、规范检查和优化建议。

## 功能列表

### 1. review-code
审查代码——对代码进行全面审查
- **输入**：源代码
- **输出**：审查报告

### 2. check-style
检查风格——检查代码风格是否符合规范
- **输入**：源代码、风格规范
- **输出**：风格检查结果

### 3. check-security
检查安全——检查代码中的安全漏洞
- **输入**：源代码
- **输出**：安全检查结果

### 4. suggest-improvements
建议改进——提供代码改进建议
- **输入**：源代码
- **输出**：改进建议

### 5. validate-api
验证API——检查API使用是否正确
- **输入**：API调用代码
- **输出**：API验证结果

## 使用示例

### 示例1：审查代码
```json
{
  "function": "review-code",
  "params": {
    "source": "function add(a, b) { return a + b; }",
    "language": "javascript"
  }
}
```

### 示例2：检查风格
```json
{
  "function": "check-style",
  "params": {
    "source": "let x=1;let y=2;",
    "styleGuide": "airbnb"
  }
}
```

### 示例3：检查安全
```json
{
  "function": "check-security",
  "params": {
    "source": "eval(userInput)"
  }
}
```

## 输出格式

### 审查报告
```json
{
  "file": "example.js",
  "language": "javascript",
  "issues": [
    {
      "line": 10,
      "type": "error",
      "message": "Potential XSS vulnerability",
      "severity": "high"
    }
  ],
  "styleIssues": [
    {
      "line": 5,
      "type": "warning",
      "message": "Missing semicolon",
      "severity": "low"
    }
  ],
  "overallScore": 85,
  "summary": "Good quality, 1 high severity issue"
}
```

## 分配部门

### 主要分配
- **研发部**：代码开发
- **IT部**：系统开发
- **数据部**：数据处理

### 协作分配
- **质管部**：质量检查
- **安全部**：安全检查
- **测试部**：代码测试

## 限制条件

1. **语言支持**：支持JavaScript、Python、TypeScript、Java、Go、Rust
2. **大小限制**：单次审查不超过1000行
3. **安全优先**：安全漏洞必须优先处理
4. **风格一致性**：必须检查风格一致性

## 最佳实践

1. **每次提交审查**：每次代码提交都经过审查
2. **安全优先**：优先处理安全漏洞
3. **风格统一**：确保代码风格统一
4. **及时修复**：发现的问题及时修复

## 常见问题

**Q: 代码审查的核心关注点有哪些？**
A: 安全性、性能、可读性、可维护性、风格一致性。

**Q: 如何处理审查中的争议？**
A: 以团队规范为准，有争议的提交团队讨论。

**Q: 审查的频率应该是多少？**
A: 每次提交代码时都进行审查，至少每天一次。

---

**Skill名称**：code-reviewer
**版本**：1.0.0
**创建时间**：2026-06-30
**创建人**：龙家科技集团-研发部
