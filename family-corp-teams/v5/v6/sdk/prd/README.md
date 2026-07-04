# PRDQueue SDK v1.0.0

跨部门PRD需求管理：提交/评审/自动搜索关键词

## 快速开始

```python
from igp_sdk.prd import PRDQueue
q = PRDQueue(".")
prd = q.submit(department="market", product="BugDoctor",
               title="需要TypeScript支持", priority="high")
print(f"PRD: {prd['id']}")
```

## 类列表

- `PRDQueue`

## 版本
`v1.0.0`
