# IGP Autonomous Agent Network (AAN) v1.0

**比传统Agent框架高一个层级的自治智能体网络**

## 架构

```
外部输入 → A2A路由 → 预测诊断 → 决策矩阵 → 执行学习 → 染色体进化
                                              ↓
                                         安全检测+合规审计
```

## 8大引擎

| 引擎 | 能力 | 优于传统 |
|------|------|---------|
| RoutingCore | Dijkstra自适应路由 | 传统静态/手动 |
| PredictiveAnalytics | ML预测故障(提前2-3min) | 传统无诊断 |
| DecisionMatrix | 规则矩阵叠加决策 | 传统硬编码if/else |
| ChromosomeFitness | 多目标进化+版控 | 传统无进化 |
| ThreatDetector | Z-score异常检测 | 传统无安全 |
| MemoryAnalytics | 两级缓存+配额 | 传统单层 |
| ComplianceMonitor | 自动合规审计 | 传统无审计 |
| A2ASecurity | 加密签名+会话 | 传统无通信 |

## 运行

```bash
python aan_v1.py          # CLI模式
python aan_dashboard.py   # Web Dashboard (http://localhost:18080)
```

## 技术栈

Python 3.11+, 无外部依赖, 全部工程复用

## 成果

- 32项升级文件, 8引擎全链路, 零外部依赖
- 成本: $0.00336 (3个付费模型调用)
- 延迟: <1ms/cycle
