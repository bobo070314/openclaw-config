"""IGP 单元测试: KnowledgeBase"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome10", "infra"))
import v5_logic_upgrade
def test_module():
    assert hasattr(v5_logic_upgrade, 'KnowledgeBase')
def test_contains():
    assert 'KnowledgeBase' in dir(v5_logic_upgrade)
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("module",test_module),("contains",test_contains)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nKnowledgeBase: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
