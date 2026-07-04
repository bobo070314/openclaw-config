# CodeAnalyzer SDK v1.0.0

代码质量分析：死代码检测/重构机会/不良模式/杂交机会

## 快速开始

```python
from igp_sdk.analyzer import CodeAnalyzer
ca = CodeAnalyzer(".")
ca.scan_refactoring()
ca.scan_bad_patterns()
ca.scan_mutation_opportunity()
print(ca.report())
```

## 类列表

- `CodeAnalyzer`

## 版本
`v1.0.0`
