"""IGP 新部门真实运行验证"""
import sys, os, subprocess

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
CHRO_BASE = os.path.join(V5, 'chromosomes')

# 新部门的代码都要通过 import 验证
NEW_CHROMS = {
    'chromosome13_silicon_memory': {
        'path': os.path.join(V5, 'v6', 'silicon_memory'),
        'imports': ['v5_silicon_memory'],
    },
    'chromosome16_infrastructure': {
        'path': os.path.join(V5, 'v6', 'api'),
        'imports': ['igp_api', 'igp_api_client'],
    },
    'chromosome17_devops': {
        'path': os.path.join(V5, 'v6', 'ci'),
        'imports': ['deploy'],
    },
    'chromosome18_core_engine': {
        'path': os.path.join(V5, 'v6'),
        'imports': ['v6_lifecycle', 'scan_registry'],
    },
    'chromosome19_product_delivery': {
        'path': os.path.join(V5, 'v6'),
        'imports': ['prd.prd_queue', 'review.v6_review_agents'],
    },
}

print("=" * 65)
print("  新部门真实运行验证")
print("=" * 65)
print()

all_ok = True
for chrom, info in NEW_CHROMS.items():
    d = info['path'].replace('/', '\\')
    print(f"  [{chrom}]")
    
    if not os.path.isdir(d):
        print(f"    ❌ 目录不存在: {d}")
        all_ok = False
        continue
    
    # 确认目录下的文件
    files = [f for f in os.listdir(d) if f.endswith('.py') and f != '__pycache__']
    print(f"      文件: {len(files)} → {', '.join(files[:5])}{'...' if len(files)>5 else ''}")
    
    # 逐个import验证
    for mod_name in info['imports']:
        cmd = [sys.executable, '-W', 'ignore', '-c', 
               f'import sys; sys.path.insert(0, r"{d}"); __import__("{mod_name}"); print("OK")']
        r = subprocess.run(cmd, capture_output=True, timeout=15, text=True, encoding='utf-8')
        if r.returncode == 0 and 'OK' in (r.stdout or ''):
            print(f"    ✅ import {mod_name} 成功")
        else:
            err = (r.stderr or r.stdout or '').split('\n')[0]
            print(f"    ❌ import {mod_name} 失败: {err[:120]}")
            all_ok = False

# 验证chromosome13能否从染色体目录导入
print()
print("  [跨染色体引用验证]")
d13 = os.path.join(CHRO_BASE, 'chromosome13_silicon_memory', 'infra')
if os.path.isdir(d13):
    cmd = [sys.executable, '-W', 'ignore', '-c',
           f'import sys; sys.path.insert(0, r"{d13}"); __import__("v5_silicon_memory"); print("chromosome13: OK")']
    r = subprocess.run(cmd, capture_output=True, timeout=15, text=True, encoding='utf-8')
    if 'OK' in (r.stdout or ''):
        print("    ✅ chromosome13/infra/v5_silicon_memory.py import 成功")
    else:
        print(f"    ❌ chromosome13 import: {(r.stderr or r.stdout or '')[:120]}")
        all_ok = False

print()
if all_ok:
    print("  ✅ 全部新部门可真实运行!")
else:
    print("  ⚠️ 部分部门有import错误，需要修复")
print("=" * 65)
