"""IGP 硅胶体记忆 v2 vs Mem0 48Kstar — 严丝合缝两列对比表
输出为纯文本表格，一条功能一行，左右对比"""
import sys

print('=' * 100)
print('  硅胶体记忆 v2  vs  Mem0 (48Kstar)')
print('=' * 100)
print()

# (功能, IGP硅胶体, Mem0, 胜负) 胜负: G=我们赢 M=他们赢 D=平
ROWS = [
    ('', '', ''),
    
    ('=== 1. 检索系统 ===', '', ''),
    ('BM25关键词', 'B 从BM25S吸收, 纯dict实现', 'B numpy/scipy加速'),
    ('TF-IDF余弦相似度', 'B Counter+math.log纯dict', 'B sklearn TfidfVectorizer'),
    ('倒排索引', 'B {word: [(idx,freq)]} 自研', 'B 靠Qdrant向量库, 无倒排'),
    ('子词/前缀匹配', 'B wallet匹配ap2_wallet', 'X 靠语义隐式覆盖'),
    ('同义词扩展', 'R 子会话在做300组映射', 'B 向量嵌入天然理解'),
    ('语义向量嵌入', 'X 无向量库, 只用hash近似', 'B Qdrant+LLM embedding 768维'),
    ('实体/知识图谱', 'B 规则提取驼峰/下划线/括号', 'B NLP实体提取+Neo4j图谱'),
    ('时间衰减排序', 'B 1/(1+0.2*h) 公式', 'B 训练的时间衰减模型'),
    ('三级记忆迁移', 'B hot(3x)/warm(1x)/cold(0.5x)', 'B LLM自主判断重要性'),
    ('冲突检测/去重', 'B 编辑距离>0.75自动合并', 'B LLM判断重复再合并'),
    ('技能融合', 'B 同名技能instruction自动合并', 'X 无此概念'),
    ('', '', ''),
    
    ('=== 2. 记忆层级 ===', '', ''),
    ('Episodic(情节)', 'B 事件列表+倒排索引+BM25', 'B Qdrant向量+时间戳', 'D'),
    ('Semantic(语义/实体)', 'B 自动提取+关系关联', 'B NLP实体+Neo4j完整图谱', 'M'),
    ('Procedural(程序/技能)', 'B 技能匹配+频率衰减+熟练度', 'B LLM提取工作流步骤', 'D'),
    ('Entity(实体层)', 'X 缺独立Entity层', 'B 独立Entity层, 链接所有记忆', 'M'),
    ('', '', ''),
    
    ('=== 3. 存储/持久化 ===', '', ''),
    ('数据库', 'B JSON文件 {轻量, 零部署}', 'B PostgreSQL {ACID, 重运维}', 'D'),
    ('向量数据库', 'X 无, 纯内存操作', 'B Qdrant {独立部署, 高精度}', 'M'),
    ('文件锁', 'B O_CREAT|O_EXCL raft风格', 'B PostgreSQL事务锁', 'D'),
    ('数据容量上限', 'M ~2000条JSON上限', 'B 百万级可扩展', 'M'),
    ('数据备份', 'X 手动拷贝JSON', 'B PostgreSQL定期备份', 'M'),
    ('', '', ''),
    
    ('=== 4. API/集成 ===', '', ''),
    ('HTTP API', 'B 22条RESTful路由 @8080', 'B MCP Server + FastAPI', 'D'),
    ('Python SDK', 'B igp_api_client.py', 'B mem0 pip包+SDK', 'D'),
    ('MCP标准协议', 'X 自研REST, 非MCP', 'B 完整MCP Server支持', 'M'),
    ('跨部门通知', 'B POST /api/v1/notify', 'X 无此概念', 'G'),
    ('CLI', 'B igp.py 15个子命令', 'B mem0 CLI', 'D'),
    ('CI/CD集成', 'B pipeline部署自动记录', 'X 无此概念', 'G'),
    ('', '', ''),
    
    ('=== 5. 部署/运维 ===', '', ''),
    ('pip依赖数', '0 纯Python stdlib', '8+ pip install mem0[all]', 'G'),
    ('部署步骤', '1 import即可', '8 pip+PostgreSQL+Qdrant+config', 'G'),
    ('安装体积', '~22KB 3个Python文件', '~200MB pip包+Qdrant镜像', 'G'),
    ('树莓派/NAS', 'B import直接跑', 'X Qdrant+PostgreSQL在ARM上维护', 'G'),
    ('Docker镜像', 'X 无', 'B 官方docker-compose.yml', 'M'),
    ('生产级运维', 'X 手动start/stop', 'B Docker+监控+备份', 'M'),
    ('', '', ''),
    
    ('=== 6. 运行成本 ===', '', ''),
    ('存记忆token', '0 不调LLM', '~6.8K token/条 (LLM提取)', 'G'),
    ('查记忆token', '0 纯检索', '~1.2K token/次 (LLM摘要)', 'G'),
    ('服务器内存', '<50MB', '>2GB (PostgreSQL+Qdrant)', 'G'),
    ('LLM调用来检索', '不需要', '每次需LLM打分', 'G'),
    ('', '', ''),
    
    ('=== 7. 检索质量 ===', '', ''),
    ('LoCoMo分数', '68.1/100', '91.6/100', 'M'),
    ('召回率@10', '60.0%', '未公开 (>85%估计)', 'M'),
    ('精确率@5', '63.3%', '未公开', 'D'),
    ('MRR (首位相关)', '80.0%', '未公开', 'D'),
    ('Benchmark规模', '32条x10查询', 'LoCoMo 300+场景', 'M'),
    ('', '', ''),
    
    ('=== 8. 商业化 ===', '', ''),
    ('许可证', 'MIT (IGP内部)', 'Apache 2.0', 'D'),
    ('免费层', '100%免费, 永远免费', '社区版免费, 企业版付费', 'G'),
    ('托管服务', '自托管 (本地)', 'Mem0 Cloud (付费SaaS)', 'M'),
    ('', '', ''),
    
    ('=== 9. 我们独有的(他们没有) ===', '', ''),
    ('', '1. 跨部门通知系统', 'X', 'G'),
    ('', '2. CI/CD pipeline自动记录', 'X', 'G'),
    ('', '3. 19个染色体部门注册表', 'X', 'G'),
    ('', '4. 子词+前缀匹配 (wallet->ap2_wallet)', 'X', 'G'),
    ('', '5. 记忆+文件锁 raft风格', 'X', 'G'),
    ('', '6. 零依赖零token全程', 'X', 'G'),
    ('', '', ''),
]

for feat, igp_val, mem0_val in ROWS:
    if not feat and not igp_val and not mem0_val:
        print()
        continue
    if feat.startswith('==='):
        print(f'  {feat}')
        continue
    if feat.startswith('') and not igp_val and not mem0_val:
        # section spacer
        continue
    
    # 普通行
    winner = ''
    if mem0_val in ('X',):
        winner = 'G'
    if igp_val in ('X',):
        winner = 'M'
    
    igp_val_clean = igp_val
    mem0_val_clean = mem0_val
    
    # 左右列
    left = f'[{winner}] {feat}'
    
    print(f'  {feat:<32s} | 我们: {igp_val:<35s} | 他们: {mem0_val}')
    
    if feat.startswith('') and igp_val.startswith('') and '独有的' in feat:
        pass

print()
print('=' * 100)
print('  统计')
print('=' * 100)

# 统计胜负
wins = {'G': 0, 'M': 0, 'D': 0}
for feat, igp_val, mem0_val in ROWS:
    if feat.startswith('===') or (not feat and not igp_val and not mem0_val):
        continue
    if not feat:
        continue
    if igp_val.startswith('X') and mem0_val.startswith('B'):
        wins['M'] += 1
    elif igp_val.startswith('B') and mem0_val.startswith('X'):
        wins['G'] += 1
    elif igp_val.startswith('R'):
        wins['M'] += 1
    else:
        # 检查胜负列
        pass

# 简单版本: 用胜负列
for feat, igp_val, mem0_val in ROWS:
    if not feat:
        continue
    if feat.startswith('==='):
        continue

print()
print(f'  我们赢 (G): 在部署, 依赖, 成本, 跨部门, 子词匹配 等领域')
print(f'  他们赢 (M): 在语义搜索, 向量库, 持久化, 大数据量, 检索质量')
print(f'  平手 (D): BM25, 时间衰减, 3层架构, API接口')
print()
print(f'  当前分: 68.1/100')
print(f'  目标: 91.7+/100 (+同义词 +hash嵌入 子会话正在跑)')
print('=' * 100)
