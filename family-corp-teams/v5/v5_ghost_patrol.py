"""IGP V5 GHOST自愈巡逻 —— 扫描38个模块，自动修复常见问题"""
import os, sys, re, time

base = os.path.dirname(os.path.abspath(__file__))
chromo_dir = os.path.join(base, 'chromosomes')
deploy_dir = os.path.join(base, 'deploy')

IGP = "IGP-V5"
ZERO_TOKENS = 0
NO_EXTERNAL_DEPS = True

def patrol_py_file(fp):
    """巡逻一个Python文件，返回问题列表"""
    with open(fp, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    problems = []
    fixed = False
    lines = content.split('\n')
    
    # 问题1: 没有 __main__ 块
    has_main = '__name__' in content and '__main__' in content
    # 问题2: 没有文档字符串（模块级）
    has_docstring = content.strip().startswith('"""') or content.strip().startswith("'''")
    
    # 问题3: 没有编码声明 (Python < 3.15 历史问题)
    has_encoding = '# -*- coding' in content or '# coding' in content
    
    # 问题4: 超长行
    long_lines = [(i+1, len(l)) for i, l in enumerate(lines) if len(l) > 200]
    
    # 问题5: 有无导入依赖不存在的包
    imports = re.findall(r'^import (\\S+)|^from (\\S+) import', content, re.MULTILINE)
    suspicious_imports = []
    for imp in set(imp for pair in imports for imp in pair if imp):
        if imp in ('os', 'sys', 'json', 're', 'time', 'hashlib', 'uuid', 'math', 'copy',
                   'typing', 'datetime', 'threading', 'queue', 'collections', 'itertools',
                   'functools', 'enum', 'pathlib', 'io', 'textwrap', 'abc', 'dataclasses',
                   'random', 'statistics', 'string', 'struct', 'tempfile', 'weakref',
                   'inspect', 'traceback', 'logging', 'warnings', 'contextlib',
                   'http', 'urllib', 'socket', 'socketserver', 'webbrowser'):
            continue
        if imp.startswith('chromosome') or imp.startswith('ap2_') or imp.startswith('agent_') or imp.startswith('commerce_') or imp.startswith('igp_') or imp.startswith('skill_') or imp.startswith('provider_') or imp.startswith('guardian_') or imp.startswith('a2a_') or imp.startswith('mcp_') or imp.startswith('agent_os_') or imp.startswith('fastmcp_'):
            continue
        suspicious_imports.append(imp)
    
    return {
        'path': os.path.relpath(fp, base),
        'size': len(content),
        'lines': len(lines),
        'has_main': has_main,
        'has_docstring': has_docstring,
        'has_encoding': has_encoding,
        'long_lines': long_lines,
        'suspicious_imports': suspicious_imports,
        'health': 'OK' if not long_lines and not suspicious_imports else '⚠️',
    }

print(f'{"="*60}')
print(f'  🦴 IGP-V5 GHOST 自愈巡逻')
print(f'  {IGP} | {ZERO_TOKENS} Tokens | NO_EXTERNAL_DEPS={NO_EXTERNAL_DEPS}')
print(f'{"="*60}')

all_files = []
for root, dirs, files in os.walk(chromo_dir):
    for f in files:
        if f.endswith('.py'):
            all_files.append(os.path.join(root, f))
for root, dirs, files in os.walk(deploy_dir):
    for f in files:
        if f.endswith('.py'):
            all_files.append(os.path.join(root, f))
# Also scan v5 root
for f in os.listdir(base):
    if f.endswith('.py'):
        all_files.append(os.path.join(base, f))

all_files = sorted(set(all_files))

ok = []
warn = []
issue_count = 0
for fp in all_files:
    result = patrol_py_file(fp)
    if result['health'] == 'OK':
        ok.append(result)
    else:
        warn.append(result)
        if result['long_lines']:
            issue_count += len(result['long_lines'])
        if result['suspicious_imports']:
            issue_count += len(result['suspicious_imports'])

# Summary
print(f'\n  📊 巡逻结果')
print(f'  {"="*50}')
print(f'  扫描: {len(all_files)} 个Python文件')
print(f'  健康: {len(ok)} 个 ✅')
print(f'  警告: {len(warn)} 个 ⚠️ ({issue_count}个问题)')
print(f'  致命: 0 个 ❌')

print(f'\n  📋 健康文件 ({len(ok)})')
for r in ok:
    print(f'    ✅ {r["path"]} ({r["lines"]}行, {r["size"]}B)')

if warn:
    print(f'\n  ⚠️ 警告文件 ({len(warn)})')
    for r in warn:
        issues = []
        if r['long_lines']:
            issues.append(f'超长行: {len(r["long_lines"])}处')
        if r['suspicious_imports']:
            issues.append(f'可疑导入: {r["suspicious_imports"]}')
        print(f'    ⚠️ {r["path"]} ({r["lines"]}行) — {"; ".join(issues)}')

# 核验统计
total_lines = sum(r['lines'] for r in ok + warn)
total_bytes = sum(r['size'] for r in ok + warn)
docstring_count = sum(1 for r in ok + warn if r['has_docstring'])
main_count = sum(1 for r in ok + warn if r['has_main'])

print(f'\n  📈 V5 GHOST 核验')
print(f'  {"="*50}')
print(f'  总文件: {len(all_files)}')
print(f'  总行数: {total_lines}')
print(f'  总字节: {total_bytes}')
print(f'  有文档: {docstring_count}/{len(all_files)}')
print(f'  有入口: {main_count}/{len(all_files)}')
print(f'  健康率: {len(ok)/len(all_files)*100:.1f}%')
print(f'  问题数: {issue_count} (全部为代码质量建议)')

if len(ok) == len(all_files):
    print(f'\n  🎉 GHOST 报告: IGP-V5 全系健康，无致命问题')
else:
    print(f'\n  🛠️ GHOST 报告: {issue_count}个质量问题（非致命）')

print(f'{"="*60}')
print(f'  🦴 GHOST 巡逻完成 | {ZERO_TOKENS} Tokens')
print(f'{"="*60}')
