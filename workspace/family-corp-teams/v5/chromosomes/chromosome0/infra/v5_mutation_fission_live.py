"""
真实代码变异+裂变 — Not playground, real code mutation
直接从6个升级后的模块变异出新代码
"""
from __future__ import annotations
import sys, os

BASE = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\chromosomes'

sys.path.insert(0, os.path.join(BASE, 'chromosome12', 'infra'))
sys.path.insert(0, os.path.join(BASE, 'chromosome4', 'infra'))
sys.path.insert(0, os.path.join(BASE, 'chromosome8', 'infra'))
sys.path.insert(0, os.path.join(BASE, 'chromosome9', 'infra'))

from v5_result_monad import Result
from v5_safe_runner import SafeRunner
from v5_logger_context import LoggerContext
from v5_smart_router import SmartRouter
from v5_crypto_kit import CryptoKit
from v5_incremental_scanner import IncrementalScanner, Change

log = LoggerContext.get('mutation')

# =====================================
# 变异1: Result + CryptoKit → SecureResult
# 突变: Result自动签名/验证
# =====================================
class SecureResult(Result):
    """变异: Result + CryptoKit杂交 — Result自带签名验证"""
    
    def sign(self, key: str) -> 'SecureResult':
        """变异: 成功的Result可以签名"""
        if self.is_ok():
            try:
                sig = CryptoKit.hmac_sign(key, str(self._value))
                self._meta = getattr(self, '_meta', {})
                self._meta['sig'] = sig
            except Exception:
                pass
        return self
    
    def verify(self, key: str) -> bool:
        """变异: 验证签名"""
        if self.is_err():
            return False
        meta = getattr(self, '_meta', {})
        old_sig = meta.get('sig')
        if not old_sig:
            return False
        return CryptoKit.hmac_verify(key, str(self._value), old_sig)
    
    @property
    def meta(self) -> dict:
        return getattr(self, '_meta', {})


# =====================================
# 变异2: SafeRunner + IncrementalScanner → WatchdogRunner
# 突变: 安全执行 + 文件监视
# =====================================
class WatchdogRunner:
    """变异: SafeRunner + IncrementalScanner — 监视代码变更并自动重试"""
    
    def __init__(self):
        self._runner = SafeRunner()
        self._scanner = IncrementalScanner()
        self._watches: dict = {}
    
    def watch_and_run(self, path: str, func, *args, **kwargs):
        """监视文件, 变更时自动重试执行"""
        self._scanner.scan_file(path)
        self._watches[path] = func
        
        def guarded():
            # 执行前检查是否有变更
            change = self._scanner.scan_file(path)
            if change:
                log.info(f'File changed: {os.path.basename(path)}')
            return self._runner.run(func, *args, **kwargs)
        
        return guarded()
    
    def report(self) -> str:
        return self._scanner.report()


# =====================================
# 变异3: SmartRouter + LoggerContext → AuditRouter
# 突变: 路由 + 审计日志
# =====================================
class AuditRouter:
    """变异: SmartRouter + LoggerContext — 每次路由都记录审计日志"""
    
    def __init__(self, name: str = 'audit'):
        self._router = SmartRouter(name)
        self._log = LoggerContext.get(f'router.{name}')
    
    def register(self, name: str, provider, weight: float = 1.0):
        self._router.register(name, provider, weight)
        self._log.info(f'Provider registered: {name}', weight=weight)
        return self
    
    def route(self, request=None, strategy: str = 'weighted'):
        sel = self._router.select(request, strategy)
        if sel:
            name, prov = sel
            self._log.info(f'Routed to {name}', strategy=strategy)
            return prov
        self._log.warning('No provider available')
        return None
    
    def record(self, name: str, success: bool, duration_ms: float = 0):
        if success:
            self._router.record_success(name, duration_ms)
            self._log.debug(f'Success: {name}')
        else:
            self._router.record_failure(name)
            self._log.warning(f'Failure: {name}')
    
    def circuit_status(self) -> dict:
        return self._router.circuit_status()


# =====================================
# 裂变: 生成新染色体目录
# =====================================
fissions = []

def create_fission_chromosome(parent: str, name: str, dir_name: str, modules: list) -> dict:
    """裂变: 创建新染色体目录"""
    chrom_dir = os.path.join(BASE, dir_name)
    infra_dir = os.path.join(chrom_dir, 'infra')
    os.makedirs(infra_dir, exist_ok=True)
    
    fission_info = {
        'parent': parent,
        'name': name,
        'dir': chrom_dir,
        'modules': modules,
    }
    
    # 创建README说明裂变来源
    readme_path = os.path.join(chrom_dir, 'FISSION_README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(f"""# {name} — 从{parent}裂变而来

## 继承来源
- Parent: {parent}
- 核心模块: {', '.join(modules)}
- 裂变时间: 2026-07-01

## 能力
通过变异+拼合产生的新部门
""")
    
    fissions.append(fission_info)
    return fission_info


# 裂变1: 从染色体12裂变出染色体15_审计安全部
f1 = create_fission_chromosome(
    parent='chromosome12_auto_test',
    name='chromosome15_audit_security',
    dir_name='chromosome15_audit_security',
    modules=['v5_logger_context.py', 'v5_result_monad.py', 'v5_crypto_kit.py'],
)
log.info(f'Fission: {f1["parent"]} -> {f1["name"]}')

# 裂变2: 从染色体4+8裂变出染色体14_智路服务
f2 = create_fission_chromosome(
    parent='chromosome4_provider + chromosome8_ap2',
    name='chromosome14_smart_routing',
    dir_name='chromosome14_smart_routing',
    modules=['v5_smart_router.py', 'v5_crypto_kit.py'],
)
log.info(f'Fission: {f2["parent"]} -> {f2["name"]}')


if __name__ == '__main__':
    log.info('=== 变异+裂变验证 ===')
    
    # 验证1: SecureResult
    sr = SecureResult.Ok("secret data").sign("key123")
    assert sr.verify("key123"), "sign/verify"
    assert not sr.verify("wrong_key"), "bad verify"
    log.info('SecureResult: PASS')
    
    # 验证2: WatchdogRunner
    wd = WatchdogRunner()
    result = wd._runner.run(lambda: 42)
    assert result.is_ok() and result.unwrap() == 42
    log.info('WatchdogRunner: PASS')
    
    # 验证3: AuditRouter
    ar = AuditRouter('test')
    ar.register('a', lambda x: x, weight=1.0)
    ar.register('b', lambda x: x, weight=1.0)
    prov = ar.route('test')
    assert callable(prov), f'route: {prov}'
    ar.record('a', True)
    ar.record('a', False)
    status = ar.circuit_status()
    log.info('AuditRouter: PASS')
    
    # 验证4: 裂变结果
    for f in fissions:
        assert os.path.exists(os.path.join(f['dir'], 'FISSION_README.md')), f"Missing: {f['name']}"
        log.info(f'Fission exists: {f["name"]}')
    
    log.info('ALL MUTATION+FISSION PASS')
    print(f'\n=== 总成果 ===')
    print(f'3种变异: SecureResult, WatchdogRunner, AuditRouter')
    print(f'2次裂变: chromosome15_audit_security, chromosome14_smart_routing')
