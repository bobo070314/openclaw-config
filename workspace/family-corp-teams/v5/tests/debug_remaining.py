"""快速修最后10个失败的测试"""
import subprocess, sys, os

TD = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\tests'

# 1. guardianact: is_allowed missing item param
# 快速看错误
r = subprocess.run([sys.executable, '-W', 'ignore', '-u', os.path.join(TD, 'test_guardian_act_guardianact.py')], capture_output=True, timeout=10, text=True, encoding='utf-8')
print("guardian act error:", r.stdout.split('\n')[-3:])

# auto_tester 三个 import err -- 检查v5_auto_tester_v2.py是否存在
path = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome12\infra\v5_auto_tester_v2.py'
print(f"v5_auto_tester_v2.py exists: {os.path.exists(path)}")
if os.path.exists(path):
    # 检查TestResult, TestSuite, AutoTester
    with open(path, 'r', encoding='utf-8') as f:
        import ast
        tree = ast.parse(f.read())
        for n in ast.walk(tree):
            if isinstance(n, ast.ClassDef):
                print(f"  Found class: {n.name}")

# mutation_fission 三个 import err
path2 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome0\infra\v5_mutation_fission.py'
print(f"\nv5_mutation_fission.py exists: {os.path.exists(path2)}")
if os.path.exists(path2):
    with open(path2, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())
        for n in ast.walk(tree):
            if isinstance(n, ast.ClassDef):
                print(f"  Found class: {n.name}")
