# SymbolicEngine SDK v1.0.0

约束求解引擎（吸收Z3思路，纯Python）

## 快速开始

```python
from igp_sdk.symbolic import SymbolicEngine
se = SymbolicEngine()
se.add_constraint("x > 5")
se.add_constraint("x < 10")
result = se.solve()
print(f"Solution: {result}")
```

## 类列表

- `SymbolicEngine`

## 版本
`v1.0.0`
