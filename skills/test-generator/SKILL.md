# Test Generator

## 描述
专业的测试用例生成专家，帮助用户自动生成高质量的单元测试和集成测试。

## 功能列表

### 1. generate-unit-tests
生成单元测试——为函数/方法生成单元测试
- **输入**：源代码
- **输出**：单元测试代码

### 2. generate-integration-tests
生成集成测试——为模块生成集成测试
- **输入**：源代码、模块依赖
- **输出**：集成测试代码

### 3. generate-edge-cases
生成边界用例——生成边界值测试用例
- **输入**：函数签名、参数范围
- **输出**：边界测试用例

### 4. generate-mock
生成Mock——为依赖项生成Mock对象
- **输入**：依赖接口
- **输出**：Mock代码

### 5. calculate-test-coverage
计算覆盖率——分析测试覆盖率
- **输入**：源代码、测试代码
- **输出**：覆盖率报告

## 使用示例

### 示例1：生成单元测试
```json
{
  "function": "generate-unit-tests",
  "params": {
    "source": "function add(a, b) { return a + b; }",
    "framework": "jest"
  }
}
```

### 示例2：生成边界用例
```json
{
  "function": "generate-edge-cases",
  "params": {
    "functionSignature": "function divide(a: number, b: number): number",
    "parameterRanges": {
      "a": "(-10^6, 10^6)",
      "b": "(-10^6, 10^6), b !== 0"
    }
  }
}
```

### 示例3：计算覆盖率
```json
{
  "function": "calculate-test-coverage",
  "params": {
    "source": "完整源代码",
    "tests": "完整测试代码"
  }
}
```

## 输出格式

### 单元测试
```json
{
  "framework": "jest",
  "testCount": 15,
  "tests": [
    {
      "name": "should add two positive numbers",
      "input": {"a": 1, "b": 2},
      "expected": 3
    }
  ],
  "edgeCases": 5,
  "coverage": {
    "lines": 95,
    "branches": 88,
    "functions": 100
  }
}
```

### 覆盖率报告
```json
{
  "totalFunctions": 20,
  "testedFunctions": 18,
  "lineCoverage": 92,
  "branchCoverage": 85,
  "uncoveredLines": [25, 30, 45],
  "recommendations": [
    "为helper.js的第25行添加测试"
  ]
}
```

## 分配部门

### 主要分配
- **研发部**：测试开发
- **测试部**：测试执行
- **质管部**：质量验收

### 协作分配
- **IT部**：系统测试
- **数据部**：数据处理测试
- **运营部**：验收测试

## 限制条件

1. **覆盖率目标**：单元测试覆盖率≥90%
2. **边界覆盖**：必须覆盖所有边界用例
3. **框架支持**：支持Jest、Mocha、JUnit、pytest
4. **自动化执行**：测试必须可自动化执行

## 最佳实践

1. **先写测试后写代码**：TDD方式
2. **覆盖所有分支**：确保分支覆盖率达到要求
3. **边界测试优先**：优先测试边界条件
4. **Mock外部依赖**：使用Mock隔离依赖

## 常见问题

**Q: 测试覆盖率目标是多少？**
A: 单元测试≥90%，集成测试≥80%，E2E测试≥70%。

**Q: 如何编写高质量测试？**
A: 测试单一功能，覆盖边界用例，Mock外部依赖，测试可重复执行。

**Q: 如何处理难以测试的代码？**
A: 重构代码使其更可测试，减少依赖，使用依赖注入。

---

**Skill名称**：test-generator
**版本**：1.0.0
**创建时间**：2026-06-30
**创建人**：龙家科技集团-研发部
