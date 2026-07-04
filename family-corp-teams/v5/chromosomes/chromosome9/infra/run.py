"""染色体9 代码修补部 验证"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v5_bug_doctor import BugDoctor
import tempfile

# 创建测试用有bug文件
test_files = []
for i, (name, code) in enumerate([
    ("buggy_1.py", "def foo(x=[]):\n    x.append(1)\n    return x\n\ntry:\n    pass\nexcept:\n    pass\n"),
    ("buggy_2.py", "password = 'super_secret_123'\nresult = eval('print(123)')\n"),
    ("buggy_3.py", "os.system('rm -rf /')\nimport pickle\ndata = pickle.loads(b'xxx')\n"),
]):
    fp = os.path.join(tempfile.gettempdir(), name)
    with open(fp, 'w') as f:
        f.write(code)
    test_files.append(fp)

# 扫描
doctor = BugDoctor()
for fp in test_files:
    bugs = doctor.scan_file(fp)
    print(f'  {" ".join(os.path.basename(fp).split("_")[1:]).replace(".py","")}:')
    for b in bugs:
        print(f'    [{b["severity"]}] L{b["line"]} {b["pattern"]} — {b["fix_tip"][:40]}')

report = doctor.get_report()
print(f'\n  总计: {report["total_bugs"]} bugs in {report["files_scanned"]} files')
print(f'  严重: {report["by_severity"].get("CRITICAL", 0)} Critical')
print(f'  高: {report["by_severity"].get("HIGH", 0)} High')
print(f'  中: {report["by_severity"].get("MEDIUM", 0)} Medium')

print(f'\n✅ 染色体9 代码修补部 验证通过')
assert report["total_bugs"] > 0, "Must detect bugs"
