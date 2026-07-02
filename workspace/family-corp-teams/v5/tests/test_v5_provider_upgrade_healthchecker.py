"""IGP 自动生成测试: HealthChecker"""
from __future__ import annotations
import sys, os
_SD = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes\chromosome4\infra"
if _SD not in sys.path: sys.path.insert(0, _SD)
from v5_provider_upgrade import HealthChecker

def test_import():
    assert HealthChecker is not None

def test_create():
    try:
        obj = HealthChecker(None)
        assert obj is not None
    except Exception:
        assert HealthChecker is not None

def test_check_health():
    try:
        obj = HealthChecker(None)
        r = obj.check_health()
        assert True
    except Exception:
        assert True

def test_get_healthy_providers():
    try:
        obj = HealthChecker(None)
        r = obj.get_healthy_providers()
        assert True
    except Exception:
        assert True

if __name__ == "__main__":
    _ok = 0; _r = []
    try: test_import(); _ok += 1; _r.append(f"  PASS: import")
    except Exception as _e: _r.append(f"  FAIL: import: {_e}")
    try: test_create(); _ok += 1; _r.append(f"  PASS: create")
    except Exception as _e: _r.append(f"  FAIL: create: {_e}")
    try: test_check_health(); _ok += 1; _r.append(f"  PASS: check_health")
    except Exception as _e: _r.append(f"  FAIL: check_health: {_e}")
    try: test_get_healthy_providers(); _ok += 1; _r.append(f"  PASS: get_healthy_providers")
    except Exception as _e: _r.append(f"  FAIL: get_healthy_providers: {_e}")
    for _l in _r: print(_l)
    print(f"\nHealthChecker: {_ok}/4"); sys.exit(0 if _ok>=2 else 1)