
# DocAgent 吸收笔记 — 2026-07-01 14:30

## 来源
- 项目: facebookresearch/DocAgent (ACL 2025)
- 技术: Multi-Agent System + Hierarchical Traversal
- 论文: arXiv 2504.08725

## 核心架构

### 1. 层次遍历 (Hierarchical Traversal)
- 按依赖拓扑排序处理文件
- 先从无依赖的文件开始建文档
- 逐层向上，已文档化的模块为上层提供上下文
- 解决"鸡生蛋"问题：文档化的代码才能解释调用它的代码

### 2. 五Agent协作系统
   Orchestrator（编排器）
   ├── Reader（阅读器）    — 解析代码AST，提取结构
   ├── Searcher（搜索器）  — 搜索内部/外部上下文
   ├── Writer（写手）      — 生成文档字符串  
   └── Verifier（检验器）  — 验证文档质量，迭代改进

### 3. 质量维度
- Completeness: 是否覆盖所有函数/参数/返回/异常
- Helpfulness: 文档是否对使用者有用
- Truthfulness: 文档是否准确反映代码行为

### 4. 评估系统
- AST静态分析驱动的完整性打分
- 不依赖LLM，纯代码分析即可得基础分
- Web UI用于人工评估

## IGP适配要点
- 我们的岗位说明书 = DocAgent的文档字符串 + 扩展的"职责/接口/依赖/调用链"
- 我们不需要LLM → 纯AST分析就能生成类签名+方法列表+属性+依赖关系
- 层次遍历法 → 先扫描无依赖的基类，再处理继承类
