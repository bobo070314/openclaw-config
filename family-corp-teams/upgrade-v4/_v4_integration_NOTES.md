# IGP v4 集成研发笔记

## 创新点：PK机制嫁接到Provider/安全/审查上

### 1. Provider路由与PK结合
- 多个Provider对同一任务进行PK
- 赢得任务的Provider在未来优先使用
- 实现方式：在ProviderRouter中添加PK逻辑，比较各Provider的响应时间和质量，选择最优者

### 2. Plan/Act与淘汰结合
- Agent连续多次Plan被拒=能力不足→启动淘汰预警
- 实现方式：在PlanActManager中添加记录和评估机制，当连续3次Plan被拒时触发预警

### 3. 代码审查与KPI结合
- 审查中发现重大问题=审查Agent加分，被审查Agent扣分
- 实现方式：在CodeReviewAgent中添加评分系统，根据审查结果调整Agent的KPI

## 其他改进
- Provider抽象层强化：统一的Provider抽象接口（chat/invoke/embed）
- Plan/Act安全模式实现：先出Plan给人看，批准后再Act执行
- 代码审查Agent实现：PR提交后自动diff分析，检查语法错误/类型问题/安全漏洞/代码风格
- 测试脚本：测试三者集成

## 下一步计划
- 实现PK机制在ProviderRouter中的具体逻辑
- 在PlanActManager中添加淘汰预警机制
- 在CodeReviewAgent中添加KPI评分系统
- 进行全面测试和优化