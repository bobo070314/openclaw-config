"""
染色体12: 自动测试部 🧪
吸收: Hypothesis属性测试思想 + logging注入 + 异常治理
补: V5缺陷2(异常处理粗糙) + 缺陷3(无日志) + 缺陷4(无测试)
0外部依赖，纯Python标准库
"""
import os, sys, ast, inspect, random, math, logging, traceback
from typing import Dict, List, Any, Callable, Tuple, Optional
from functools import wraps


# ====== 日志体系 ======

class V5Logger:
    """统一日志系统 — 自动注入所有V5模块"""
    
    _instances = {}
    
    @classmethod
    def get(cls, name: str):
        if name not in cls._instances:
            logger = logging.getLogger(f'igp.{name}')
            logger.setLevel(logging.INFO)
            if not logger.handlers:
                handler = logging.StreamHandler()
                fmt = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                                       datefmt='%H:%M:%S')
                handler.setFormatter(fmt)
                logger.addHandler(handler)
            cls._instances[name] = logger
        return cls._instances[name]


# ====== 自动测试生成器 ======

class AutoTester:
    """属性测试生成器 (从Hypothesis吸收核心思想)
    
    对函数自动生成边界测试用例:
    - int: 0, 1, -1, MAX, MIN, random
    - float: 0.0, 1.0, -1.0, inf, nan
    - str: empty, single char, long, unicode
    - list: empty, 1 elem, None elem, nested
    - dict: empty, string keys, nested
    """
    
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.results = []
        self.test_count = 0
        self.fail_count = 0
    
    def _generate_value(self, param_type: str, param_name: str = '') -> Any:
        """根据类型生成边界测试值"""
        strategies = {
            'int': [0, 1, -1, 2**31-1, -2**31, self.rng.randint(-1000, 1000)],
            'float': [0.0, 1.0, -1.0, float('inf'), float('-inf'), 1e-10, -1e-10],
            'str': ['', 'a', 'hello_world', 'x' * 100, '\u4e2d\u6587', 'null', 'None'],
            'bool': [True, False],
            'list': [[], [1], [None], [1, 2, 3], list(range(10))],
            'dict': [{}, {'key': 'value'}, {'a': 1, 'b': 2}, {1: 1, 2: 2}],
            'None': [None],
        }
        base = strategies.get(param_type, [None])
        return base[self.rng.randint(0, len(base) - 1)]
    
    def _infer_params(self, func: Callable) -> List[Dict]:
        """从函数签名推断参数类型"""
        sig = inspect.signature(func)
        params = []
        for name, param in sig.parameters.items():
            if name == 'self':
                continue
            anno = param.annotation if param.annotation != inspect.Parameter.empty else 'Any'
            # 简化类型映射
            type_map = {
                int: 'int', float: 'float', str: 'str', bool: 'bool',
                list: 'list', dict: 'dict', 'int': 'int', 'float': 'float',
                'str': 'str', 'bool': 'bool', 'list': 'list', 'dict': 'dict',
            }
            ptype = type_map.get(anno, 'int')
            params.append({
                'name': name,
                'type': ptype,
                'has_default': param.default != inspect.Parameter.empty,
            })
        return params
    
    def test_function(self, func: Callable, test_count: int = 20) -> Dict:
        """对函数运行自动测试"""
        params = self._infer_params(func)
        results = {'function': func.__name__, 'tests': [], 'passed': 0, 'failed': 0, 'errors': []}
        
        for i in range(test_count):
            args = []
            for p in params:
                val = self._generate_value(p['type'], p['name'])
                args.append(val)
            
            try:
                result = func(*args)
                results['tests'].append({'args': args, 'result': str(result)[:50], 'status': 'pass'})
                results['passed'] += 1
            except Exception as e:
                if str(e).startswith('Precondition failed'):
                    results['tests'].append({'args': args, 'error': 'precondition', 'status': 'skip'})
                else:
                    results['tests'].append({'args': args, 'error': str(e)[:80], 'status': 'fail'})
                    results['failed'] += 1
                    results['errors'].append({'args': args, 'error': str(e)})
        
        self.results.append(results)
        self.test_count += test_count
        self.fail_count += results['failed']
        return results
    
    def report(self) -> Dict:
        """生成测试报告"""
        total = self.test_count
        passed = total - self.fail_count
        return {
            'total': total,
            'passed': passed,
            'failed': self.fail_count,
            'pass_rate': round(passed / total * 100, 1) if total > 0 else 0,
            'has_crashes': any(r['failed'] > 0 for r in self.results),
        }


# ====== 异常治理 ======
class SafeRunner:
    """安全的函数执行器 — 统一异常治理
    
    将任意函数调用包装为Result对象:
    - .ok: 是否成功
    - .value: 成功时的返回值
    - .error: 失败时的异常信息
    """
    
    class Result:
        def __init__(self, ok: bool, value=None, error=None):
            self.ok = ok
            self.value = value
            self.error = error
        
        def __repr__(self):
            return f"Result(ok={self.ok}, value={self.value!r})" if self.ok else f"Result(ok=False, error={self.error})"
    
    @staticmethod
    def run(func: Callable, *args, **kwargs) -> 'SafeRunner.Result':
        try:
            result = func(*args, **kwargs)
            return SafeRunner.Result(True, value=result)
        except Exception as e:
            tb = traceback.format_exc()
            return SafeRunner.Result(False, error=f"{type(e).__name__}: {e}")


if __name__ == '__main__':
    print("🧪 染色体12 自动测试部 验证")
    
    import tempfile
    
    # 1. 日志测试
    logger = V5Logger.get('test')
    logger.info("Logging test: chromosome 12")
    logger.warning("Warning test: should appear")
    print("  Logger: ✅ instantiated")
    
    # 2. 自动测试测试
    def add(x: int, y: int) -> int:
        """加法"""
        return x + y
    
    def divide(a: float, b: float) -> float:
        """除法 - 可抛出异常"""
        return a / b
    
    tester = AutoTester(seed=99)
    add_result = tester.test_function(add, 10)
    div_result = tester.test_function(divide, 10)
    
    print(f"  add: {add_result['passed']}/{add_result['passed'] + add_result['failed']} passed")
    print(f"  divide: {div_result['passed']}/{div_result['passed'] + div_result['failed']} passed")
    
    report = tester.report()
    print(f"  总通过率: {report['pass_rate']}%")
    assert report['total'] == 20, f"Expected 20 tests, got {report['total']}"
    
    # 3. SafeRunner测试
    safe = SafeRunner()
    r1 = safe.run(lambda: 42)
    r2 = safe.run(lambda: 1/0)
    print(f"  SafeRunner success: {r1}")
    print(f"  SafeRunner error: {r2}")
    assert r1.ok
    assert not r2.ok
    
    print("\n✅ 染色体12 自动测试部 验证通过")
