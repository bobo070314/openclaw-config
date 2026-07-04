"""IGP SDK 批量封装脚本 — 一次性生成7个SDK的标准包装"""
import os, shutil, sys

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
V6 = os.path.join(V5, 'v6')
SDK_DIR = os.path.join(V6, 'sdk')

# === SDK定义 ===
SDKS = {
    "doctor": {
        "name": "BugDoctor SDK",
        "desc": "10种bug pattern检测：死锁/竞态/内存泄露/N+1/注入等",
        "source_file": os.path.join(V5, 'chromosomes', 'chromosome9', 'infra', 'v5_bug_doctor.py'),
        "classes": ["BugDoctor"],
        "example": """from igp_sdk.doctor import BugDoctor
d = BugDoctor()
d.scan_directory(".")
report = d.get_report()
print(f"Found {len(report)} issues")""",
    },
    "analyzer": {
        "name": "CodeAnalyzer SDK",
        "desc": "代码质量分析：死代码检测/重构机会/不良模式/杂交机会",
        "source_file": os.path.join(V5, 'chromosomes', 'chromosome0', 'infra', 'v5_code_analyzer.py'),
        "classes": ["CodeAnalyzer"],
        "example": """from igp_sdk.analyzer import CodeAnalyzer
ca = CodeAnalyzer(".")
ca.scan_refactoring()
ca.scan_bad_patterns()
ca.scan_mutation_opportunity()
print(ca.report())""",
    },
    "complexity": {
        "name": "ComplexityAnalyzer SDK",
        "desc": "圈复杂度/认知复杂度度量，支持单个文件和目录批量分析",
        "source_file": os.path.join(V5, 'chromosomes', 'chromosome11', 'infra', 'v5_complexity_analyzer.py'),
        "classes": ["ComplexityAnalyzer"],
        "example": """from igp_sdk.complexity import ComplexityAnalyzer
ca = ComplexityAnalyzer()
result = ca.analyze_file("module.py")
print(f"Score: {result.get('score')}")""",
    },
    "symbolic": {
        "name": "SymbolicEngine SDK",
        "desc": "约束求解引擎（吸收Z3思路，纯Python）",
        "source_file": os.path.join(V5, 'chromosomes', 'chromosome10', 'infra', 'v5_symbolic_engine.py'),
        "classes": ["SymbolicEngine"],
        "example": """from igp_sdk.symbolic import SymbolicEngine
se = SymbolicEngine()
se.add_constraint("x > 5")
se.add_constraint("x < 10")
result = se.solve()
print(f"Solution: {result}")""",
    },
    "lifecycle": {
        "name": "Lifecycle SDK",
        "desc": "产品生命周期管理：Research→Alpha→Beta→GA→Deprecated→EOL",
        "source_file": os.path.join(V6, 'v6_lifecycle.py'),
        "classes": ["LifecycleManager"],
        "example": """from igp_sdk.lifecycle import LifecycleManager
lm = LifecycleManager("product_registry.json")
s = lm.summary()
print(f"Total products: {s['total']}")""",
    },
    "review": {
        "name": "ReviewAgents SDK",
        "desc": "三Agent评审：架构Agent + 安全Agent + 兼容Agent",
        "source_file": os.path.join(V6, 'review', 'v6_review_agents.py'),
        "classes": ["review_file", "ArchitectureAgent", "SecurityAgent", "CompatibilityAgent"],
        "example": """from igp_sdk.review import review_file
result = review_file("module.py")
print(f"Score: {result['total_score']}/30 {'PASS' if result['passed'] else 'FAIL'}")""",
    },
    "prd": {
        "name": "PRDQueue SDK",
        "desc": "跨部门PRD需求管理：提交/评审/自动搜索关键词",
        "source_file": os.path.join(V6, 'prd', 'prd_queue.py'),
        "classes": ["PRDQueue"],
        "example": """from igp_sdk.prd import PRDQueue
q = PRDQueue(".")
prd = q.submit(department="market", product="BugDoctor",
               title="需要TypeScript支持", priority="high")
print(f"PRD: {prd['id']}")""",
    },
}

def make_sdk(key, meta):
    target = os.path.join(SDK_DIR, key)
    source_dir = os.path.join(target, 'source')
    examples_dir = os.path.join(target, 'examples')
    
    # 清理旧目录
    if os.path.exists(target):
        shutil.rmtree(target)
    
    os.makedirs(source_dir)
    os.makedirs(examples_dir)
    
    # 复制源文件
    src_name = os.path.basename(meta['source_file'])
    dst = os.path.join(source_dir, src_name)
    shutil.copy2(meta['source_file'], dst)
    
    # version.py
    with open(os.path.join(target, 'version.py'), 'w', encoding='utf-8') as f:
        f.write(f'VERSION = "1.0.0"\n')
        f.write(f'NAME = "{meta["name"]}"\n')
        f.write(f'DESCRIPTION = "{meta["desc"]}"\n')
    
    # __init__.py
    classes_str = ', '.join(meta['classes'])
    mod_name = src_name.replace('.py', '')
    with open(os.path.join(target, '__init__.py'), 'w', encoding='utf-8') as f:
        f.write(f'"""{meta["name"]} v1.0.0 — {meta["desc"]}"""\n')
        f.write(f'from .source.{mod_name} import {classes_str}\n')
        f.write(f'from .version import VERSION, NAME\n')
        f.write(f'\n__all__ = [{", ".join(repr(c) for c in meta["classes"])}]\n')
    
    # README.md
    with open(os.path.join(target, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(f'# {meta["name"]} v1.0.0\n\n')
        f.write(f'{meta["desc"]}\n\n')
        f.write(f'## 快速开始\n\n```python\n{meta["example"]}\n```\n\n')
        f.write(f'## 类列表\n\n')
        for c in meta['classes']:
            f.write(f'- `{c}`\n')
        f.write(f'\n## 版本\n`v1.0.0`\n')
    
    # examples/basic.py
    with open(os.path.join(examples_dir, 'basic.py'), 'w', encoding='utf-8') as f:
        f.write(f'"""{meta["name"]} 使用示例"""\n')
        f.write(f'import sys, os\n')
        f.write(f'sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n\n')
        f.write(f'{meta["example"]}\n')
    
    return target


print(f"生成 {len(SDKS)} 个SDK...")
for key, meta in SDKS.items():
    path = make_sdk(key, meta)
    print(f"  ✅ {key:15} → {path}")

print(f"\n所有SDK已生成在: {SDK_DIR}")
print("SDK结构:")
for root, dirs, files in os.walk(SDK_DIR):
    level = root.replace(SDK_DIR, '').count(os.sep)
    prefix = '  ' * level + '📁' if level == 0 else '  ' * level + '├─' if level > 0 else ''
    if level > 0:
        base = os.path.basename(root)
        if base != '__pycache__':
            print(f'{prefix} {base}/')
    for f in files:
        if f.endswith('.py') or f.endswith('.md'):
            print(f'  {"  " * (level+1)}├─ {f}')
