"""
染色体13: 人力资源部 — 岗位说明书生成与维护
吸收自: facebookresearch/DocAgent (ACL 2025)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from infra.v5_hr_engine import main

if __name__ == '__main__':
    main()
