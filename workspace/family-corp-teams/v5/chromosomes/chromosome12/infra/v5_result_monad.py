"""
IGP Result Monad — Ok/Err模式
吸收自: Rust std::result monad
纯标准库
"""
from __future__ import annotations
from typing import Any, Callable, Generic, Iterator, Optional, TypeVar

T = TypeVar('T')
E = TypeVar('E')
U = TypeVar('U')


class Result(Generic[T, E]):
    """Result[T, E] — 显式成功/失败"""
    
    __slots__ = ('_ok', '_value', '_error', '_trace')
    
    def __init__(self, ok: bool, value: T = None, error: E = None):
        self._ok = ok
        self._value = value
        self._error = error
        self._trace = None if ok else []
    
    @classmethod
    def Ok(cls, value: T = None) -> 'Result[T, Any]':
        return cls(True, value)
    
    @classmethod
    def Err(cls, error: E = None) -> 'Result[Any, E]':
        return cls(False, error=error)
    
    def is_ok(self) -> bool:
        return self._ok
    
    def is_err(self) -> bool:
        return not self._ok
    
    def unwrap(self) -> T:
        if self._ok:
            return self._value
        raise RuntimeError(f"Unwrap failed: {self._error}")
    
    def unwrap_or(self, default: U) -> T | U:
        return self._value if self._ok else default
    
    def unwrap_or_else(self, fn: Callable[[E], T]) -> T:
        return self._value if self._ok else fn(self._error)
    
    def expect(self, msg: str) -> T:
        if self._ok:
            return self._value
        raise RuntimeError(f"{msg}: {self._error}")
    
    def map(self, fn: Callable[[T], U]) -> 'Result[U, E]':
        if self._ok:
            try:
                return Result.Ok(fn(self._value))
            except Exception as e:
                return Result.Err(e)
        return Result.Err(self._error)
    
    def bind(self, fn: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        """flat_map"""
        if self._ok:
            try:
                return fn(self._value)
            except Exception as e:
                return Result.Err(e)
        return Result.Err(self._error)
    
    def ok(self) -> Optional[T]:
        return self._value if self._ok else None
    
    def err(self) -> Optional[E]:
        return self._error if not self._ok else None
    
    def __repr__(self) -> str:
        if self._ok:
            return f"Ok({self._value!r})"
        return f"Err({self._error!r})"
    
    def __bool__(self) -> bool:
        return self._ok
    
    def __iter__(self) -> Iterator[T]:
        if self._ok:
            yield self._value
    
    def to_dict(self) -> dict:
        return {
            'ok': self._ok,
            'value': self._value,
            'error': str(self._error) if self._error else None,
        }
