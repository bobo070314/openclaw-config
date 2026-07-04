# IGP v3.0 Absorption Blueprint — 消化行业顶级设计

## 核心理念

> 不是照抄 Cursor/Claude Code/Codex，而是悟出它们的**设计哲学**，化为 IGP 自己的升级。

---

## 学到的东西

### 1. Open SWE (LangChain) — "沙箱化Agent编排"
- **哲学**: 每个任务一个隔离沙箱 → Agent在沙箱里全权操作 → 结果 out-of-band 汇报
- **我们学什么**: 把 IGP 的"虚拟团队PK"升级为"真实沙箱执行"——每个团队派发任务时，不是在文件里模拟，而是在 Docker 容器里真刀真枪跑
- **IGP 改造**: igp_engine.py 派发工单时，可选的执行模式：`mode: simulate|docker|mcp`

### 2. SWE-agent (Princeton) — "bash→edit→done 三环"
- **哲学**: Agent 不需要复杂框架，一个 bash shell + 一个编辑器就够。关键在于**纯粹的观察-行动循环**
- **我们学什么**: IGP 的"3队PK"可以简化为：每队本质就是 `[观察repo]→[bash修]→[git diff]→[打分]` 循环
- **IGP 改造**: 每个 team 的 `execute(task)` 方法就是 `observe() → act() → verify() → score()`

### 3. OpenHands — "多后端Agent调度器"
- **哲学**: 不绑定任何 Agent，通过统一的 ACP (Agent-Client Protocol) 连接不同 Agent 后端
- **我们学什么**: IGP 的14部门 ×3队 = 42个Agent实例，但底层引擎应该共享。不要每个部门造轮子
- **IGP 改造**: 一个 `igp_agent_runner.py` 统一驱动所有 team，通过 MCP 调用工具

### 4. MCP (Model Context Protocol) — "标准工具接口"
- **哲学**: 工具就是API。任何 Agent 可以调用任何工具。关键工具：`filesystem`, `git`, `shell`, `web`, `sequential_thinking`
- **我们学什么**: IGP不需要自己实现代码索引/git操作/沙箱——MCP已经提供了标准实现
- **IGP 改造**: 写一个 `igp_mcp_bridge.py`，把 MCP server 的工具暴露给 IGP 的 team

### 5. Claude Code / Cursor / Codex — "通用模式：感知→推理→行动→验证"
- **哲学**: 所有顶级的编码Agent都遵循同一模式：
  1. **感知**: 读取 repo 结构 + RAG 索引 + 上下文
  2. **推理**: 规划变更方案（思维的链条）
  3. **行动**: 多文件修改（不是单文件）
  4. **验证**: 运行测试 + lint + 确认
- **我们学什么**: 这是通用的"工程师循环"，IGP 的每个 team 都应该按这个循环运作
- **IGP 改造**: team 的执行周期从此改为 感知→推理→行动→验证 四步

### 6. MetaGPT — "多Agent角色协作"
- **哲学**: 软件公司每个角色（PM/架构师/工程师/QA）由不同 Agent 扮演，流水线协作
- **我们学什么**: 这就是IGP早就有的理念！但MetaGPT是真正的AI Agent协作，我们是虚拟管理
- **IGP 改造**: 把 IGP 的"虚拟部门"逐步变成"真实Agent部门"——每个team背后是一个真正的LLM Agent

---

## 升级公式

```
IGP v3.0 = IGP v2.0 管理引擎 
         + MCP 工具层 (文件系统/Git/Shell)
         + Agent 执行层 (每个team一个真正的Agent实例)
         + 沙箱隔离层 (Docker)
         + RAG 知识层 (代码库索引)
```

### 保持独特性
- ✅ PK 竞争机制不丢（但不模拟了——让真实Agent在沙箱里PK）
- ✅ 淘汰再生不丢（做的差的Agent方案被淘汰，换新工具栈）
- ✅ KPI 评分不丢（但评分来自真实执行结果，不是模拟）
- ✅ 空转就绪不丢
