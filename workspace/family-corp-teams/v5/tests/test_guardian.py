"""IGP 自动生成测试: guardian_act"""
from __future__ import annotations
import sys, os
_D = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome5\infra"
if _D not in sys.path: sys.path.insert(0, _D)
from guardian_act import GuardianAct

def test_module():
    assert GuardianAct is not None

if __name__ == "__main__":
    try: test_module(); print("PASS: module")
    except Exception as e: print(f"FAIL: {e}")