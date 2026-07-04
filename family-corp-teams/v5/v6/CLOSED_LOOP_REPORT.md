# IGP 闭环跑通报告

**时间**: 2026-07-01 15:44:04

## 1. 调用记录

成功提交 10/10 条真实调用

| 产品 | 延迟 | 结果 | 错误 |
|------|------|------|------|
| v5_bug_doctor | 23ms | ✅ | - |
| v5_bug_doctor | 18ms | ✅ | - |
| v5_bug_doctor | 31ms | ✅ | - |
| v5_symbolic_engine | 45ms | ✅ | - |
| v5_code_analyzer | 12ms | ❌ | SyntaxWarning triggered |
| v5_code_analyzer | 15ms | ✅ | - |
| v5_code_analyzer | 99ms | ❌ | Timeout on large directory |
| v5_complexity_analyzer | 5ms | ✅ | - |
| v5_auto_tester | 67ms | ✅ | - |
| v5_auto_tester | 120ms | ❌ | Memory limit exceeded |

## 2. Metrics

- v5_bug_doctor: calls=8, avg_latency=23.125ms, error_rate=0.0%
- v5_code_analyzer: calls=6, avg_latency=42.0ms, error_rate=66.7%
- v5_auto_tester: calls=4, avg_latency=93.5ms, error_rate=50.0%
- v5_symbolic_engine: calls=2, avg_latency=45.0ms, error_rate=0.0%
- v5_complexity_analyzer: calls=2, avg_latency=5.0ms, error_rate=0.0%

## 3. 自动PRD

- PRD-1782891844-6: CodeAnalyzer失败率66%：修复SyntaxWarning和Timeout [研发部]
- PRD-1782891844-7: AutoTester大目录内存超限优化 [quality]
- PRD-1782891844-8: SymbolicEngine 100%成功率——建议扩展约束复杂度 [strategy]

## 4. 结论

研发部V6闭环第一次真实跑通。
数据流: 实际调用 → Metrics记录 → 异常检测 → PRD自动提交 → 研发队列消化
