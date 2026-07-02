# BugDoctor SDK v1.0.0

10种bug pattern检测：死锁/竞态/内存泄露/N+1/注入等

## 快速开始

```python
from igp_sdk.doctor import BugDoctor
d = BugDoctor()
d.scan_directory(".")
report = d.get_report()
print(f"Found {len(report)} issues")
```

## 类列表

- `BugDoctor`

## 版本
`v1.0.0`
