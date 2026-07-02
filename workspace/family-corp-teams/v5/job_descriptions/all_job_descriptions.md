# IGP Job Descriptions
Generated: 2026-07-01T08:43:42.264804+00:00
Total positions: 94 classes

## chromosome0 (8 positions)
  trophy2 | check4 | warning2
### trophy AuditRouter
- **File**: `v5_mutation_fission_live.py`
- **Role**: 变异: SmartRouter + LoggerContext — 每次路由都记录审计日志
- **Capabilities**: 5 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(name)`
  - `register(name, provider, weight)`
  - `route(request, strategy)`
  - `record(name, success, duration_ms)`
  - `circuit_status()`
### warning AutoFixScanner
- **File**: `v5_mutation_fission.py`
- **Role**: 自动修复扫描器 — SafeRunner的安全 + IncrementalScanner的扫描
- **Capabilities**: 2 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `scan_and_fix(path)`
### trophy CodeAnalyzer
- **File**: `v5_code_analyzer.py`
- **Role**: 代码分析器 — 吸收Vulture/rope/Semgrep的精髓
- **Capabilities**: 8 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(base_dir)`
  - `scan_dead_code()` - 吸收Vulture: 检测死代码（未引用的函数/类）
  - `scan_refactoring()` - 吸收rope: 检测可重构代码
  - `scan_bad_patterns()` - 吸收Semgrep: 检测不良模式
  - `scan_mutation_opportunity()` - 自研: 检测可以变异+裂变的组合机会
  - `all_results()`
  - `total_issues()`
  - `report()`
### check FissionEngine
- **File**: `v5_mutation_fission.py`
- **Role**: 裂变引擎 — 从现有染色体分裂出新部门
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `fission(parent, child, modules, description)` - 裂变记录: parent染色体分裂出child染色体
  - `all_fissions()`
### check MutationEngine
- **File**: `v5_mutation_fission.py`
- **Role**: 变异引擎 — 对现有代码做4种突变
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `cross_breed(source_class, donor_class, name)` - 杂交: 两个类的方法合并
  - `auto_generate(source_class, base_class, prefix)` - 自动生成: 基于方法名生成新方法变体
  - `combine_into_hybrid(cls_list, name)` - 多类杂交: 从多个类各取精华组成新类
  - `copy_mutate(source, name)` - 复制变异: 以source为模板创建新类, 部分方法重写
### check SecureResult
- **File**: `v5_mutation_fission_live.py`
- **Role**: 变异: Result + CryptoKit杂交 — Result自带签名验证
- **Capabilities**: 3 methods | 0 props | 1 bases
- **Inherits**: Result
- **Methods**:
  - `sign(key)` - 变异: 成功的Result可以签名
  - `verify(key)` - 变异: 验证签名
  - `meta()`
### warning SmartAuditor
- **File**: `v5_mutation_fission.py`
- **Role**: 审计路由日志器
- **Capabilities**: 2 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `log_route(request)`
### check WatchdogRunner
- **File**: `v5_mutation_fission_live.py`
- **Role**: 变异: SafeRunner + IncrementalScanner — 监视代码变更并自动重试
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `watch_and_run(path, func)` - 监视文件, 变更时自动重试执行
  - `report()`
## chromosome1 (7 positions)
  trophy4 | check2 | warning1
### check FastMCPExport
- **File**: `mcp_v2_upgrade.py`
- **Role**: FastMCP导出器
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(name)`
  - `tool(func, name)` - 注册工具
  - `run(host, port)` - 启动MCP Server
### check FastMCPExporter
- **File**: `fastmcp_export.py`
- **Role**: FastMCP工具导出器
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `export_tools()` - 导出工具清单
  - `count()` - 工具数量
  - `get_schema(name)` - 获取工具schema
### trophy MCPClient
- **File**: `igp_mcp_v5_client.py`
- **Role**: MCP Client - 连接任何MCP Server（stdio/HTTP）
- **Capabilities**: 8 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(server_url)`
  - `connect_stdio(command, args)` - 模拟stdio连接（打印配置就绪）
  - `connect_http(url)` - 连接HTTP MCP Server（模拟）
  - `discover_tools()` - 发现Server上所有工具
  - `call_tool(name, arguments)` - 调用工具并返回结果
  - `get_call_log()` - 获取调用日志（用于PK排名）
  - `get_stats()` - 获取统计信息
  - `is_connected()`
### warning MCPHandler
- **File**: `mcp_v2_upgrade.py`
- **Role**: No description
- **Capabilities**: 1 methods | 0 props | 1 bases
- **Inherits**: BaseHTTPRequestHandler
- **Methods**:
  - `do_GET()`
### trophy MCPServer
- **File**: `igp_mcp_v5_server.py`
- **Role**: MCP Server exporter for IGP Skills
- **Capabilities**: 8 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(skills_package)`
  - `register_tool(name, func, description, input_schema)` - 注册一个工具到MCP Server
  - `register_resource(uri, data_getter, mime_type)` - 注册一个资源
  - `get_tool_list()` - 返回工具列表（符合MCP格式）
  - `call_tool(name, arguments)` - 调用工具
  - `start()` - 模拟启动Server
  - `stop()`
  - `tool_count()`
### trophy MCP_PK_Rank
- **File**: `igp_mcp_pk.py`
- **Role**: MCP PK ranking module
- **Capabilities**: 6 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `update_ranking(server_id, call_count, success_rate, token_efficiency)` - Update the ranking data for a server
  - `get_ranked_servers()` - Get servers ranked by token efficiency
  - `check_eligibility(server_id)` - Check if a server is eligible for promotion or demotion
  - `promote_server(server_id)` - Promote a server
  - `demote_server(server_id)` - Demote a server
### trophy MCPv2Discovery
- **File**: `mcp_v2_upgrade.py`
- **Role**: MCP Server自动发现 (v2)
- **Capabilities**: 6 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `discover_local()` - 扫描本地端口发现MCP Server
  - `discover_pypi(query)` - 扫描PyPI发现MCP Server包
  - `get_tool_list(server_id)` - 获取server的工具列表
  - `get_server_info(server_id)` - 获取Server完整信息
  - `create_evaluation(tool_name)` - 创建工具评分卡
## chromosome10 (7 positions)
  trophy5 | check2 | warning0
### check ContractDecorator
- **File**: `v5_symbolic_engine.py`
- **Role**: 从deal吸收的契约式编程装饰器
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `precondition(check_func)` - 前置条件装饰器
  - `postcondition(check_func)` - 后置条件装饰器
  - `invariant(check_func)` - 类不变量装饰器
### trophy ContractDecoratorV2
- **File**: `v5_logic_upgrade.py`
- **Role**: Design-by-contract: pre/post/invariant with quantifiers
- **Capabilities**: 7 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `precondition(condition, description)` - Decorator: check condition before function executes
  - `postcondition(condition, description)` - Decorator: check condition on return value
  - `invariant(condition, description)` - Register a class invariant
  - `check_invariants(instance)` - Batch check all invariants on an instance
  - `forall(iterable, condition)` - Forall quantifier: ALL elements satisfy condition
  - `exists(iterable, condition)` - Exists quantifier: at least ONE element satisfies condition
### trophy KnowledgeBase
- **File**: `v5_logic_upgrade.py`
- **Role**: Persistent fact/rule knowledge base backed by JSON file
- **Capabilities**: 7 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(path)`
  - `_load()`
  - `_save()`
  - `add_fact(predicate)` - Add a fact with optional confidence score
  - `add_rule(antecedents, consequent, name, weight)` - Add an inference rule: if ALL antecedents match, THEN consequent
  - `query(predicate)` - Query facts by predicate
  - `clear()`
### trophy LogicReasoner
- **File**: `v5_symbolic_engine.py`
- **Role**: 逻辑推理引擎 — 规则匹配 + 变量替换推理链
- **Capabilities**: 5 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `add_rule(rule_name, premise, conclusion)` - 添加推理规则: 如果premise成立则conclusion成立
  - `add_fact(fact)` - 添加已知事实
  - `_substitute(template, var, value)` - 替换变量 (如 man(X) + X=Socrates -> man(Socrates))
  - `reason(query)` - 前向推理: 能否证明query成立
### check LogicReasonerV2
- **File**: `v5_logic_upgrade.py`
- **Role**: First-order logic reasoner with unlimited depth and persistent KB
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(kb)`
  - `forward_chain(max_iterations)` - Forward chaining: apply rules to derive new facts
  - `backward_chain(goal_predicate, goal_args, depth)` - Backward chaining: find proof for a goal
  - `explain(fact_id)` - Explain how a fact was derived
### trophy SymbolicEngine
- **File**: `v5_symbolic_engine.py`
- **Role**: 纯Python符号推理引擎（从Z3吸收核心思想）
- **Capabilities**: 6 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `add_var(name, vtype, bounds)` - 声明符号变量
  - `add_constraint(expr)` - 添加约束条件
  - `solve()` - 简单约束求解器（区间传播）
  - `check()` - 检查当前约束是否可满足
  - `infer_return_type(func)` - 从函数体推断返回类型
### trophy SymbolicEngineV2
- **File**: `v5_logic_upgrade.py`
- **Role**: Symbolic constraint solver supporting int, string, bool, set types
- **Capabilities**: 5 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `declare(name, var_type, domain)` - Declare a symbolic variable
  - `_default_domain(var_type)`
  - `add_constraint(expr)` - Add a constraint expression (lambda or string)
  - `solve(max_solutions)` - Solve constraints via backtracking
## chromosome11 (1 positions)
  trophy1 | check0 | warning0
### trophy ComplexityAnalyzer
- **File**: `v5_complexity_analyzer.py`
- **Role**: 纯Python圈复杂度分析器 (从radon吸收核心算法)
- **Capabilities**: 10 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `analyze_file(filepath)` - 分析单文件
  - `_calc_complexity(func_node)` - 计算圈复杂度: 1(基线) + if/while/for/except/and/or/assert
  - `_nasa_rank(complexity)`
  - `_has_docstring(node)`
  - `_has_type_hints(node)`
  - `_infer_type(node)` - AST推断函数类型
  - `_maintainability_index(avg_complexity, total_lines)` - Maintainability Index简化版
  - ... +2 more
## chromosome12 (10 positions)
  trophy6 | check1 | warning3
### trophy AutoTester
- **File**: `v5_auto_tester.py`
- **Role**: 属性测试生成器 (从Hypothesis吸收核心思想)
- **Capabilities**: 5 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(seed)`
  - `_generate_value(param_type, param_name)` - 根据类型生成边界测试值
  - `_infer_params(func)` - 从函数签名推断参数类型
  - `test_function(func, test_count)` - 对函数运行自动测试
  - `report()` - 生成测试报告
### trophy AutoTester
- **File**: `v5_auto_tester_v2.py`
- **Role**: 自动测试器 — 全自动运行/验证/报告
- **Capabilities**: 5 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(base_dir)`
  - `add_suite(name, suite)`
  - `run_module(module_path)` - 安全运行一个模块的测试
  - `run_all_modules()` - 扫描并运行目录下所有Python模块
  - `generate_report(results)` - 生成Markdown测试报告
### trophy LoggerContext
- **File**: `v5_logger_context.py`
- **Role**: 上下文日志器 — bind/unbind/with_context/json_output/auto_caller
- **Capabilities**: 16 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(name, ctx)`
  - `get(cls, name)`
  - `bind()`
  - `unbind()`
  - `with_context()`
  - `bind_global(cls)`
  - `json_output(cls, enabled)`
  - `set_level(cls, level)`
  - ... +8 more
### warning Result
- **File**: `v5_auto_tester.py`
- **Role**: No description
- **Capabilities**: 2 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(ok, value, error)`
  - `__repr__()`
### trophy Result
- **File**: `v5_result_monad.py`
- **Role**: Result[T, E] — 显式成功/失败
- **Capabilities**: 17 methods | 0 props | 1 bases
- **Inherits**: Subscript(value=Name(id='Generic', ctx=Load()), slice=Tuple(elts=[Name(id='T', ctx=Load()), Name(id='E', ctx=Load())], ctx=Load()), ctx=Load())
- **Methods**:
  - `__init__(ok, value, error)`
  - `Ok(cls, value)`
  - `Err(cls, error)`
  - `is_ok()`
  - `is_err()`
  - `unwrap()`
  - `unwrap_or(default)`
  - `unwrap_or_else(fn)`
  - ... +9 more
### warning SafeRunner
- **File**: `v5_auto_tester.py`
- **Role**: 安全的函数执行器 — 统一异常治理
- **Capabilities**: 1 methods | 0 props | 0 bases
- **Methods**:
  - `run(func)`
### trophy SafeRunner
- **File**: `v5_safe_runner.py`
- **Role**: 安全执行器v2 — 重试+超时+熔断+批量
- **Capabilities**: 9 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(default_retries, default_timeout)`
  - `run(func)`
  - `run_async(func)`
  - `batch_run(funcs, max_workers)`
  - `with_sandbox(func)`
  - `circuit_breaker(name, failure_threshold, recovery_timeout)`
  - `_update_stats(name, success)`
  - `statistics()`
  - ... +1 more
### check TestResult
- **File**: `v5_auto_tester_v2.py`
- **Role**: 测试结果 — 使用Result monad作为internal
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(name, passed, details, duration_ms)`
  - `from_result(cls, name, result, duration_ms)`
  - `to_dict()`
### trophy TestSuite
- **File**: `v5_auto_tester_v2.py`
- **Role**: 测试套件 — 带SafeRunner重试+超时保护
- **Capabilities**: 5 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(name)`
  - `add(name, func)` - 添加一个测试用例
  - `run_all()` - 运行全部测试
  - `run_safe(name, func)` - 单测试安全执行
  - `statistics()`
### warning V5Logger
- **File**: `v5_auto_tester.py`
- **Role**: 统一日志系统 — 自动注入所有V5模块
- **Capabilities**: 1 methods | 0 props | 0 bases
- **Methods**:
  - `get(cls, name)`
## chromosome13_hr (4 positions)
  trophy0 | check1 | warning3
### warning JobDescription
- **File**: `v5_hr_engine.py`
- **Role**: 岗位说明书 — 单个类的职责/接口/依赖/调用链
- **Capabilities**: 2 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(class_name, file_path, chromosome)`
  - `to_dict()`
### check Reader
- **File**: `v5_hr_engine.py`
- **Role**: DocAgent Reader — 解析代码AST，提取结构
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(base_dir)`
  - `scan()`
  - `_parse_file(fp, chromosome)`
  - `_base_name(node)`
### warning ReportWriter
- **File**: `v5_hr_engine.py`
- **Role**: DocAgent Writer — 输出岗位说明书
- **Capabilities**: 2 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(jobs)`
  - `write_md(out_path)`
### warning Verifier
- **File**: `v5_hr_engine.py`
- **Role**: DocAgent Verifier — 验证岗位说明书完整性
- **Capabilities**: 2 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(jobs)`
  - `verify()`
## chromosome2 (6 positions)
  trophy3 | check3 | warning0
### trophy A2AFederation
- **File**: `a2a_v2_upgrade.py`
- **Role**: A2A联邦 — Agent发现 + 注册 + 广播
- **Capabilities**: 8 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `register(card)` - 注册一个Agent到联邦
  - `unregister(agent_id)` - 注销Agent
  - `find_by_capability(capability)` - 按能力查找Agent
  - `find_by_skill(skill_name)` - 按技能名称查找Agent
  - `broadcast(query, capability)` - 广播消息到匹配的Agent
  - `list_all()` - 列出所有Agent
  - `count()`
### trophy A2ATaskProtocol
- **File**: `a2a_v2_upgrade.py`
- **Role**: A2A任务协议 — 任务发送/流式/取消 (JSON-RPC 2.0)
- **Capabilities**: 5 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `create_task(agent_id, query, session_id, metadata)` - 创建任务 JSON-RPC 2.0
  - `create_streaming(agent_id, query)` - 创建流式任务 (JSON-RPC 2.0)
  - `cancel_task(task_id)` - 取消任务
  - `get_task_status(task_id)` - 获取任务状态
### check AgentCard
- **File**: `a2a_agent_card.py`
- **Role**: Agent身份/能力/端点描述
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `to_dict()` - JSON序列化
  - `from_dict(cls, data)` - JSON反序列化
  - `save(path)` - 保存为.card.json文件
  - `load(cls, path)` - 从.card.json文件加载
### check AgentCard
- **File**: `a2a_v2_upgrade.py`
- **Role**: A2A Agent Card — Agent身份描述 (符合Google A2A标准)
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(name, description, url, version, capabilities)`
  - `add_skill(skill_id, name, description, input_schema, output_schema)` - 添加一个技能
  - `to_json()`
  - `to_dict()`
### trophy AgentDiscoveryService
- **File**: `a2a_discovery.py`
- **Role**: Agent发现服务实现
- **Capabilities**: 7 methods | 0 props | 0 bases
- **Methods**:
  - `__post_init__()`
  - `register(agent_card)` - 注册Agent Card
  - `find_by_capability(capability, value)` - 根据能力查找Agent
  - `broadcast(message, exclude_ids)` - 广播消息到所有Agent
  - `get_all_agents()` - 获取所有注册的Agent
  - `save_registry(path)` - 保存注册表到文件
  - `load_registry(path)` - 从文件加载注册表
### check TaskMessage
- **File**: `a2a_task_protocol.py`
- **Role**: A2A任务协议消息结构
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `to_dict()` - 转换为字典
  - `to_json()` - 转换为JSON字符串
  - `from_json(cls, json_str)` - 从JSON字符串解析
  - `is_streaming()` - 判断是否为流式消息
## chromosome3 (6 positions)
  trophy5 | check1 | warning0
### trophy SkillMarket
- **File**: `skill_market.py`
- **Role**: No description
- **Capabilities**: 6 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `add_skill(skill_name, metadata, instructions)`
  - `rate_skill(skill_name, score)`
  - `get_top_skills(limit)`
  - `install_skill(skill_name)`
  - `uninstall_skill(skill_name)`
### trophy SkillPKRank
- **File**: `skill_pk_rank.py`
- **Role**: No description
- **Capabilities**: 5 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `update_stats(skill_name, success_rate, token_usage)`
  - `calculate_score(skill_name)`
  - `rank_skills()`
  - `check_promotion(skill_name)`
### check SkillPluginLoader
- **File**: `v5_market_upgrade.py`
- **Role**: No description
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(registry)`
  - `load_skill(skill_path)`
  - `_parse_skill_metadata(content)`
### trophy SkillRegistry
- **File**: `v5_market_upgrade.py`
- **Role**: No description
- **Capabilities**: 8 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `add_skill(skill_id, metadata)`
  - `remove_skill(skill_id)`
  - `get_skill(skill_id)`
  - `search_skills(query)`
  - `list_all_skills()`
  - `get_tags()`
  - `get_keywords()`
### trophy SkillSearchEngine
- **File**: `v5_market_upgrade.py`
- **Role**: No description
- **Capabilities**: 5 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(registry)`
  - `search(query)`
  - `list_all()`
  - `get_tags()`
  - `get_keywords()`
### trophy SkillVersionManager
- **File**: `v5_market_upgrade.py`
- **Role**: No description
- **Capabilities**: 6 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(registry)`
  - `get_version(skill_id)`
  - `set_version(skill_id, version)`
  - `get_dependencies(skill_id)`
  - `set_dependencies(skill_id, dependencies)`
  - `check_dependencies(skill_id)`
## chromosome4 (10 positions)
  trophy2 | check7 | warning1
### check CircuitBreaker
- **File**: `v5_provider_upgrade.py`
- **Role**: No description
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(max_failures, reset_timeout)`
  - `is_open(provider)`
  - `record_failure(provider)`
  - `reset(provider)`
### check HealthChecker
- **File**: `v5_provider_upgrade.py`
- **Role**: No description
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(providers)`
  - `check_health()`
  - `get_healthy_providers()`
### check MockProvider
- **File**: `run.py`
- **Role**: No description
- **Capabilities**: 4 methods | 0 props | 1 bases
- **Inherits**: ProviderAbstraction
- **Methods**:
  - `__init__(name)`
  - `chat(prompt, model)`
  - `invoke(command, model)`
  - `embed(text, model)`
### trophy ProviderAbstraction
- **File**: `provider_abstraction.py`
- **Role**: Provider抽象层 — 统一调用/嵌入/调用接口
- **Capabilities**: 6 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(name)`
  - `add_model(name, handler)`
  - `chat(model, messages)` - 通用对话调用 — 代理到具体Provider
  - `embed(model, texts)` - 通用嵌入调用
  - `invoke(model, fn_name, args)` - 通用函数调用
  - `list_models()`
### check ProviderPK
- **File**: `provider_pk.py`
- **Role**: No description
- **Capabilities**: 4 methods | 0 props | 1 bases
- **Inherits**: ProviderAbstraction
- **Methods**:
  - `__init__(providers)`
  - `update_scores()`
  - `get_provider_ranking()`
  - `chat(prompt, model)`
### check ProviderPK
- **File**: `v5_provider_upgrade.py`
- **Role**: No description
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(providers)`
  - `update_elo_score(provider, result)`
  - `get_top_providers(count)`
### check SmartRouter
- **File**: `provider_router.py`
- **Role**: No description
- **Capabilities**: 3 methods | 0 props | 1 bases
- **Inherits**: ProviderAbstraction
- **Methods**:
  - `__init__(providers)`
  - `route(task)`
  - `chat(prompt, model)`
### warning SmartRouter
- **File**: `v5_provider_upgrade.py`
- **Role**: No description
- **Capabilities**: 2 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(providers, white_list)`
  - `route_request(request)`
### trophy SmartRouter
- **File**: `v5_smart_router.py`
- **Role**: 智能路由v2 — 4种策略 + 熔断器 + A/B + 灰度
- **Capabilities**: 17 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(name)`
  - `register(name, provider, weight)`
  - `unregister(name)`
  - `select(request, strategy)`
  - `route(request, strategy)`
  - `circuit_breaker(name, threshold, timeout)`
  - `_check_circuit(name)`
  - `record_success(name, duration_ms)`
  - ... +9 more
### check WeightedLoadBalancer
- **File**: `v5_provider_upgrade.py`
- **Role**: No description
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(providers)`
  - `get_next_provider()`
  - `get_provider_by_weight()`
## chromosome5 (4 positions)
  trophy2 | check1 | warning1
### trophy GuardianAct
- **File**: `guardian_act.py`
- **Role**: Guardian行动者 — 队列/黑白名单管理
- **Capabilities**: 7 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `add_to_queue(item)` - 添加项目到审核队列
  - `process_queue()` - 处理队列
  - `update_whitelist(entity, reason)` - 更新白名单
  - `update_blacklist(entity, reason)` - 更新黑名单
  - `is_allowed(entity)` - 检查是否允许
  - `stats()`
### check GuardianPlan
- **File**: `guardian_act.py`
- **Role**: Guardian执行计划
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(name)`
  - `add_step(action)`
  - `execute()` - 执行计划
### trophy GuardianPlan
- **File**: `guardian_plan.py`
- **Role**: Plan阶段：只读分析，不执行任何修改
- **Capabilities**: 6 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `receive_request(request)` - 接收操作请求
  - `analyze_risk()` - 分析风险等级
  - `generate_report()` - 生成Plan报告
  - `get_actions()` - 获取已记录的操作请求
  - `execute()` - 不执行任何修改
### warning GuardianPolicy
- **File**: `guardian_act.py`
- **Role**: Guardian策略管理
- **Capabilities**: 1 methods | 0 props | 0 bases
- **Methods**:
  - `log_misclassification(entity, policy, reason)` - 记录误分类
## chromosome6 (8 positions)
  trophy5 | check3 | warning0
### trophy ACPClient
- **File**: `acp_client.py`
- **Role**: No description
- **Capabilities**: 9 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(api_url)`
  - `create_checkout(payload)`
  - `get_cart(cart_id)`
  - `update_cart_item(cart_id, item_id, payload)`
  - `delete_cart_item(cart_id, item_id)`
  - `checkout(cart_id)`
  - `get_quote(product_id)`
  - `place_order(order_data)`
  - ... +1 more
### trophy AgentCommerce
- **File**: `agent_commerce.py`
- **Role**: No description
- **Capabilities**: 8 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(aap_api_url, acp_api_url)`
  - `register_service_provider(service_name, pricing_model, price_per_token, price_per_task)`
  - `set_pricing_strategy(strategy, parameters)`
  - `track_revenue(service_name, revenue_amount)`
  - `generate_profit_report(start_date, end_date)`
  - `handle_inquiry(inquiry_data)`
  - `place_order(order_data)`
  - `process_payment(payment_data)`
### trophy AgentCommerceEngine
- **File**: `agent_commerce_v2.py`
- **Role**: Agent商业交易引擎
- **Capabilities**: 5 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `register_service(agent_id, service_name, price_per_task)` - 注册Agent服务
  - `charge_task(agent_id, task_name, tokens)` - 对任务收费（模拟）
  - `get_revenue(agent_id)` - 获取收入
  - `get_report()` - 生成收入报告
### trophy CommercePK
- **File**: `commerce_pk.py`
- **Role**: No description
- **Capabilities**: 6 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(commerce_engine)`
  - `rank_services_by_income(start_date, end_date)`
  - `rank_services_by_profit_margin(start_date, end_date)`
  - `rank_services_by_customer_satisfaction(start_date, end_date)`
  - `eliminate_losing_services(start_date, end_date)`
  - `reward_high_profit_services(start_date, end_date)`
### trophy CommercePKRank
- **File**: `commerce_pk_v2.py`
- **Role**: 商业PK排名引擎 v2
- **Capabilities**: 6 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `register(agent_id, name)` - 注册一个商业服务
  - `record_transaction(agent_id, revenue, cost, rating)` - 记录一笔交易
  - `get_ranking()` - 获取排名（按综合得分）
  - `eliminate(min_score)` - 淘汰低分服务
  - `score_summary()` - 生成评分摘要
### check PayPalIntegration
- **File**: `agent_commerce_v2.py`
- **Role**: PayPal 支付集成 (FREE_MODE锁定)
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(client_id, client_secret)`
  - `create_payment(amount, currency)` - 创建支付
  - `execute_payment(payment_id, payer_id)` - 执行支付
### check ShopifyIntegration
- **File**: `agent_commerce_v2.py`
- **Role**: Shopify 电商集成 (FREE_MODE锁定)
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(access_token, store)`
  - `list_products()` - 列出商品
  - `create_order(line_items)` - 创建订单
### check StripeIntegration
- **File**: `agent_commerce_v2.py`
- **Role**: Stripe 支付集成 (FREE_MODE锁定，永远不真发请求)
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(api_key)`
  - `create_customer(email, name)` - 创建客户
  - `create_charge(amount, currency, customer_id, description)` - 创建收款
  - `get_balance()` - 获取余额
## chromosome7 (9 positions)
  trophy5 | check4 | warning0
### trophy AgentOSKernel
- **File**: `agent_os_kernel.py`
- **Role**: Agent OS内核 — IO/路由/预算管理
- **Capabilities**: 7 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(name)`
  - `register_agent(agent_id, handler)`
  - `send_message(to, msg, sender)` - 发送消息到指定Agent
  - `receive()` - 接收下一条消息
  - `stop()` - 停止内核
  - `_manage_token_budget(max_budget)` - 管理token预算
  - `status()`
### check AgentOSScheduler
- **File**: `agent_os_kernel.py`
- **Role**: Agent OS调度器 — 任务调度/预算管理
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `add_task(task_id, func, priority)`
  - `_manage_token_budget(max_budget)` - 管理调度器的token预算
  - `run_pending()`
### check AgentOSScheduler
- **File**: `agent_os_scheduler.py`
- **Role**: No description
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `schedule(processes)`
  - `_is_priority_task(process_id)`
  - `_manage_token_budget(process_id)`
### check AgentOSShell
- **File**: `agent_os_kernel.py`
- **Role**: Agent OS Shell — CLI/帮助
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(kernel)`
  - `run_command(cmd)`
  - `_show_help()` - 显示帮助
### trophy AgentOSShell
- **File**: `agent_os_shell.py`
- **Role**: No description
- **Capabilities**: 8 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(kernel)`
  - `start()`
  - `_run_chromosome(process_id)`
  - `_show_processes()`
  - `_show_resource_usage()`
  - `_show_logs(process_id)`
  - `_show_help()`
  - `stop()`
### trophy IPCChannel
- **File**: `v5_agent_os_upgrade.py`
- **Role**: Inter-process communication via message queues and event bus
- **Capabilities**: 6 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `send(channel, message, sender)` - Send a message to a channel queue
  - `receive(channel, timeout)` - Receive from a channel queue (blocking with timeout)
  - `subscribe(event_type, callback)` - Subscribe to event bus notifications
  - `_publish(event_type, data)`
  - `stats()` - Return queue depth per channel
### trophy KernelV2
- **File**: `v5_agent_os_upgrade.py`
- **Role**: Agent OS Kernel v2 — process management, monitoring, watchdog
- **Capabilities**: 6 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `spawn(name, func, args, priority, token_limit)` - Spawn a new process
  - `start_watchdog()` - Start the watchdog monitor thread
  - `stop_watchdog()`
  - `get_monitor()` - Return full system monitor snapshot
  - `kill(pid)` - Kill a process by pid
### check ProcessScheduler
- **File**: `v5_agent_os_upgrade.py`
- **Role**: Multi-level priority scheduler with thread pool
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(max_workers)`
  - `submit(func, args, priority, name)` - Submit a task to the scheduler
  - `run_once()` - Execute one cycle: drain queues by priority
  - `get_status()` - Return snapshot of scheduler state
### trophy TokenBudget
- **File**: `v5_agent_os_upgrade.py`
- **Role**: Token budget manager with real-time tracking
- **Capabilities**: 6 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(default_limit)`
  - `register_agent(agent_id, limit)` - Register an agent with a token budget
  - `allocate(agent_id, task_id, tokens)` - Allocate tokens to a task for an agent
  - `consume(task_id, tokens)` - Consume tokens from a task allocation
  - `get_usage(agent_id)` - Return usage report for agent or all
  - `reset(agent_id)` - Reset budgets for agent or all
## chromosome8 (8 positions)
  trophy3 | check3 | warning2
### check AP2PaymentGateway
- **File**: `ap2_payment_gateway.py`
- **Role**: No description
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `register_wallet(wallet_id, currency)`
  - `process_payment_request(payment_request)`
### check AP2PaymentGateway
- **File**: `v5_ap2_upgrade.py`
- **Role**: AP2支付网关 — 评分+结算+交易
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `update_elo_score(agent_id, result)` - 更新Agent ELO评分
  - `record_settlement(agent_id, amount, action)` - 记录结算
  - `reset()` - 重置评分
### trophy AP2Protocol
- **File**: `ap2_protocol.py`
- **Role**: No description
- **Capabilities**: 6 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `create_payment_request(sender_agent_id, receiver_agent_id, amount, currency, memo)`
  - `verify_payment_request(payment_request)`
  - `aggregate_micro_payments(payments)`
  - `create_receipt(payment_request, transaction_id)`
  - `create_invoice(payment_request, transaction_id, status)`
### warning AP2Protocol
- **File**: `ap2_wallet.py`
- **Role**: AP2协议处理
- **Capabilities**: 2 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `create_wallet(address)`
### check AP2Wallet
- **File**: `ap2_wallet.py`
- **Role**: AP2钱包 — 交易记录/余额管理
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(address)`
  - `process_payment(payment_request)`
  - `get_transactions(limit)`
  - `get_balance()`
### trophy CryptoKit
- **File**: `v5_crypto_kit.py`
- **Role**: 加密工具套件 — 签名/哈希/加密/密钥管理/JWT
- **Capabilities**: 12 methods | 0 props | 0 bases
- **Methods**:
  - `hash(data, algo)`
  - `hmac_sign(key, msg, algo)`
  - `hmac_verify(key, msg, sig, algo)`
  - `gen_key(bits)`
  - `gen_token(bytes_count)`
  - `gen_keypair()`
  - `sign(private_key, msg)`
  - `verify(public_key, msg, sig)`
  - ... +4 more
### trophy KeyManager
- **File**: `v5_crypto_kit.py`
- **Role**: 密钥管理器
- **Capabilities**: 5 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `add_key(kid, key, ktype)`
  - `get_key(kid)`
  - `rotate(kid, new_key)`
  - `derive(master, ctx, bits)`
### warning SignatureVerifier
- **File**: `v5_crypto_kit.py`
- **Role**: 签名验证器 — 继承CryptoKit全部功能
- **Capabilities**: 0 methods | 0 props | 1 bases
- **Inherits**: CryptoKit
- **Methods**:
## chromosome9 (6 positions)
  trophy2 | check2 | warning2
### check AutoFixer
- **File**: `v5_code_repair_upgrade.py`
- **Role**: No description
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(file_path)`
  - `_read_file()`
  - `_write_file(content)`
  - `apply_fix(pattern)`
### check BugDoctor
- **File**: `v5_bug_doctor.py`
- **Role**: V5代码Bug扫描器
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `scan_file(filepath)` - 扫描单个文件，返回bugs列表
  - `scan_directory(directory, pattern)` - 扫描整个目录
  - `get_report()` - 生成扫描报告
### trophy BugDoctorV2
- **File**: `v5_code_repair_upgrade.py`
- **Role**: No description
- **Capabilities**: 6 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `scan_file(filepath)`
  - `scan_directory(directory, pattern)`
  - `get_report()`
  - `auto_fix(file_path, pattern_name)`
  - `incremental_scan(git_diff)`
### warning Change
- **File**: `v5_incremental_scanner.py`
- **Role**: 单次代码变更
- **Capabilities**: 1 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(path, ctype, lines, old_hash, new_hash)`
### warning IncrementalScanner
- **File**: `v5_code_repair_upgrade.py`
- **Role**: No description
- **Capabilities**: 2 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(git_diff)`
  - `scan_changes()`
### trophy IncrementalScanner
- **File**: `v5_incremental_scanner.py`
- **Role**: 增量扫描器v2 — diff/scan/watch/report
- **Capabilities**: 10 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `_file_hash(path)`
  - `scan_diff(diff_text, base_dir)`
  - `scan_file(path, last_version)`
  - `track_change(path, ctype, lines)`
  - `watch(directory, recursive, interval, callback)`
  - `stop_watch()`
  - `report(fmt)`
  - ... +2 more

---

Summary: 94 classes | trophy45 advanced