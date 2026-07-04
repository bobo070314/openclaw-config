"""IGP 自动生成测试: lifecycle"""
from __future__ import annotations
import sys, os
_D = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6"
if _D not in sys.path: sys.path.insert(0, _D)
from v6_lifecycle import LifecycleManager

def test_module():
    assert LifecycleManager is not None

if __name__ == "__main__":
    try: test_module(); print("PASS: module")
    except Exception as e: print(f"FAIL: {e}")