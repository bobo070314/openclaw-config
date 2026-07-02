"""真实覆盖率报告"""
import subprocess, sys, os, tempfile

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
TD = os.path.join(V5, 'tests')
SRC = os.path.join(V5, 'chromosomes')

# 找所有 .py 源文件（排除__pycache__和run.py）
src_files = []
for root, dirs, files in os.walk(SRC):
    dirs[:] = [d for d in dirs if d != '__pycache__']
    for f in files:
        if f.endswith('.py') and f != '__pycache__' and f != 'run.py':
            src_files.append(os.path.join(root, f))

# 找所有测试文件
test_files = [os.path.join(TD, f) for f in os.listdir(TD) if f.startswith('test_') and f.endswith('.py')]

# 统计各源文件对应测试覆盖
total_src_lines = 0
total_src_files = len(src_files)
covered_src_classes = set()

# 收集所有源文件的类定义
import ast
src_class_map = {}  # file -> set(classes)
for sf in src_files:
    try:
        with open(sf, 'r', encoding='utf-8') as f:
            raw = f.read()
            tree = ast.parse(raw)
        classes = set()
        lines = raw.split('\n')
        code_lines = sum(1 for l in lines if l.strip() and not l.strip().startswith('#') and not l.strip().startswith('"""') and not l.strip().startswith("'''"))
        for n in ast.walk(tree):
            if isinstance(n, ast.ClassDef):
                classes.add(n.name)
        src_class_map[sf] = (classes, code_lines)
        total_src_lines += code_lines
    except:
        src_class_map[sf] = (set(), 0)

# 统计测试覆盖了哪些类
test_covered_classes = set()
for tf in test_files:
    try:
        with open(tf, 'r', encoding='utf-8') as f:
            content = f.read()
        # 找所有 import 的类名
        for line in content.split('\n'):
            if 'from' in line and 'import' in line:
                parts = line.split('import')
                if len(parts) > 1:
                    for name in parts[1].split(','):
                        name = name.strip().strip('()')
                        for n in name.split(' as '):
                            n = n.strip()
                            if n and n[0].isupper():
                                test_covered_classes.add(n)
    except:
        pass

# 统计有多少类被覆盖
all_classes = set()
class_file_map = {}  # class -> file
for sf, (classes, _) in src_class_map.items():
    for c in classes:
        all_classes.add(c)
        class_file_map[c] = sf

covered = all_classes & test_covered_classes
uncovered = all_classes - test_covered_classes

print("=" * 60)
print("  IGP V5 覆盖率真实报告")
print("=" * 60)
print()
print(f"  代码源文件: {total_src_files}")
print(f"  有效代码行: {total_src_lines}")
print(f"  总类数:     {len(all_classes)}")
print(f"  测试文件数: {len(test_files)}")
print()
print(f"  🏆 被覆盖的类: {len(covered)}/{len(all_classes)} ({len(covered)*100//len(all_classes) if all_classes else 0}%)")
print()

# 列出uncovered的类
if uncovered:
    print(f"  ⚠️ 未覆盖的类 ({len(uncovered)}个):")
    for c in sorted(uncovered):
        fname = os.path.relpath(class_file_map.get(c, ''), V5)
        print(f"    - {c} ({fname})")

print()
print("=" * 60)
print("  覆盖30%+要求: 现有测试覆盖了", len(covered), "个类")
print("  但要达到代码行50%", "→ 需要对这些未覆盖类写有意义的API测试")
print("=" * 60)
