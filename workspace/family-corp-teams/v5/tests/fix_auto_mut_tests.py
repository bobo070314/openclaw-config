"""重写auto_tester和mutation_fission测试"""
import os

TD = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\tests'

def make_test(modname, clsname, pparts, init_args_str, method1, method1_call):
    backslash = '\\\\'
    path_str = backslash.join(pparts)
    lines = []
    lines.append(f'"""IGP 单元测试: {clsname}"""')
    lines.append('from __future__ import annotations')
    lines.append('import sys, os')
    lines.append('V5 = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\v5"')
    lines.append(f'sys.path.insert(0, os.path.join(V5, "{path_str}"))')
    lines.append(f'from {modname} import {clsname}')
    lines.append('')
    lines.append(f'def test_create():')
    lines.append(f'    obj = {clsname}({init_args_str}); assert obj is not None')
    lines.append('')
    lines.append(f'def test_{method1}():')
    lines.append(f'    obj = {clsname}({init_args_str}); r = obj.{method1_call}')
    lines.append('    assert r is not None')
    lines.append('')
    lines.append('if __name__ == "__main__":')
    lines.append('    _ok = 0; _r = []')
    lines.append(f'    for _n, _f in [("create",test_create),("{method1}",test_{method1})]:')
    lines.append('        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")')
    lines.append('        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")')
    lines.append('    for l in _r: print(l)')
    lines.append(f'    print(f"\\n{clsname}: {{_ok}}/2"); sys.exit(0 if _ok==2 else 1)')
    return '\n'.join(lines)

tests = [
    ('test_v5_auto_tester_v2_autotester.py', 'v5_auto_tester_v2', 'AutoTester',
     ['chromosomes', 'chromosome12', 'infra'], '', 'add_suite', 'add_suite("test")'),
    ('test_v5_auto_tester_v2_testresult.py', 'v5_auto_tester_v2', 'TestResult',
     ['chromosomes', 'chromosome12', 'infra'], '"test", True, {}, 0', 'to_dict', 'to_dict()'),
    ('test_v5_auto_tester_v2_testsuite.py', 'v5_auto_tester_v2', 'TestSuite',
     ['chromosomes', 'chromosome12', 'infra'], '"test"', 'add', 'add("test")'),
    ('test_v5_mutation_fission_autofixscanner.py', 'v5_mutation_fission', 'AutoFixScanner',
     ['chromosomes', 'chromosome0', 'infra'], '', 'scan_and_fix', 'scan_and_fix()'),
    ('test_v5_mutation_fission_fissionengine.py', 'v5_mutation_fission', 'FissionEngine',
     ['chromosomes', 'chromosome0', 'infra'], '', 'fission', 'fission("chromosome1", ["m1"])'),
    ('test_v5_mutation_fission_mutationengine.py', 'v5_mutation_fission', 'MutationEngine',
     ['chromosomes', 'chromosome0', 'infra'], '', 'cross_breed', 'cross_breed("SecureResult", "CryptoKit")'),
]

for fname, modname, clsname, pparts, init_args_str, method1, method1_call in tests:
    content = make_test(modname, clsname, pparts, init_args_str, method1, method1_call)
    path = os.path.join(TD, fname)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Written: {fname}")
