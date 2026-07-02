# Lifecycle SDK v1.0.0

产品生命周期管理：Research→Alpha→Beta→GA→Deprecated→EOL

## 快速开始

```python
from igp_sdk.lifecycle import LifecycleManager
lm = LifecycleManager("product_registry.json")
s = lm.summary()
print(f"Total products: {s['total']}")
```

## 类列表

- `LifecycleManager`

## 版本
`v1.0.0`
