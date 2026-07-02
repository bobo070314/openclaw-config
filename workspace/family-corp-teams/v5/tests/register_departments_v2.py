"""IGP 部门注册 v2 — 只创建符号注册，不复制文件"""
import os

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
CHRO_BASE = os.path.join(V5, 'chromosomes')

# 硅胶体记忆 → chromosome13
CH13 = os.path.join(CHRO_BASE, 'chromosome13_silicon_memory', 'infra')
os.makedirs(CH13, exist_ok=True)

# 创建 v5_silicon_memory 的软入口文件（实际代码回源v6/silicon_memory）
ch13_main = os.path.join(CH13, 'v5_silicon_memory.py')
if not os.path.exists(ch13_main):
    with open(ch13_main, 'w', encoding='utf-8') as f:
        f.write("""\"\"\"IGP Chromosome 13: 硅胶体记忆部 — 回源 v6/silicon_memory\"\"\"
import sys, os as _os
_SRC = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))), 'v6', 'silicon_memory')
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)
from v5_silicon_memory import *
""")
    print(f"CREATED: {ch13_main}")

# chromosome16 — infrastructure (API+CLI)
CH16 = os.path.join(CHRO_BASE, 'chromosome16_infrastructure', 'infra')
os.makedirs(CH16, exist_ok=True)

api_src = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))), 'v6', 'api')

ch16_main = os.path.join(CH16, '__init__.py')
