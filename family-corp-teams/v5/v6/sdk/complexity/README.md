# ComplexityAnalyzer SDK v1.0.0

圈复杂度/认知复杂度度量，支持单个文件和目录批量分析

## 快速开始

```python
from igp_sdk.complexity import ComplexityAnalyzer
ca = ComplexityAnalyzer()
result = ca.analyze_file("module.py")
print(f"Score: {result.get('score')}")
```

## 类列表

- `ComplexityAnalyzer`

## 版本
`v1.0.0`
