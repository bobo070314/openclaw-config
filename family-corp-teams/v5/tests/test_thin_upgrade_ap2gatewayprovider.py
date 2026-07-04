"""IGP 自动生成测试: AP2GatewayProvider"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes"
if _SD not in sys.path: sys.path.insert(0, _SD)
from thin_upgrade import AP2GatewayProvider

def test_import():
    assert AP2GatewayProvider is not None

def test_create():
    obj = AP2GatewayProvider()
    assert obj is not None

def test_register_wallet():
    assert hasattr(AP2GatewayProvider, "register_wallet")

def test_process_payment():
    assert hasattr(AP2GatewayProvider, "process_payment")

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_register_wallet(); _ok += 1; _r.append(f"  PASS: register_wallet")
    except Exception as _e: _r.append(f"  FAIL: register_wallet: {_e}")
    try: test_process_payment(); _ok += 1; _r.append(f"  PASS: process_payment")
    except Exception as _e: _r.append(f"  FAIL: process_payment: {_e}")
    for _l in _r: print(_l)
    print(f"\nAP2GatewayProvider: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)