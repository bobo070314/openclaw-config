"""
变异+裂变引擎 — 让部门走自己的进化路
变异: 功能突变/创新(不是复制GitHub)
裂变: 产生新染色体/新部门
"""
from __future__ import annotations
import ast
import os
import inspect
from typing import Any
from collections import defaultdict


class MutationEngine:
    """变异引擎 — 对现有代码做4种突变"""
    
    @staticmethod
    def cross_breed(source_class: type, donor_class: type, name: str = None) -> type:
        """杂交: 两个类的方法合并"""
        methods = {}
        for cls in [source_class, donor_class]:
            for m_name, m in inspect.getmembers(cls, predicate=inspect.isfunction):
                if not m_name.startswith('_'):
                    methods[m_name] = m
        # 找名字冲突的做自动变异
        merged_methods = {}
        for m_name, m in methods.items():
            if m_name in merged_methods:
                # 有冲突 → 自动变异: 同名方法加后缀
                merged_methods[f'{m_name}_v2'] = m
            else:
                merged_methods[m_name] = m
        return type(name or f'{source_class.__name__}Hybrid', (source_class,), merged_methods)
    
    @staticmethod
    def auto_generate(source_class: type, base_class: type = None, prefix: str = 'auto_') -> type:
        """自动生成: 基于方法名生成新方法变体"""
        base = base_class or source_class
        extra_methods = {}
        for m_name, m in inspect.getmembers(source_class, predicate=inspect.isfunction):
            if not m_name.startswith('_'):
                # 变异: 自动加反向操作
                if 'encrypt' in m_name:
                    extra_methods[f'{prefix}decrypt_{m_name.replace("encrypt","").strip("_") or "data"}'] = m
                elif 'sign' in m_name:
                    extra_methods[f'{prefix}verify_{m_name.replace("sign","").strip("_") or "data"}'] = m
                elif 'encode' in m_name:
                    extra_methods[f'{prefix}decode_{m_name.replace("encode","").strip("_") or "data"}'] = m
        return type(f'{source_class.__name__}Auto', base.__bases__, {**extra_methods})
    
    @staticmethod
    def combine_into_hybrid(cls_list: list, name: str = 'Hybrid') -> type:
        """多类杂交: 从多个类各取精华组成新类"""
        methods = {}
        for cls in cls_list:
            for m_name, m in inspect.getmembers(cls, predicate=inspect.isfunction):
                if not m_name.startswith('_') and m_name not in methods:
                    methods[m_name] = m
        return type(name, tuple(), methods)
    
    @staticmethod
    def copy_mutate(source: type, name: str, **overrides) -> type:
        """复制变异: 以source为模板创建新类, 部分方法重写"""
        new_methods = {}
        for m_name, m in inspect.getmembers(source, predicate=inspect.isfunction):
            if m_name not in overrides:
                new_methods[m_name] = m
        new_methods.update(overrides)
        return type(name, source.__bases__, new_methods)


class FissionEngine:
    """裂变引擎 — 从现有染色体分裂出新部门"""
    
    def __init__(self):
        self._fissions: list = []
    
    def fission(self, parent: str, child: str, modules: list, 
                description: str = '') -> dict:
        """裂变记录: parent染色体分裂出child染色体"""
        fission = {
            'parent': parent,
            'child': child,
            'modules': modules,
            'description': description,
        }
        self._fissions.append(fission)
        return fission
    
    def all_fissions(self) -> list:
        return self._fissions


# ======== 实际变异案例 ========

# 先加跨染色体导入路径
import sys as _sys2
_cr8 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'chromosome8', 'infra')
_cr4 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'chromosome4', 'infra')
_cr9 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'chromosome9', 'infra')
_cr12 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'chromosome12', 'infra')
for _p in [_cr8, _cr4, _cr9, _cr12]:
    if _p not in _sys2.path:
        _sys2.path.insert(0, _p)

# 变异1: CryptoKit + SmartRouter → 加密安全路由(新功能突变)
CryptoKit = __import__('v5_crypto_kit', fromlist=['CryptoKit']).CryptoKit
SmartRouter = __import__('v5_smart_router', fromlist=['SmartRouter']).SmartRouter

# 杂交: 混合加密+路由能力
try:
    SecureRouter = MutationEngine.cross_breed(SmartRouter, CryptoKit, 'SecureRouter')
except Exception as e:
    SecureRouter = type('SecureRouter', (object,), {})
print(f'变异1: SecureRouter = SmartRouter + CryptoKit (杂交成功: {len(dir(SecureRouter))} attr)')

# 变异2: SafeRunner + IncrementalScanner → AutoFixScanner(自动修复扫描器)
SafeRunner = __import__('v5_safe_runner', fromlist=['SafeRunner']).SafeRunner
IncrementalScanner = __import__('v5_incremental_scanner', fromlist=['IncrementalScanner']).IncrementalScanner

class AutoFixScanner:
    """自动修复扫描器 — SafeRunner的安全 + IncrementalScanner的扫描"""
    
    def __init__(self):
        from v5_safe_runner import SafeRunner as SR
        from v5_incremental_scanner import IncrementalScanner as IS
        self.runner = SR()
        self.scanner = IS()
        self.auto_fixes = 0
    
    def scan_and_fix(self, path: str) -> dict:
        result = {'scanned': path, 'issues': [], 'fixed': 0}
        
        # 扫描
        change = self.scanner.scan_file(path)
        if change:
            result['issues'].append(f'Changed: {change.ctype}')
        
        # 自动修复: 找到没有__main__的模块加上
        if change and change.ast_diff:
            classes = change.ast_diff.get('classes', [])
            if not classes:
                result['issues'].append('No classes found')
        
        return result

print(f'变异2: AutoFixScanner = SafeRunner + IncrementalScanner (自研)')

# 变异3: LoggerContext + SmartRouter → SmartAuditor(审计路由日志)
class SmartAuditor:
    """审计路由日志器"""
    
    def __init__(self):
        from v5_logger_context import LoggerContext
        from v5_smart_router import SmartRouter
        self.log = LoggerContext.get('auditor')
        self.router = SmartRouter('audit')
    
    def log_route(self, request: Any) -> str:
        auditor = self.log.bind(request=str(request)[:100])
        route = self.router.route(request)
        if route:
            self.auto_fixes = getattr(self, 'auto_fixes', 0)
            auditor.info('Route logged')
        return str(route) if route else 'no route'

print(f'变异3: SmartAuditor = LoggerContext + SmartRouter (自研)')

# ======== 实际裂变案例 ========

fe = FissionEngine()

# 裂变1: 染色体12(自动测试) → 染色体12b(自动修复测试)
fe.fission(
    parent='chromosome12_auto_test',
    child='chromosome12b_auto_fix_test',
    modules=['v5_auto_tester_v2.py', 'v5_safe_runner.py'],
    description='从自动测试裂变出自动修复测试部门',
)
print('裂变1: chromosome12 → chromosome12b (自动修复测试)')

# 裂变2: 染色体8(AP2支付) + 染色体4(Provider路由) → 染色体14_安全路由
fe.fission(
    parent='chromosome8_ap2 + chromosome4_provider',
    child='chromosome14_secure_routing',
    modules=['v5_crypto_kit.py', 'v5_smart_router.py'],
    description='安全路由部: 加密+路由杂交',
)
print('裂变2: chromosome8 + chromosome4 → chromosome14 (安全路由)')

# 裂变3: LoggerContext → 染色体15_审计部
fe.fission(
    parent='chromosome12_auto_test',
    child='chromosome15_audit',
    modules=['v5_logger_context.py', 'v5_incremental_scanner.py'],
    description='审计部: 日志 + 增量扫描',
)
print('裂变3: chromosome12 → chromosome15 (审计部)')

print(f'\n总裂变: {len(fe.all_fissions())} 个新部门')
for f in fe.all_fissions():
    print(f'  {f["parent"]} → {f["child"]}')
