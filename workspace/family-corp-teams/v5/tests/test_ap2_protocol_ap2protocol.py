"""IGP 单元测试: AP2Protocol"""
from __future__ import annotations
import sys, os
V5 = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome8", "infra"))
from ap2_protocol import AP2Protocol
def test_create():
    obj = AP2Protocol(); assert obj is not None
def test_create_payment_request():
    obj = AP2Protocol()
    r = obj.create_payment_request("agent1", "agent2", 100, "IGP")
    assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("create_payment_request",test_create_payment_request)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\nAP2Protocol: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
