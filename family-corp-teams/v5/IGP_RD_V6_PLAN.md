# IGP 研发部 V6 升级方案
## 面向国际研发部标准：Research→Engineering→Product→Scale

---

## 一、三个AI独立评审机制（替代人工Code Review）

```
吸收PR → Agent A（架构评审）→ Agent B（安全评审）→ Agent C（兼容性评审）
         ↓ 都通过 → 进入研发管道
         ↓ 2票否决 → 退回吸收队列 + 修改意见
```

### 实现方式
**不需要真正3个LLM调用**，直接在AST+模式匹配上做三视角评审：

| 评审Agent | 检查项 | 方法 |
|:---------|:------|:----|
| **架构Agent** | 设计模式/职责单一/耦合度 | 依赖图分析 + 圈复杂度 |
| **安全Agent** | eval/exec/bare except/注入 | 模式匹配（已有部分） |
| **兼容Agent** | 侧写签名API变化/文件结构变化 | AST diff对比 |

**效果**：每个吸收PR自动生成 REVIEW_报告.md，三位Agent各自打分（1-10），<18分驳回。

### 产出文件
- `chromosome0/infra/v6_review_agents.py` — 三Agent评审引擎
- `chromosome0/infra/v6_lifecycle.py` — 生命周期管理

---

## 二、生命周期管理（Research→Alpha→Beta→GA→Deprecated→EOL）

```
Research  →  Alpha  →  Beta  →  GA  →  Deprecated  →  EOL
  (吸收)    (变异)   (部门试用) (正式)   (逐步移除)    (下线)
```

### 每个产品的状态文件（纯dict）

```python
{
    "name": "BugDoctor",
    "version": "1.0.0",
    "stage": "alpha",
    "changelog": ["v1.0.0: 10种bug pattern检测上线"],
    "dependents": ["chromosome9"],
    "api_signature": ["scan_file(path)->List[Bug]", "scan_dir(path)->Dict"],
    "metrics": {"calls": 0, "avg_latency": 0, "error_rate": 0},
}
```

### 产出文件
- `v6/product_registry.json` — 所有产品的注册表
- `v6/lifecycle.py` — 自动升级stage的调度器

---

## 三、CLI 工具箱（研发部可交付物 #1）

### 设计：一行命令给部门员工用

**用法**：
```bash
igp doctor --dir .               # BugDoctor 扫描当前目录
igp analyze --dir .               # CodeAnalyzer 全维度分析
igp complexity --file module.py   # 复杂度分析
igp test --dir .                  # 自动测试生成+运行
igp lifecycle --list              # 所有产品生命周期状态
igp review pr.zip                 # 三Agent评审一个PR包
igp prd new --to market           # 给市场部提交PRD需求
igp metrics --product Doctor      # 看某个产品的使用数据
igp version --product Doctor      # 看版本+changelog
```

### 实现方式
一个 igp_cli.py 入口，argparse 分command。Windows上写 .bat wrapper。

### 产出文件
- `v6/cli/igp.py` — 主入口
- `v6/cli/igp.cmd` — Windows批处理包装
- `v6/cli/commands/doctor.py` — BugDoctor CLI
- `v6/cli/commands/analyze.py` — CodeAnalyzer CLI
- `v6/cli/commands/complexity.py` — ComplexityAnalyzer CLI
- `v6/cli/commands/lifecycle.py` — 生命周期CLI
- `v6/cli/commands/review.py` — 三Agent评审CLI
- `v6/cli/commands/prd.py` — PRD提交CLI
- `v6/cli/commands/metrics.py` — 度量查看CLI
- `v6/cli/commands/version.py` — 版本查看CLI

---

## 四、SDK 发布（研发部可交付物 #2）

### 设计：给部门员工import用的标准化包

**安装方式**（纯文件复制，无pip）：
```bash
igp sdk install Doctor           # 把BugDoctor SDK复制到目标项目
igp sdk update Doctor            # 更新到最新版本
igp sdk list                     # 列出所有可用SDK
```

**用法**（部门员工写代码）：
```python
from igp_sdk.doctor import scan_files, BugReport
from igp_sdk.analyzer import CodeAnalysis
from igp_sdk.complexity import analyze_complexity
from igp_sdk.symbolic import SymbolicEngine
```

**每个SDK包含**：
- `__init__.py` + 主入口（清理公共API）
- `README.md` — quickstart
- `examples/` — 示例代码
- `version.py` — 独立版本号

### 产出目录
- `v6/sdk/doctor/` — BugDoctor SDK
- `v6/sdk/analyzer/` — CodeAnalyzer SDK
- `v6/sdk/complexity/` — ComplexityAnalyzer SDK
- `v6/sdk/symbolic/` — SymbolicEngine SDK
- `v6/sdk/review/` — 三Agent评审SDK
- `v6/sdk/cli/` — 给SDK使用者集成CLI
- `v6/cli/commands/sdk.py` — SDK安装管理CLI

---

## 五、HTTP API 网关（研发部可交付物 #3）

### 设计：让下游部门通过HTTP调用，不接触源码

```
POST /api/v1/doctor/scan
GET  /api/v1/analyze/report
GET  /api/v1/complexity?file=xxx.py
POST /api/v1/review/pr
GET  /api/v1/lifecycle/products
POST /api/v1/prd/submit
GET  /api/v1/metrics/product?name=Doctor
```

### 实现方式
Python内置 http.server（0依赖）。

### 产出文件
- `v6/api/igp_api.py` — HTTP API服务器
- `v6/api/igp_api_routes.py` — 路由注册
- `v6/api/igp_api_client.py` — 给下游部门import的API客户端

---

## 六、PRD 系统（跨部门需求收集）

### 设计：部门员工可以提交产品需求

**CLI 方式**：
```bash
igp prd new --from market --product BugDoctor --title "检测Python 3.14 decorator语法" --priority high
```

**API 方式**：
```python
from igp_sdk.prd import PRDClient
prd = client.submit(department="market", product="BugDoctor", title="检测3.14语法", priority="high")
```

**自动处理流程**：
1. PRD进入队列 → 三Agent评审（可行性/投入/收益）
2. 评审通过 → 自动转化为吸收关键词 → GitHub搜索
3. 搜索到 → 进入吸收队列
4. 吸收完成 → 通知提交人

### 产出文件
- `v6/prd/prd_queue.py` — PRD队列管理
- `v6/prd/prd_review.py` — 三Agent评审
- `v6/prd/prd_auto_search.py` — 自动转GitHub搜索

---

## 七、度量系统（使用数据追踪）

### 设计：每个工具被调用了多少次、错误率、延迟

**数据收集**（零成本，纯文件追加）：
```python
Metrics.record("doctor.scan_file", latency_ms=12, success=True)
```

**存储**（.jsonl）：
```json
{"ts": "15:00:01", "product": "doctor", "method": "scan_file", "latency_ms": 12, "success": true}
{"ts": "15:00:02", "product": "doctor", "method": "scan_file", "latency_ms": 45, "success": false, "error": "SyntaxError"}
```

**查询**：
```bash
igp metrics --product Doctor --period 7d
# Calls: 1,234 | Avg latency: 23ms | Error rate: 0.8% | Top error: SyntaxError
# Most popular: scan_file (890 calls) | Least used: scan_dir (12 calls)
```

### 产出文件
- `v6/metrics/metrics_collector.py` — 数据收集器
- `v6/metrics/metrics_reporter.py` — 报告生成器
- `v6/metrics/data/` — 数据目录（.jsonl）

---

## 八、总体架构图

```
                    ┌────────────────────────────────┐
                    │        吸收管道                  │
                    │  GitHub→三Agent评审→吸收→变异→裂变 │
                    └──────────┬─────────────────────┘
                               │
                    ┌──────────▼─────────────────────┐
                    │        产品注册表                │
                    │  product_registry.json          │
                    │  Research→Alpha→Beta→GA→Dep→EOL│
                    └──────────┬─────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
   ┌─────▼─────┐        ┌─────▼─────┐        ┌─────▼─────┐
   │   CLI     │        │   SDK     │        │   HTTP    │
   │  igp run  │        │ import    │        │   API     │
   │  一行命令  │        │  标准化包  │        │  RESTful  │
   └─────┬─────┘        └─────┬─────┘        └─────┬─────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
                    ┌──────────▼─────────────────────┐
                    │       下游部门                   │
                    │  染色体1-12 + 染色体13_HR        │
                    │  真实使用→PRD→反馈→度量         │
                    └────────────────────────────────┘
                                        ↕
                    ┌────────────────────────────────┐
                    │        反馈闭环                  │
                    │  Metrics → PRD → Research      │
                    │  Error tracking → Bug fix       │
                    └────────────────────────────────┘
```

---

## 九、实施顺序

### 第1波：基础设施（30分钟）
1. `v6/product_registry.json` — 扫描66个文件，登记所有产品
2. `v6/lifecycle.py` — 生命周期管理器
3. `v6/metrics/metrics_collector.py` — 度量收集器

### 第2波：CLI工具箱（40分钟）
4. `v6/cli/igp.py` — 主入口 + argparse
5. `v6/cli/commands/` — 6个命令
6. `v6/cli/igp.cmd` — Windows批处理

### 第3波：SDK标准包（40分钟）
7. 逐个产品封装SDK
8. `v6/cli/commands/sdk.py` — SDK安装管理
9. 每个SDK附带 README.md + examples/

### 第4波：三Agent评审 + PRD + API（30分钟）
10. `v6/prd/` — PRD系统
11. `v6/review/v6_review_agents.py` — 三Agent评审
12. `v6/api/igp_api.py` — HTTP API服务器

---

## 十、预期产出

```bash
# CLI
igp doctor --dir .                # 扫描当前目录的bug
igp lifecycle --list              # 所有产品生命周期
igp metrics --product Doctor      # 使用数据

# SDK
from igp_sdk.doctor import scan_files

# 三Agent评审
igp review pr.zip

# HTTP API
curl http://localhost:8080/api/v1/doctor/scan -d '{"dir":"."}'

# PRD
igp prd new --from market --title "需要TypeScript支持"

# 版本管理
igp version --product Doctor      # 输出版本+changelog
```

---

| 模块 | 解决什么问题 | 文件数 | 行数预估 |
|:----|:-----------|:-----:|:--------|
| 三Agent评审 | 跳过人工code review | 2 | ~300 |
| 生命周期管理 | 版本+兼容性+废弃 | 2 | ~200 |
| CLI工具箱 | 部门员工1行命令用工具 | 9 | ~700 |
| SDK标准包 | 部门员工import标准化 | 20 | ~800 |
| HTTP API | RESTful远程调用 | 3 | ~300 |
| PRD系统 | 跨部门需求采集 | 3 | ~250 |
| 度量系统 | 使用数据驱动决策 | 2 | ~200 |
| **总计** | **7大模块全解决** | **~41** | **~2750** |
