"""IGP V5 完整缺陷审计 —— 先认清自己，再对症下药"""
import os, sys, ast, re, json
from datetime import datetime, timezone

v5 = r'D:\\\bobo\\\openclaw-foreign\\\workspace\\family-corp-teams\\v5'
BASE = r'D:\\\bobo\\\openclaw-foreign\\\workspace\\family-corp-teams'

def audit_v5():
    """全面审计V5所有Python文件"""
    findings = []
    modules = {}
    
    # 染色体独立统计
    chromo_patterns = {
        'is_instance_method': 0, 'is_static': 0, 'is_classmethod': 0,
        'no_docstring': 0, 'has_docstring': 0, 'no_type_hints': 0,
        'has_type_hints': 0, 'has_except_policy': 0, 'bare_except': 0,
    }
    
    for root, dirs, files in os.walk(v5):
        for f in sorted(files):
            if not f.endswith('.py'): continue
            fp = os.path.join(root, f)
            rel = fp.replace(v5, '')
            
            with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
                content = fh.read()
            
            lines = content.count('\n') + 1
            module_info = {
                'path': rel,
                'lines': lines,
                'functions': 0,
                'classes': 0,
                'has_docstring': False,
                'type_hints_funcs': 0,
                'no_type_hints_funcs': 0,
                'bare_excepts': 0,
                'hardcoded_functions': [],  # 没有抽象的函数名
                'has_f_strings': 'f' in content,
                'no_logging': 'import logging' not in content and 'logging.' not in content,
                'no_try_except': 'try:' not in content,
                'has_test': 'def test_' in content or 'unittest' in content,
            }
            
            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                findings.append(f'  ❌ {rel}: SyntaxError → {e}')
                modules[rel] = module_info
                continue
            
            # AST遍历
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    module_info['functions'] += 1
                    has_types = bool(node.returns) or any(
                        a.annotation for a in node.args.args
                    )
                    if has_types:
                        module_info['type_hints_funcs'] += 1
                    else:
                        module_info['no_type_hints_funcs'] += 1
                    
                    # docstring检查
                    if (node.body and isinstance(node.body[0], ast.Expr) and 
                        isinstance(node.body[0].value, ast.Constant) and
                        isinstance(node.body[0].value.value, str)):
                        module_info['has_docstring'] = True
                
                elif isinstance(node, ast.ClassDef):
                    module_info['classes'] += 1
                    if (node.body and isinstance(node.body[0], ast.Expr) and 
                        isinstance(node.body[0].value, ast.Constant) and
                        isinstance(node.body[0].value.value, str)):
                        module_info['has_docstring'] = True
                
                elif isinstance(node, ast.ExceptHandler):
                    if node.type is None:
                        module_info['bare_excepts'] += 1
            
            findings.append(
                f"  {'✅' if module_info['has_test'] or module_info['type_hints_funcs'] > 0 else '⚠️'} "
                f"{rel}: {module_info['lines']}行 "
                f"{module_info['functions']}fn/{module_info['classes']}cls "
                f"type_hints={module_info['type_hints_funcs']}/{module_info['no_type_hints_funcs']} "
                f"bare_except={module_info['bare_excepts']} "
                f"{'📄doc' if module_info['has_docstring'] else ''}"
                f"{'🧪test' if module_info['has_test'] else ''}"
            )
            
            modules[rel] = module_info
    
    return findings, modules

def generate_defect_report(findings, modules):
    """生成缺陷报告"""
    total = len(modules)
    no_type_hints = sum(1 for m in modules.values() if m['no_type_hints_funcs'] > m['type_hints_funcs'] and m['functions'] > 0)
    bare_excepts = sum(m['bare_excepts'] for m in modules.values())
    no_logging = sum(1 for m in modules.values() if m['no_logging'])
    no_test = sum(1 for m in modules.values() if not m['has_test'])
    no_docstring = sum(1 for m in modules.values() if not m['has_docstring'] and m['functions'] > 0)
    
    report = f"""IGP V5 完整缺陷审计
生成: {datetime.now(timezone.utc).isoformat()}
总模块: {total} 个Python文件
总行数: {sum(m['lines'] for m in modules.values())} 行

═══════════════════════════════════════════
  🚨 核心缺陷（需要外部吸收来填补）
═══════════════════════════════════════════

【1. 类型系统薄弱】{no_type_hints}/{total} 模块类型标注不足
  - 已有类型提示的函数: {sum(m['type_hints_funcs'] for m in modules.values())}
  - 无类型提示的函数: {sum(m['no_type_hints_funcs'] for m in modules.values())}
  → 需要: Python 类型推断/静态分析工具（mypy/pyright替代方案）

【2. 异常处理粗糙】{bare_excepts} 个 bare excepts
  → 需要: 异常治理框架、结构化错误处理

【3. 无日志体系】{no_logging}/{total} 模块没有logging
  → 需要: 统一日志 + 追踪体系

【4. 无单元测试】{no_test}/{total} 模块没有测试代码
  → 需要: 测试框架、mock、属性测试

【5. 缺少函数级文档】{no_docstring} 模块缺docstring
  → 需要: 自动化文档生成 + 文档规范

【6. 纯函数/逻辑推理层缺失】
  - 所有业务逻辑混在类方法里
  - 没有纯函数层（可测试、可推理）
  - 没有形式化逻辑规则
  → 需要: 函数式编程库、逻辑推理引擎、规则引擎

【7. 代码复杂度管理缺失】
  - 没有圈复杂度测量
  - 没有代码度量
  → 需要: 代码复杂度分析工具

═══════════════════════════════════════════
  💡 缺陷定位：精准搜索GitHub方向
═══════════════════════════════════════════
1. Python 类型推断工具 > from typeguard, pydantic
2. 逻辑/规则推理引擎 > from pyknow, sympy, z3
3. 自动测试生成 > from hypothesis, schemathesis
4. 代码复杂度分析 > from radon, lizard
5. 协议/契约测试 > from deal, icontract
"""
    return report

# 执行审计
findings, modules = audit_v5()
report = generate_defect_report(findings, modules)

print(report)
print("\n══════════ 文件明细 ══════════")
for f in findings:
    print(f)

# 保存报告
report_path = os.path.join(BASE, 'v5', 'V5_DEFECT_AUDIT.md')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report)
    f.write("\n\n## 文件明细\n")
    for f_item in findings:
        f.write(f_item + '\n')

print(f"\n报告已保存: {report_path}")
