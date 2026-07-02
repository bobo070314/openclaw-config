"""批量修复测试文件的 import 路径"""
import os

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
td = os.path.join(V5, 'tests')

fixes = {
    'test_code_analyzer.py': ('chromosomes', 'chromosome0', 'infra'),
    'test_fastmcp_exporter.py': ('chromosomes', 'chromosome1', 'infra'),
    'test_smart_router.py': ('chromosomes', 'chromosome4', 'infra'),
    'test_guardian_policy.py': ('chromosomes', 'chromosome5', 'infra'),
    'test_incremental_scanner.py': ('chromosomes', 'chromosome9', 'infra'),
    'test_logger_context.py': ('chromosomes', 'chromosome12', 'infra'),
    'test_mcp_client.py': ('chromosomes', 'chromosome1', 'infra'),
    'test_result_monad.py': ('chromosomes', 'chromosome12', 'infra'),
    'test_agent_commerce.py': ('chromosomes', 'chromosome6', 'infra'),
    'test_commerce_pk.py': ('chromosomes', 'chromosome6', 'infra'),
    'test_safe_runner.py': ('chromosomes', 'chromosome12', 'infra'),
    'test_agent_os_kernel.py': ('chromosomes', 'chromosome7', 'infra'),
}

for fname, (c1, c2, c3) in fixes.items():
    path = os.path.join(td, fname)
    src = open(path, 'r', encoding='utf-8').read()
    
    # 替换已有的sys.path.insert行成正确的路径
    old_line = f'sys.path.insert(0, os.path.join(V5, "{c1}", "{c2}", "{c3}"))'
    new_line = f'sys.path.insert(0, os.path.join(V5, "{c1}", "{c2}", "{c3}"))'
    
    # 检查当前是否写对了
    if old_line not in src:
        # 找到当前的行并替换
        lines = src.split('\n')
        fixed = []
        for line in lines:
            if 'sys.path.insert' in line and ('chromosomes' in line or 'infra' in line):
                # 替换成正确的
                parts = line.replace('"', '').split(', ')
                new = f'sys.path.insert(0, os.path.join(V5, "{c1}", "{c2}", "{c3}"))'
                fixed.append(new)
                print(f'{fname}: fixed path -> {c1}/{c2}/{c3}')
            else:
                fixed.append(line)
        src = '\n'.join(fixed)
        open(path, 'w', encoding='utf-8').write(src)

print("Done")
