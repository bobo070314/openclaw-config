"""
染色体12自动测试部 — 使用升级后的 Result + SafeRunner + LoggerContext
改造原 v5_auto_tester.py，注入新基础设施
这是部门实际用的版本，不是研发的玩具
"""
from __future__ import annotations
import sys, os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

from v5_result_monad import Result
from v5_safe_runner import SafeRunner
from v5_logger_context import LoggerContext, root as log_root

log = log_root.bind(module='auto_tester')


class TestResult:
    """测试结果 — 使用Result monad作为internal"""
    
    def __init__(self, name: str, passed: bool, details: str = '', duration_ms: float = 0):
        self.name = name
        self.passed = passed
        self.details = details
        self.duration_ms = duration_ms
    
    @classmethod
    def from_result(cls, name: str, result: Result, duration_ms: float = 0) -> 'TestResult':
        if result.is_ok():
            return cls(name, True, str(result.unwrap_or('')), duration_ms)
        return cls(name, False, str(result.err() or ''), duration_ms)
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'passed': self.passed,
            'details': self.details,
            'duration_ms': self.duration_ms,
        }


class TestSuite:
    """测试套件 — 带SafeRunner重试+超时保护"""
    
    def __init__(self, name: str = 'default'):
        self.name = name
        self.tests: list = []
        self._runner = SafeRunner(default_retries=2, default_timeout=10.0)
    
    def add(self, name: str, func, *args, retries: int = None, timeout: float = None, **kwargs):
        """添加一个测试用例"""
        self.tests.append({
            'name': name,
            'func': func,
            'args': args,
            'kwargs': kwargs,
            'retries': retries,
            'timeout': timeout,
        })
        return self
    
    def run_all(self) -> list[TestResult]:
        """运行全部测试"""
        results = []
        for test in self.tests:
            log.info(f'Running test: {test["name"]}')
            r = self._runner.run(
                test['func'], *test['args'],
                retries=test['retries'],
                timeout=test['timeout'],
                name=test['name'],
                **test['kwargs'],
            )
            tr = TestResult.from_result(test['name'], r, 0.0)
            results.append(tr)
            
            if tr.passed:
                log.info(f'  PASS: {test["name"]}')
            else:
                log.warning(f'  FAIL: {test["name"]} - {tr.details}')
        
        passed = sum(1 for r in results if r.passed)
        log.info(f'Test suite {self.name}: {passed}/{len(results)} passed')
        return results
    
    def run_safe(self, name: str, func, *args, **kwargs) -> TestResult:
        """单测试安全执行"""
        r = self._runner.run(func, *args, name=name, **kwargs)
        return TestResult.from_result(name, r)
    
    def statistics(self) -> dict:
        return {
            'name': self.name,
            'total': len(self.tests),
            'runner_stats': self._runner.statistics(),
        }


class AutoTester:
    """自动测试器 — 全自动运行/验证/报告"""
    
    def __init__(self, base_dir: str = '.'):
        self.base_dir = base_dir
        self._suites: dict[str, TestSuite] = {}
        self._runner = SafeRunner()
    
    def add_suite(self, name: str, suite: TestSuite):
        self._suites[name] = suite
        log.info(f'Suite added: {name}')
    
    def run_module(self, module_path: str) -> Result:
        """安全运行一个模块的测试"""
        def _run():
            result = {}
            exec_globals = {}
            try:
                with open(module_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                exec(compile(code, module_path, 'exec'), exec_globals)
                result['file'] = _os.path.basename(module_path)
                result['status'] = 'executed'
            except SyntaxError as e:
                result['file'] = _os.path.basename(module_path)
                result['status'] = 'syntax_error'
                result['error'] = str(e)
            return result
        return self._runner.run(_run, name=f'module:{_os.path.basename(module_path)}')
    
    def run_all_modules(self) -> list[Result]:
        """扫描并运行目录下所有Python模块"""
        results = []
        for root, dirs, files in _os.walk(self.base_dir):
            for f in files:
                if f.endswith('.py') and not f.startswith('__'):
                    r = self.run_module(_os.path.join(root, f))
                    results.append(r)
        return results
    
    def generate_report(self, results: list) -> str:
        """生成Markdown测试报告"""
        passed = sum(1 for r in results if r.is_ok())
        log.info(f'Report: {passed}/{len(results)} modules ok', total=len(results))
        return f'# Auto Test Report\n\n{passed}/{len(results)} modules passed\n'


# 快速验证
if __name__ == '__main__':
    log.info('=== AutoTester self-test ===')
    
    suite = TestSuite('smoke')
    suite.add('add', lambda a, b: a + b, 1, 2)
    suite.add('div', lambda a, b: a / b, 10, 2)
    suite.add('error', lambda: 1/0)  # should fail gracefully
    
    results = suite.run_all()
    assert results[0].passed, 'add should pass'
    assert results[2].passed == False, 'div by zero should fail'
    
    log.info('AutoTester self-test: PASS', passed=sum(1 for r in results if r.passed))
