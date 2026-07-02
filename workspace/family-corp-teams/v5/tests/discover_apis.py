"""发现每个模块的真正API（跳过无法parse的）"""
import sys, os, ast

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'

targets = [
    ('test_code_analyzer', 'chromosomes', 'chromosome0', 'infra', 'v5_code_analyzer'),
    ('test_fastmcp_exporter', 'chromosomes', 'chromosome1', 'infra', 'fastmcp_export'),
    ('test_smart_router', 'chromosomes', 'chromosome4', 'infra', 'v5_smart_router'),
    ('test_guardian_policy', 'chromosomes', 'chromosome5', 'infra', 'guardian_policy'),
    ('test_incremental_scanner', 'chromosomes', 'chromosome9', 'infra', 'v5_incremental_scanner'),
    ('test_logger_context', 'chromosomes', 'chromosome12', 'infra', 'v5_logger_context'),
    ('test_mcp_client', 'chromosomes', 'chromosome1', 'infra', 'igp_mcp_v5_client'),
    ('test_result_monad', 'chromosomes', 'chromosome12', 'infra', 'v5_result_monad'),
    ('test_agent_commerce', 'chromosomes', 'chromosome6', 'infra', 'agent_commerce_v2'),
    ('test_commerce_pk', 'chromosomes', 'chromosome6', 'infra', 'commerce_pk_v2'),
]

for tname, c1, c2, c3, modname in targets:
    path = os.path.join(V5, c1, c2, c3, f'{modname}.py')
    src = open(path, 'r', encoding='utf-8').read()
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        print(f"=== {tname} ({modname}) PARSE FAILED: {e} ===")
        continue
    
    classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    top_level = [n for n in ast.iter_child_nodes(tree) if isinstance(n, ast.ClassDef)]
    
    print(f"=== {tname} ({modname}) ===")
    print(f"  Classes: {[c.name for c in classes]}")
    
    for cls in top_level:
        methods = [n.name for n in ast.iter_child_nodes(cls) if isinstance(n, ast.FunctionDef)]
        print(f"  {cls.name}: {methods}")
        for m in ast.iter_child_nodes(cls):
            if isinstance(m, ast.FunctionDef) and m.name == '__init__':
                args = [a.arg for a in m.args.args if a.arg != 'self']
                print(f"    __init__({', '.join(args)})")
    
    print()
