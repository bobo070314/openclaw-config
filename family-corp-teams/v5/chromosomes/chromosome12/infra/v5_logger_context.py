"""
IGP LoggerContext — 结构化日志上下文
吸收自: structlog的context binding设计
纯标准库
"""
from __future__ import annotations
import logging
import json
import sys as _sys
import os as _os
import traceback as _tb
from typing import Any, Dict
from datetime import datetime, timezone


class LoggerContext:
    """上下文日志器 — bind/unbind/with_context/json_output/auto_caller"""
    
    _instances: Dict[str, 'LoggerContext'] = {}
    _global_bindings: Dict[str, Any] = {}
    _json_mode: bool = False
    
    def __init__(self, name: str, ctx: Dict[str, Any] = None):
        self._name = name
        self._ctx = ctx or {}
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)
        if not self._logger.handlers:
            handler = logging.StreamHandler(_sys.stderr)
            handler.setFormatter(logging.Formatter('%(message)s'))
            self._logger.addHandler(handler)
    
    @classmethod
    def get(cls, name: str = None) -> 'LoggerContext':
        if name is None:
            name = cls._caller_module()
        if name not in cls._instances:
            cls._instances[name] = cls(name, dict(cls._global_bindings))
        return cls._instances[name]
    
    def bind(self, **ctx: Any) -> 'LoggerContext':
        new_ctx = dict(self._ctx)
        new_ctx.update(ctx)
        return LoggerContext(self._name, new_ctx)
    
    def unbind(self, *keys: str) -> 'LoggerContext':
        new_ctx = dict(self._ctx)
        for key in keys:
            new_ctx.pop(key, None)
        return LoggerContext(self._name, new_ctx)
    
    def with_context(self, **ctx: Any) -> 'LoggerContext':
        return self.bind(**ctx)
    
    @classmethod
    def bind_global(cls, **ctx: Any):
        cls._global_bindings.update(ctx)
        for inst in cls._instances.values():
            inst._ctx.update(ctx)
    
    @classmethod
    def json_output(cls, enabled: bool = True):
        cls._json_mode = enabled
    
    @classmethod
    def set_level(cls, level: str):
        cls._min_level = getattr(logging, level.upper(), logging.DEBUG)
        for inst in cls._instances.values():
            inst._logger.setLevel(cls._min_level)
    
    def _log(self, level: int, msg: str, **extra: Any):
        try:
            data = {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'level': logging.getLevelName(level),
                'logger': self._name,
                'caller': self._caller_info(),
                'message': msg,
            }
            data.update(self._ctx)
            data.update(extra)
            
            if self._json_mode:
                text = json.dumps(data, ensure_ascii=False, default=str)
            else:
                ctx_str = ' '.join(f'{k}={v!r}' for k, v in self._ctx.items())
                extra_str = ' '.join(f'{k}={v!r}' for k, v in extra.items())
                parts = [f'[{data["level"]:>7}]', data["caller"], msg]
                if ctx_str:
                    parts.append(f'({ctx_str})')
                if extra_str:
                    parts.append(f'[{extra_str}]')
                text = ' '.join(parts)
            
            self._logger.handle(logging.LogRecord(
                self._name, level, '', 0, text, (), None
            ))
        except Exception:
            pass
    
    def debug(self, msg: str, **extra):
        self._log(logging.DEBUG, msg, **extra)
    
    def info(self, msg: str, **extra):
        self._log(logging.INFO, msg, **extra)
    
    def warning(self, msg: str, **extra):
        self._log(logging.WARNING, msg, **extra)
    
    def error(self, msg: str, **extra):
        self._log(logging.ERROR, msg, **extra)
    
    def exception(self, msg: str, **extra):
        extra['traceback'] = _tb.format_exc()
        self._log(logging.ERROR, msg, **extra)
    
    @staticmethod
    def _caller_info() -> str:
        for frame in _tb.extract_stack():
            fn = _os.path.basename(frame.filename)
            if fn not in ('v5_logger_context.py', '__init__.py'):
                return f'{fn}:{frame.lineno}'
        return '?:?'
    
    @staticmethod
    def _caller_module() -> str:
        import inspect
        for frame_info in inspect.stack():
            fn = _os.path.basename(frame_info.filename)
            if fn not in ('v5_logger_context.py', '__init__.py', 'threading.py'):
                return fn.replace('.py', '')
        return 'unknown'


# 根日志器
root = LoggerContext.get('igp')
