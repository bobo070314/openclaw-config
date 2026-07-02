"""
IGP SafeRunner v2 — 安全执行器
吸收自: Python concurrent.futures + retry/backoff模式
纯标准库
"""
from __future__ import annotations
import time
import random
import threading
import traceback as tb
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any, Callable, List, Tuple

from v5_result_monad import Result


class SafeRunner:
    """安全执行器v2 — 重试+超时+熔断+批量"""
    
    def __init__(self, default_retries: int = 3, default_timeout: float = 30.0):
        self.default_retries = default_retries
        self.default_timeout = default_timeout
        self._executor = ThreadPoolExecutor(max_workers=4)
        self._circuit_breakers: dict[str, dict] = {}
        self._stats: dict[str, dict] = {}
    
    def run(
        self,
        func: Callable,
        *args,
        retries: int = None,
        timeout: float = None,
        catch: tuple = (Exception,),
        name: str = None,
        **kwargs
    ) -> Result:
        retries = retries if retries is not None else self.default_retries
        timeout = timeout if timeout is not None else self.default_timeout
        name = name or getattr(func, '__name__', str(func))
        
        # 熔断器检查
        cb = self._circuit_breakers.get(name)
        if cb and cb.get('open', False):
            now = time.time()
            if now - cb.get('opened_at', 0) < cb.get('recovery_timeout', 30):
                return Result.Err(RuntimeError(f"Circuit open: {name}"))
            cb['open'] = False  # half-open
        
        last_error = None
        for attempt in range(retries + 1):
            try:
                if timeout and timeout > 0:
                    fut = self._executor.submit(func, *args, **kwargs)
                    value = fut.result(timeout=timeout)
                else:
                    value = func(*args, **kwargs)
                
                self._update_stats(name, True)
                return Result.Ok(value)
            
            except Exception as e:
                last_error = e
                if attempt < retries:
                    delay = min(0.5 * (2 ** attempt), 30.0)
                    jitter = random.uniform(0, delay * 0.1)
                    time.sleep(delay + jitter)
                else:
                    self._update_stats(name, False)
        
        return Result.Err(last_error)
    
    def run_async(self, func: Callable, *args, **kwargs) -> Future:
        return self._executor.submit(lambda: self.run(func, *args, **kwargs))
    
    def batch_run(self, funcs: List[Tuple[Callable, tuple, dict]], max_workers: int = 4) -> List[Result]:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.run, func, *a, **kw) for func, a, kw in funcs]
            return [f.result() for f in futures]
    
    def with_sandbox(self, func: Callable, *args, **kwargs) -> Result:
        try:
            result = [None]
            error = [None]
            done = threading.Event()
            
            def sandboxed():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    error[0] = e
                finally:
                    done.set()
            
            t = threading.Thread(target=sandboxed, daemon=True)
            t.start()
            done.wait(timeout=self.default_timeout)
            
            if error[0]:
                return Result.Err(error[0])
            if not done.is_set():
                return Result.Err(TimeoutError("Sandbox timeout"))
            return Result.Ok(result[0])
        except Exception as e:
            return Result.Err(e)
    
    def circuit_breaker(self, name: str, failure_threshold: int = 5, recovery_timeout: float = 30.0):
        self._circuit_breakers[name] = {
            'failure_threshold': failure_threshold,
            'recovery_timeout': recovery_timeout,
            'open': False,
            'opened_at': 0,
            'failure_count': 0,
        }
        return self
    
    def _update_stats(self, name: str, success: bool):
        if name not in self._stats:
            self._stats[name] = {'ok': 0, 'fail': 0}
        self._stats[name]['ok' if success else 'fail'] += 1
        
        cb = self._circuit_breakers.get(name)
        if cb:
            if success:
                cb['failure_count'] = 0
                cb['open'] = False
            else:
                cb['failure_count'] = cb.get('failure_count', 0) + 1
                if cb['failure_count'] >= cb['failure_threshold']:
                    cb['open'] = True
                    cb['opened_at'] = time.time()
    
    def statistics(self) -> dict:
        return dict(self._stats)
    
    def shutdown(self, wait: bool = True):
        self._executor.shutdown(wait=wait)


def ensure(fn: Callable, default=None, retries: int = 2):
    """便捷函数: 执行并安全返回"""
    runner = SafeRunner(default_retries=retries)
    r = runner.run(fn)
    return r.unwrap_or(default)
