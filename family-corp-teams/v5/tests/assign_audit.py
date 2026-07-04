"""IGP 部门分配审计"""
import os

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'

# IGP金字塔部门
CHROMOSOMES = [
    ('chromosome1', 'MCP协议部'),
    ('chromosome2', 'A2A协议部'),
    ('chromosome3', '市场扩展部'),
    ('chromosome4', 'Provider路由器'),
    ('chromosome5', '治理/政策部'),
    ('chromosome6', '商业部'),
    ('chromosome7', 'Agent OS部'),
    ('chromosome8', 'AP2协议部'),
    ('chromosome9', 'Bug检查部'),
    ('chromosome10', '逻辑推理部'),
    ('chromosome11', '类型/度量部'),
    ('chromosome12', '自动测试部'),
    ('chromosome0', '变异裂变中心'),
    ('chromosome14_smart_routing', '智能路由部'),
    ('chromosome15_audit_security', '审计安全部'),
]

# 非染色体部门
OTHER_DIRS = [
    ('v6/api', 'API服务部'),
    ('v6/cli', 'CLI工具部'),
    ('v6/sdk', 'SDK包管理部'),
    ('v6/prd', 'PRD产品部'),
    ('v6/review', '评审Agent部'),
    ('v6/ci', 'CI/CD部'),
    ('v6/silicon_memory', '硅胶体记忆部'),  # <-- 有吗?
    ('absorb/docagent', '岗位定义部'),
    ('absorb/scouting', '侦察兵部'),
    ('deploy', '部署部'),
]

print("=" * 65)
print("  IGP 工程部 — 部门分配审计")
print("=" * 65)
print()

total_files = 0
unassigned = []

# 扫描整个chromosomes目录
CHRO_BASE = os.path.join(V5, 'chromosomes')
for root, dirs, files in os.walk(CHRO_BASE):
    dirs[:] = [d for d in dirs if d != '__pycache__']
    for f in files:
        if not f.endswith('.py') or f == '__pycache__':
            continue
        total_files += 1
        rel = os.path.relpath(os.path.join(root, f), V5)
        
        # 检查分配
        assigned = False
        ch = os.path.basename(os.path.dirname(os.path.dirname(root))) if 'infra' in root else ''
        for chrom, name in CHROMOSOMES:
            if chrom in rel:
                assigned = True
                break
        if not assigned:
            unassigned.append(rel)

# 扫描v6/和非染色体目录
V6 = os.path.join(V5, 'v6')
for root, dirs, files in os.walk(V6):
    dirs[:] = [d for d in dirs if d != '__pycache__']
    for f in files:
        if not f.endswith('.py') or f == '__pycache__':
            continue
        total_files += 1
        rel = os.path.relpath(os.path.join(root, f), V5)
        assigned = False
        for d, name in OTHER_DIRS:
            if d in rel:
                assigned = True
                break
        if not assigned:
            unassigned.append(rel)

# 扫描其他顶层
for root, dirs, files in os.walk(V5):
    dirs[:] = [d for d in dirs if d != '__pycache__' and d not in ('chromosomes', 'v6', '__pycache__')]
    if root == V5:
        for f in files:
            if not f.endswith('.py') or f == '__pycache__':
                continue
            total_files += 1
            rel = os.path.relpath(os.path.join(root, f), V5)
            unassigned.append(rel)

print(f"  总文件数: {total_files}")
print(f"  已分配:   {total_files - len(unassigned)}")
print(f"  未分配:   {len(unassigned)}")
print()

if unassigned:
    # 按目录分组
    from collections import defaultdict
    groups = defaultdict(list)
    for u in unassigned:
        dirname = os.path.dirname(u)
        groups[dirname].append(os.path.basename(u))
    
    print("  ⚠️ 未分配文件:")
    for dirname in sorted(groups.keys()):
        files = groups[dirname]
        print(f"    📁 {dirname}/ ({len(files)} files)")
        for f in sorted(files):
            print(f"        - {f}")

print()
print("=" * 65)
print()
print("  硅胶体记忆:")
print(f"    v6/silicon_memory/ → 在v6/下，但未注册为核心部门")
print()
print("  建议:")
print("    1. 硅胶体记忆 → 注册为 'chromosome13_silicon_memory'")
print("    2. tests/ → 分配时chromosome编号+部门名")
print("=" * 65)
