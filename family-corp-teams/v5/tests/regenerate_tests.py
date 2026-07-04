"""批量重写所有13个新测试文件（用真实API）"""
from __future__ import annotations
import os

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
td = os.path.join(V5, 'tests')

tests = {}

tests['test_code_analyzer.py'] = '''"""IGP 单元测试: CodeAnalyzer"""
from __future__ import annotations
import sys, os
V5 = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome0", "infra"))
from v5_code_analyzer import CodeAnalyzer
def test_create():
    ca = CodeAnalyzer(V5); assert ca is not None
def test_scan():
    ca = CodeAnalyzer(V5); r = ca.scan_dead_code(); assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("scan",test_scan)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\\nCodeAnalyzer: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''

tests['test_smart_router.py'] = '''"""IGP 单元测试: SmartRouter"""
from __future__ import annotations
import sys, os
V5 = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome4", "infra"))
from v5_smart_router import SmartRouter
def test_create():
    sr = SmartRouter("test"); assert sr is not None
def test_route():
    sr = SmartRouter("test"); r = sr.route({"type":"test"})
    assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("route",test_route)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\\nSmartRouter: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''

tests['test_guardian_policy.py'] = '''"""IGP 单元测试: GuardianPolicy"""
from __future__ import annotations
import sys, os
V5 = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome5", "infra"))
from guardian_policy import GuardianPolicy
def test_create():
    gp = GuardianPolicy(); assert gp is not None
def test_check_file():
    gp = GuardianPolicy(); r = gp.check_file_op("/tmp/test.txt", "delete")
    assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("check_file",test_check_file)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\\nGuardianPolicy: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''

tests['test_incremental_scanner.py'] = '''"""IGP 单元测试: IncrementalScanner"""
from __future__ import annotations
import sys, os
V5 = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome9", "infra"))
from v5_incremental_scanner import IncrementalScanner
def test_create():
    s = IncrementalScanner(); assert s is not None
def test_report():
    s = IncrementalScanner(); r = s.report()
    assert isinstance(r, dict)
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("report",test_report)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\\nIncrementalScanner: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''

tests['test_logger_context.py'] = '''"""IGP 单元测试: LoggerContext"""
from __future__ import annotations
import sys, os
V5 = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome12", "infra"))
from v5_logger_context import LoggerContext
def test_create():
    lc = LoggerContext("test"); assert lc is not None
def test_info():
    lc = LoggerContext("test"); lc.info("test"); assert True
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("info",test_info)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\\nLoggerContext: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''

tests['test_mcp_client.py'] = '''"""IGP 单元测试: MCPClient"""
from __future__ import annotations
import sys, os
V5 = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome1", "infra"))
from igp_mcp_v5_client import MCPClient
def test_create():
    mc = MCPClient("http://localhost:8000"); assert mc is not None
def test_connected():
    mc = MCPClient("http://localhost:8000"); r = mc.is_connected()
    assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("connected",test_connected)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\\nMCPClient: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''

tests['test_result_monad.py'] = '''"""IGP 单元测试: Result"""
from __future__ import annotations
import sys, os
V5 = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome12", "infra"))
from v5_result_monad import Result
def test_ok():
    r = Result.Ok(42); assert r.is_ok
def test_err():
    r = Result.Err("err"); assert r.is_err
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("ok",test_ok),("err",test_err)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\\nResult: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''

tests['test_agent_commerce.py'] = '''"""IGP 单元测试: AgentCommerceEngine"""
from __future__ import annotations
import sys, os
V5 = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome6", "infra"))
from agent_commerce_v2 import AgentCommerceEngine
def test_create():
    ac = AgentCommerceEngine(); assert ac is not None
def test_charge():
    ac = AgentCommerceEngine(); r = ac.charge_task("test", 0)
    assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("charge",test_charge)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\\nAgentCommerceEngine: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''

tests['test_commerce_pk.py'] = '''"""IGP 单元测试: CommercePKRank"""
from __future__ import annotations
import sys, os
V5 = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome6", "infra"))
from commerce_pk_v2 import CommercePKRank
def test_create():
    cp = CommercePKRank(); assert cp is not None
def test_ranking():
    cp = CommercePKRank(); r = cp.get_ranking()
    assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("ranking",test_ranking)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\\nCommercePKRank: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''

tests['test_safe_runner.py'] = '''"""IGP 单元测试: SafeRunner"""
from __future__ import annotations
import sys, os
V5 = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome12", "infra"))
from v5_safe_runner import SafeRunner
def test_create():
    sr = SafeRunner(); assert sr is not None
def test_run():
    sr = SafeRunner(); r = sr.run(lambda: 42)
    assert r is not None
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("run",test_run)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\\nSafeRunner: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''

tests['test_agent_os_kernel.py'] = '''"""IGP 单元测试: AgentOSKernel"""
from __future__ import annotations
import sys, os
V5 = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\v5"
sys.path.insert(0, os.path.join(V5, "chromosomes", "chromosome7", "infra"))
from agent_os_kernel import AgentOSKernel
def test_create():
    k = AgentOSKernel(); assert k is not None
def test_register():
    k = AgentOSKernel(); k.register_agent("test", {"name":"test"})
    s = k.status(); assert s.get("agents",0) >= 1
if __name__ == "__main__":
    _ok = 0; _r = []
    for _n, _f in [("create",test_create),("register",test_register)]:
        try: _f(); _ok+=1; _r.append(f"  PASS: {_n}")
        except Exception as e: _r.append(f"  FAIL: {_n}: {e}")
    for l in _r: print(l)
    print(f"\\nAgentOSKernel: {_ok}/2"); sys.exit(0 if _ok==2 else 1)
'''

# 写入
for name, content in tests.items():
    path = os.path.join(td, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Written: {name}")

# 修复 fastmcp_export.py 的语法错误
fastmcp_path = os.path.join(V5, 'chromosomes', 'chromosome1', 'infra', 'fastmcp_export.py')
src = open(fastmcp_path, 'r', encoding='utf-8').read()
# indent error on line 14
lines = src.split('\n')
print(f"\\nfastmcp_export.py line 14: {lines[13][:60] if len(lines) > 13 else 'N/A'}")
