# ReviewAgents SDK v1.0.0

三Agent评审：架构Agent + 安全Agent + 兼容Agent

## 快速开始

```python
from igp_sdk.review import review_file
result = review_file("module.py")
print(f"Score: {result['total_score']}/30 {'PASS' if result['passed'] else 'FAIL'}")
```

## 类列表

- `review_file`
- `ArchitectureAgent`
- `SecurityAgent`
- `CompatibilityAgent`

## 版本
`v1.0.0`
