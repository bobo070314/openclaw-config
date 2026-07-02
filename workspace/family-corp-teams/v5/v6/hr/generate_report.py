"""IGP HR 部门 — 岗位说明书自动生成报告"""
from __future__ import annotations
import os
import sys
import time
import ast

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
sys.path.insert(0, V5)
sys.path.insert(0, os.path.join(V5, 'absorb', 'docagent'))
sys.path.insert(0, os.path.join(V5, 'absorb'))

try:
    from v5_job_engine import Reader
    has_engine = True
    print(f"  Reader loaded: {Reader}")
except Exception as e:
    print(f"JobEngine Reader import失败: {e}, 使用回落模式")
    has_engine = False

HR_DIR = os.path.join(V5, 'v6', 'hr')
os.makedirs(HR_DIR, exist_ok=True)

# 扫描所有Python文件
python_files = []
for root, dirs, files in os.walk(V5):
    if '.git' in root or '__pycache__' in root:
        continue
    for f in files:
        if f.endswith('.py'):
            python_files.append(os.path.join(root, f))

print(f"扫描 {len(python_files)} 个Python文件...")

# ======== AST扫描 ========
by_chrom = {}
chrom_order = []

for fp in python_files:
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content)
        classes = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
        functions = len([n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))])
        
        rel = os.path.relpath(fp, V5)
        parts = rel.replace('\\', '/').split('/')
        
        # 染色体分类
        chrom = "other"
        for p in parts:
            if p.startswith('chromosome'):
                chrom = p
                break
        if chrom == "other":
            if 'v6' in parts:
                chrom = "chromosome_v6"
            elif 'absorb' in parts:
                chrom = "chromosome_absorb"
            elif 'deploy' in parts:
                chrom = "deploy"
            elif 'igp_inject' in parts:
                chrom = "igp_inject"
            elif 'job_descriptions' in parts:
                chrom = "job_descriptions"
        
        if chrom not in by_chrom:
            by_chrom[chrom] = {'files': 0, 'classes': 0, 'functions': 0, 'lines': 0}
            chrom_order.append(chrom)
        by_chrom[chrom]['files'] += 1
        by_chrom[chrom]['classes'] += classes
        by_chrom[chrom]['functions'] += functions
        by_chrom[chrom]['lines'] += content.count('\n') + 1
        
    except Exception:
        pass

# ======== 排序 ========
def sort_key(chrom):
    digits = ''.join(c for c in chrom if c.isdigit())
    return (0, int(digits)) if digits else (1, chrom)

chrom_order.sort(key=sort_key)

# ======== 生成报告 ========
total_files = sum(v['files'] for v in by_chrom.values())
total_classes = sum(v['classes'] for v in by_chrom.values())
total_funcs = sum(v['functions'] for v in by_chrom.values())
total_lines = sum(v['lines'] for v in by_chrom.values())

report_path = os.path.join(HR_DIR, 'job_report.md')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(f"# IGP HR 岗位说明书报告\n\n")
    f.write(f"**生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write("---\n\n")
    
    f.write("## 总览\n\n")
    f.write("| 指标 | 数值 |\n|---|---|\n")
    f.write(f"| 扫描文件数 | {total_files} |\n")
    f.write(f"| 检测到类数 | {total_classes} |\n")
    f.write(f"| 检测到函数数 | {total_funcs} |\n")
    f.write(f"| 总代码行数 | {total_lines:,} |\n")
    f.write(f"| 染色体数 | {len(by_chrom)} |\n\n")
    
    f.write("## 按染色体分组\n\n")
    f.write("| 染色体 | 文件 | 类 | 函数 | 代码行 | 类/文件 | 岗位充足率 |\n")
    f.write("|---|---|---|---|---|---|---|\n")
    
    for chrom in chrom_order:
        v = by_chrom[chrom]
        positions = v['classes'] + v['lines'] // 200
        adequacy = min(100, positions * 10)
        cls_per_file = round(v['classes'] / v['files'], 1) if v['files'] else 0
        f.write(f"| {chrom} | {v['files']} | {v['classes']} | {v['functions']} | {v['lines']:,} | {cls_per_file} | {adequacy}% |\n")
    
    f.write("\n## 代码行热力图\n\n")
    max_lines = max(v['lines'] for v in by_chrom.values()) or 1
    for chrom in chrom_order:
        v = by_chrom[chrom]
        bar_len = v['lines'] * 40 // max_lines
        bar = '█' * bar_len + '░' * (40 - bar_len)
        f.write(f"  {chrom:<25} {bar} {v['lines']:,}行\n")
    
    f.write("\n## 薄弱染色体（<3个类）\n\n")
    weak = [(c, v) for c, v in by_chrom.items() if v['classes'] < 3]
    if weak:
        for chrom, v in weak:
            f.write(f"- **{chrom}**: {v['classes']}个类, {v['functions']}个函数, {v['lines']}行\n")
    else:
        f.write("无\n")
    
    f.write("\n## 高产出染色体（>20个类）\n\n")
    rich = [(c, v) for c, v in by_chrom.items() if v['classes'] > 20]
    if rich:
        for chrom, v in rich:
            f.write(f"- **{chrom}**: {v['classes']}个类, {v['functions']}个函数, {v['lines']:,}行\n")
    else:
        f.write("无\n")
    
    f.write("\n## 待改进项\n\n")
    f.write("1. **染色体覆盖不完整**: " + str(len(weak)) + "个染色体少于3个类，需补充\n")
    f.write("2. **岗位描述文档**: 部分类缺少docstring，可参考v5_job_engine.py补充\n")
    f.write("3. **岗位漏斗**: Research→Alpha→Beta→GA的生命周期通路需加速\n\n")
    
    f.write("---\n")
    f.write("*报告由IGP HR部门自动生成*\n")

print(f"  ️ 报告已生成: {report_path}")

# ======== HR Dashboard ========
thin_chroms = sum(1 for v in by_chrom.values() if v['classes'] < 3)
rich_chroms = sum(1 for v in by_chrom.values() if v['classes'] >= 10)
avg_positions = total_classes / max(1, len(by_chrom))

dashboard_path = os.path.join(HR_DIR, 'hr_dashboard.txt')
with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write("IGP HR 部门岗位状况\n")
    f.write("=" * 55 + "\n")
    f.write(f"总岗位数(类):          {total_classes}\n")
    f.write(f"总函数数:              {total_funcs}\n")
    f.write(f"覆盖目录数:            {len(by_chrom)}\n")
    f.write(f"人均岗位(类/目录):      {avg_positions:.1f}\n")
    f.write(f"高产出目录(>=10类):     {rich_chroms}\n")
    f.write(f"薄弱目录(<3类):        {thin_chroms}\n")
    f.write(f"  -> 含: {', '.join(c for c, v in by_chrom.items() if v['classes'] < 3)}\n")
    f.write(f"丰满率:                {(1 - thin_chroms/max(1,len(by_chrom)))*100:.0f}%\n")
    f.write("=" * 55 + "\n")
    f.write(f"\n染色体分布:\n")
    for chrom in chrom_order:
        v = by_chrom[chrom]
        pct = v['lines'] * 100 / max(1, total_lines)
        f.write(f"  {chrom:<25} {v['classes']:3}类 {v['functions']:3}func {v['lines']:>6,}行 ({pct:.0f}%)\n")

print(f"  ️ Dashboard已生成: {dashboard_path}")

# ======== 打印摘要 ========
print(f"\n{'='*55}")
print(f"HR 报告摘要")
print(f"{'='*55}")
for chrom in chrom_order:
    v = by_chrom[chrom]
    pct = v['lines'] * 100 / max(1, total_lines)
    print(f"  {chrom:<25} {v['files']:3}个文件  {v['classes']:3}个类  {v['functions']:3}个函数  {v['lines']:>6,}行 ({pct:.0f}%)")
print(f"{'='*55}")
print(f"  总计: {total_files}个文件, {total_classes}个类, {total_funcs}个函数, {total_lines:,}行")
