# Security Auditor

## 描述
专业的代码安全审计专家，帮助用户发现和修复代码中的安全漏洞。

## 功能列表

### 1. audit-security
审计安全——全面审计代码安全
- **输入**：源代码
- **输出**：安全审计报告

### 2. detect-xss
检测XSS——检测跨站脚本攻击漏洞
- **输入**：代码
- **输出**：XSS检测结果

### 3. detect-sqli
检测SQL注入——检测SQL注入漏洞
- **输入**：代码
- **输出**：SQL注入检测结果

### 4. detect-csrf
检测CSRF——检测跨站请求伪造漏洞
- **输入**：代码
- **输出**：CSRF检测结果

### 5. suggest-fix
建议修复——提供安全修复建议
- **输入**：安全漏洞描述
- **输出**：修复方案

## 使用示例

### 示例1：审计安全
```json
{
  "function": "audit-security",
  "params": {
    "source": "完整的源代码",
    "language": "javascript"
  }
}
```

### 示例2：检测XSS
```json
{
  "function": "detect-xss",
  "params": {
    "code": "document.write(userInput)",
    "context": "浏览器端"
  }
}
```

### 示例3：检测SQL注入
```json
{
  "function": "detect-sqli",
  "params": {
    "code": "SELECT * FROM users WHERE id = '" + userId + "'",
    "database": "MySQL"
  }
}
```

## 输出格式

### 安全审计报告
```json
{
  "totalIssues": 5,
  "critical": 1,
  "high": 2,
  "medium": 1,
  "low": 1,
  "vulnerabilities": [
    {
      "type": "XSS",
      "severity": "critical",
      "line": 25,
      "description": "未对用户输入进行转义",
      "fix": "使用textContent替代innerHTML"
    }
  ]
}
```

### 修复方案
```json
{
  "vulnerability": "SQL注入",
  "severity": "high",
  "rootCause": "字符串拼接SQL",
  "fixCode": "使用参数化查询",
  "priority": "立即修复"
}
```

## 分配部门

### 主要分配
- **安全部**：安全审计
- **IT部**：系统安全
- **研发部**：安全开发

### 协作分配
- **质管部**：安全检查
- **法务部**：合规检查
- **审计部**：合规审计

## 限制条件

1. **全面性**：审计必须覆盖所有安全维度
2. **准确性**：漏洞检测必须准确
3. **及时性**：关键漏洞必须立即报告
4. **合规性**：必须符合安全合规要求

## 最佳实践

1. **每次上线前审计**：每次上线前进行安全审计
2. **关键漏洞优先**：关键漏洞优先修复
3. **代码审查结合**：安全审计结合代码审查
4. **持续监控**：持续监控安全状态

## 常见问题

**Q: 安全审计的核心关注点有哪些？**
A: XSS、SQL注入、CSRF、SSRF、认证授权、数据加密、敏感信息泄露。

**Q: 如何处理发现的安全漏洞？**
A: 评估严重性→确定优先级→修复→验证→记录。

**Q: 审计的频率应该是多少？**
A: 每次上线前全面审计，每周增量审计，每天安全检查。

---

**Skill名称**：security-auditor
**版本**：1.0.0
**创建时间**：2026-06-30
**创建人**：龙家科技集团-IT部
