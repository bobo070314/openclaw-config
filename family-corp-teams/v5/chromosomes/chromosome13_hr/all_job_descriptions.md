# IGP Job Descriptions
Generated: 2026-07-01T06:31:10.784263+00:00
Total positions: 70 classes

## chromosome1 (6 positions)
  trophy4 | check2 | warning0
### check FastMCPExporter
- **File**: `mcp_v2_upgrade.py`
- **Role**: FastMCP格式导出器 —— 把IGP Skills导出为FastMCP兼容Server
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `add_tool(name, func, description, input_schema)` - 添加一个工具（FastMCP兼容格式）
  - `export_fastmcp_py(output_path)` - 导出为FastMCP兼容的Python文件
  - `export_mcp_json()` - 导出MCP Server的JSON清单
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
### trophy MCPRegistry
- **File**: `mcp_v2_upgrade.py`
- **Role**: MCP服务器注册表 —— 自动发现生态中的MCP Server
- **Capabilities**: 6 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `register_stdio(server_id, command, args, name, description)` - 注册一个stdio MCP Server
  - `register_http(server_id, url, name, description)` - 注册一个HTTP MCP Server
  - `discover_local(scan_ports)` - 扫描本地端口，发现MCP Server
  - `discover_pypi(query)` - 扫描PyPI发现MCP Server包
  - `get_tool_list(server_id)` - 获取Server的工具列表
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
### check MCPServerRank
- **File**: `mcp_v2_upgrade.py`
- **Role**: MCP Server PK排名 v2
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `record_call(server_id, success, duration_ms, tokens, error)` - 记录一次MCP调用
  - `get_ranking()` - 按效率排名
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
## chromosome12 (4 positions)
  trophy1 | check0 | warning3
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
### warning Result
- **File**: `v5_auto_tester.py`
- **Role**: No description
- **Capabilities**: 2 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(ok, value, error)`
  - `__repr__()`
### warning SafeRunner
- **File**: `v5_auto_tester.py`
- **Role**: 安全的函数执行器 — 统一异常治理
- **Capabilities**: 1 methods | 0 props | 0 bases
- **Methods**:
  - `run(func)`
### warning V5Logger
- **File**: `v5_auto_tester.py`
- **Role**: 统一日志系统 — 自动注入所有V5模块
- **Capabilities**: 1 methods | 0 props | 0 bases
- **Methods**:
  - `get(cls, name)`
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
  trophy0 | check9 | warning1
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
- **Inherits**: Provider
- **Methods**:
  - `__init__(name)`
  - `chat(prompt, model)`
  - `invoke(command, model)`
  - `embed(text, model)`
### check Provider
- **File**: `provider_abstraction.py`
- **Role**: No description
- **Capabilities**: 3 methods | 0 props | 1 bases
- **Inherits**: ABC
- **Methods**:
  - `chat(prompt, model)`
  - `invoke(command, model)`
  - `embed(text, model)`
### check ProviderPK
- **File**: `provider_pk.py`
- **Role**: No description
- **Capabilities**: 4 methods | 0 props | 1 bases
- **Inherits**: ProviderRouter
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
### check ProviderRouter
- **File**: `provider_abstraction.py`
- **Role**: No description
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(providers)`
  - `route(task)`
  - `chat(prompt, model)`
### check SmartRouter
- **File**: `provider_router.py`
- **Role**: No description
- **Capabilities**: 3 methods | 0 props | 1 bases
- **Inherits**: ProviderRouter
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
### check WeightedLoadBalancer
- **File**: `v5_provider_upgrade.py`
- **Role**: No description
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(providers)`
  - `get_next_provider()`
  - `get_provider_by_weight()`
## chromosome5 (3 positions)
  trophy3 | check0 | warning0
### trophy GuardianAct
- **File**: `guardian_act.py`
- **Role**: No description
- **Capabilities**: 7 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `add_to_queue(action)` - 添加需要审批的操作队列
  - `create_checkpoint(file_path)` - 创建安全回滚点
  - `auto_rollback(checkpoint_id)` - 自动回滚
  - `execute_actions()` - 执行审批通过的操作
  - `update_whitelist(new_entries)` - 更新操作白名单
  - `update_blacklist(new_entries)` - 更新操作黑名单
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
### trophy GuardianPolicy
- **File**: `guardian_policy.py`
- **Role**: No description
- **Capabilities**: 5 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `check_file_op(file_path)` - 检查文件操作策略
  - `check_command_exec(command)` - 检查命令执行策略
  - `check_mcp_call(method)` - 检查MCP调用策略
  - `log_misclassification(item)` - 记录误报/漏报
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
## chromosome7 (8 positions)
  trophy5 | check3 | warning0
### trophy AgentOSKernel
- **File**: `agent_os_kernel.py`
- **Role**: No description
- **Capabilities**: 11 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `create_process(process_id, token_budget)`
  - `allocate_token(process_id, amount)`
  - `release_token(process_id, amount)`
  - `send_message(sender, receiver, message)`
  - `receive_message(process_id)`
  - `get_process_status(process_id)`
  - `get_memory_usage(process_id)`
  - ... +3 more
### check AgentOSScheduler
- **File**: `agent_os_kernel.py`
- **Role**: No description
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `schedule(processes)`
  - `_is_priority_task(process_id)`
  - `_manage_token_budget(process_id)`
### check AgentOSScheduler
- **File**: `agent_os_scheduler.py`
- **Role**: No description
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `schedule(processes)`
  - `_is_priority_task(process_id)`
  - `_manage_token_budget(process_id)`
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
## chromosome8 (7 positions)
  trophy3 | check3 | warning1
### check AP2PaymentGateway
- **File**: `ap2_payment_gateway.py`
- **Role**: No description
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `register_wallet(wallet_id, currency)`
  - `process_payment_request(payment_request)`
### trophy AP2PaymentGateway
- **File**: `v5_ap2_upgrade.py`
- **Role**: AP2 Payment Gateway v2 with full functionality
- **Capabilities**: 8 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `register_wallet(wallet_address, public_key)` - Register a wallet with its public key
  - `process_payment(transaction_data)` - Process a payment transaction
  - `refund_payment(transaction_id, amount)` - Process a refund
  - `generate_invoice(transaction_id, amount)` - Generate an invoice
  - `get_balance(wallet_address)` - Get wallet balance
  - `get_transaction_history(wallet_address)` - Get transaction history
  - `settle()` - Perform settlement
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
### trophy AP2Wallet
- **File**: `ap2_wallet.py`
- **Role**: No description
- **Capabilities**: 11 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(wallet_id, currency)`
  - `_load_transactions()`
  - `_save_transactions()`
  - `add_transaction(transaction)`
  - `update_balance(amount)`
  - `set_budget(budget)`
  - `check_budget(amount)`
  - `get_balance()`
  - ... +3 more
### check DoubleSpendDetector
- **File**: `v5_ap2_upgrade.py`
- **Role**: Detects double spending by tracking transaction hashes
- **Capabilities**: 3 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `detect_double_spend(transaction_hash)` - Check if transaction hash has been seen before
  - `reset()` - Clear all recorded transactions
### check SettlementEngine
- **File**: `v5_ap2_upgrade.py`
- **Role**: Handles off-chain settlement and reconciliation
- **Capabilities**: 4 methods | 0 props | 0 bases
- **Methods**:
  - `__init__()`
  - `record_settlement(transaction_id, amount, timestamp)` - Record a settlement transaction
  - `reconcile()` - Reconcile all settlements
  - `generate_invoice(transaction_id, amount)` - Generate an invoice for a transaction
### warning SignatureVerifier
- **File**: `v5_ap2_upgrade.py`
- **Role**: Verifies Ed25519 signatures
- **Capabilities**: 2 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(public_key)`
  - `verify_signature(message, signature)` - Verify a signature against a message using Ed25519
## chromosome9 (4 positions)
  trophy1 | check2 | warning1
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
### warning IncrementalScanner
- **File**: `v5_code_repair_upgrade.py`
- **Role**: No description
- **Capabilities**: 2 methods | 0 props | 0 bases
- **Methods**:
  - `__init__(git_diff)`
  - `scan_changes()`

---

Summary: 70 classes | trophy36 advanced