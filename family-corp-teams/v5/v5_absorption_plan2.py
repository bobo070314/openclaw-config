"""
IGP 第2波外部吸收作战方案
基于V5完整缺陷审计 + GitHub搜索 + 现有仓库扫描
"""

import os, sys, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
V5_CHROMO = os.path.join(BASE, 'v5', 'chromosomes')
GH = r'D:\\\bobo\\\openclaw-foreign\\\workspace\\gh-enterprise-baseline'

def scan_source(name):
    fp = os.path.join(GH, name)
    if not os.path.isdir(fp):
        return []
    py_files = []
    for root, dirs, files in os.walk(fp):
        if '.git' in dirs:
            dirs.remove('.git')
        for f in files:
            if f.endswith('.py'):
                rel = os.path.relpath(os.path.join(root, f), fp)
                sz = os.path.getsize(os.path.join(root, f))
                py_files.append((rel, sz))
    return py_files

# 扫描所有可吸收源
sources = {}
for name in ['z3', 'deal', 'ultimate_bug_scanner', 'claude_code_agent_farm']:
    py = scan_source(name)
    if py:
        total_lines = sum(s for _, s in py)
        sources[name] = {
            'files': len(py),
            'total_bytes': total_lines,
            'top_files': sorted(py, key=lambda x: -x[1])[:6]
        }

print("\n" + "="*60)
print("  🏛️  IGP 第2波吸收：诊断→决策→执行")
print("="*60)

# 7个缺陷 + 3条新染色体方案
print("""
╔══════════════════════════════════════════════════════╗
║  🚨 V5 缺陷审计结果 (62文件, 5852行)                ║
╠══════════════════════════════════════════════════════╣
║ 缺陷1: 类型系统薄弱    22/62模块缺类型标注          ║
║        (116个函数无type hint, 173个有)              ║
║ 缺陷2: 异常处理粗糙    4个bare except               ║
║ 缺陷3: 无日志体系      56/62模块没有logging         ║
║ 缺陷4: 无单元测试      61/62模块没测试代码          ║
║ 缺陷5: 缺少函数文档    23模块缺docstring            ║
║ 缺陷6: 纯函数/推理层缺 业务逻辑全混在方法里         ║
║ 缺陷7: 无代码复杂度    没有圈复杂度测量             ║
╚══════════════════════════════════════════════════════╝
""")

# 三条新染色体方案
new_chromosomes = [
    ("染色体10: 逻辑推理部 🧠", "补缺陷6", [
        "Z3 SMT求解器(25K⭐) → 符号执行+自动推理",
        "SymPy → 数学推理层",
        "deal → 契约式编程(前置/后置/不变量)",
        "吸收核心: SMT求解、符号推理、逻辑契约"
    ]),
    ("染色体11: 类型/度量部 📏", "补缺陷1+7", [
        "radon → 圈复杂度+代码度量 (纯Python)",
        "typeguard → 运行时类型检查",
        "吸收核心: 自动类型推断、复杂度分级、质量门禁"
    ]),
    ("染色体12: 自动测试部 🧪", "补缺陷2+3+4", [
        "Hypothesis → 属性测试(自动生成测试)",
        "icontract/hypothesis-hypothesis → 契约生成测试",
        "logging模块 → 统一日志+追踪(标准库内置)",
        "吸收核心: 自动化测试生成、日志注入、错误治理"
    ]),
]

for name, target, items in new_chromosomes:
    print(f"  {name} ({target})")
    for i in items:
        print(f"    · {i}")
    print()

# 消化深度
for name, info in sources.items():
    print(f"  📦 {name}: {info['files']}个Python文件, {info['total_bytes']:,}B")
    for f, s in info['top_files'][:3]:
        print(f"    · {f} ({s}B)")

# V5现存问题快速修复
print("""
╔══════════════════════════════════════════════════════╗
║  ⚡ 执行方案：V5现存BUG先修再吸收                   ║
╠══════════════════════════════════════════════════════╣
║  立刻修：                                              ║
║  1. fastmcp_export.py: SyntaxError (缩进)            ║
║  2. v5_injector.py: SyntaxError (字符串引号)          ║
║                                                       ║
║  吸收架子：                                           ║
║  3. 染色体10-12 空壳创建 (含吸收报告)                ║
║  4. 用deal→添加契约式编程到V5核心函数               ║
║  5. 用radon→写纯Python复杂度扫描器(0依赖)           ║
╚══════════════════════════════════════════════════════╝
""")
