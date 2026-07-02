"""IGP V5 真实类覆盖率 stats"""
import os, re, sys

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
TD = os.path.join(V5, 'tests')
CHRO = os.path.join(V5, 'chromosomes')

# 1. 扫描所有源文件中的类
all_classes = {}  # class_name -> file
class_to_test = {}  # class_name -> [test_files]
test_for_class = {}  # test_file -> {classes_covered}

for root, dirs, files in os.walk(CHRO):
    dirs[:] = [d for d in dirs if d != '__pycache__']
    for f in files:
        if not f.endswith('.py') or f == '__pycache__':
            continue
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8') as fh:
            for line in fh:
                m = re.match(r'^class\s+(\w+)', line)
                if m:
                    all_classes[m.group(1)] = path

# 再加上v6, absorb里的小
for extra in ['v6', 'absorb']:
    extra_dir = os.path.join(V5, extra)
    if os.path.isdir(extra_dir):
        for root, dirs, files in os.walk(extra_dir):
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for f in files:
                if not f.endswith('.py') or f == '__pycache__':
                    continue
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as fh:
                    for line in fh:
                        m = re.match(r'^class\s+(\w+)', line)
                        if m:
                            all_classes[m.group(1)] = path

# 2. 扫描所有测试文件中的 import
covered = set()
for tf in os.listdir(TD):
    if not tf.startswith('test_') or not tf.endswith('.py'):
        continue
    path = os.path.join(TD, tf)
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        content = fh.read()
    for line in content.split('\n'):
        m = re.match(r'^from\s+(\S+)\s+import\s+(.+)', line)
        if m:
            mod = m.group(1)
            names = [n.strip().split(' as ')[0].strip() for n in m.group(2).split(',')]
            for n in names:
                if n in all_classes:
                    covered.add(n)

# 3. 输出
total = len(all_classes)
cov = len(covered)
uncovered_set = set(all_classes.keys()) - covered

percent = round(cov / total * 100) if total > 0 else 0

print("=" * 60)
print(f"  IGP V5 覆盖率报告（类级别）")
print("=" * 60)
print(f"  总类数:              {total}")
print(f"  已覆盖类:            {cov}")
print(f"  覆盖率:              {percent}%")
print(f"  测试文件数:          {len([f for f in os.listdir(TD) if f.startswith('test_') and f.endswith('.py')])}")
print()

if uncovered_set:
    print(f"  ⚠️ 未覆盖的类 ({len(uncovered_set)}):")
    for c in sorted(uncovered_set)[:20]:
        f = all_classes[c]
        rel = os.path.relpath(f, V5)
        print(f"    - {c:<28} ({rel})")
    if len(uncovered_set) > 20:
        print(f"    ... 还有 {len(uncovered_set)-20} 个")

print()
print(f"  📊 覆盖率统计: {cov}/{total} = {percent}%")
