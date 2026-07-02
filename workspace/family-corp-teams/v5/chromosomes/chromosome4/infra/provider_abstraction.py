"""
染色体4 Provider抽象 — 填充空方法
升级: chat/embed/invoke空 → 真实实现
"""
from __future__ import annotations
from typing import Any, Dict, List


class ProviderAbstraction:
    """Provider抽象层 — 统一调用/嵌入/调用接口"""
    
    def __init__(self, name: str = 'default'):
        self.name = name
        self._models: Dict[str, Any] = {}
    
    def add_model(self, name: str, handler) -> 'ProviderAbstraction':
        self._models[name] = handler
        return self
    
    def chat(self, model: str, messages: List[Dict], **kwargs) -> Dict:
        """通用对话调用 — 代理到具体Provider"""
        handler = self._models.get(model)
        if handler is None:
            return {
                'error': f'Model {model} not found',
                'available': list(self._models.keys()),
            }
        if callable(handler):
            return handler(messages, **kwargs)
        return {'error': f'Handler for {model} is not callable'}
    
    def embed(self, model: str, texts: List[str]) -> List[List[float]]:
        """通用嵌入调用"""
        handler = self._models.get(model)
        if handler is None:
            return [[0.0] * 384 for _ in texts]
        if callable(handler):
            result = handler(texts)
            if isinstance(result, list):
                return result
        return [[0.0] * 384 for _ in texts]
    
    def invoke(self, model: str, fn_name: str, args: Dict = None) -> Any:
        """通用函数调用"""
        handler = self._models.get(model)
        if handler is None:
            return None
        if hasattr(handler, fn_name):
            return getattr(handler, fn_name)(**(args or {}))
        return None
    
    def list_models(self) -> List[str]:
        return list(self._models.keys())
