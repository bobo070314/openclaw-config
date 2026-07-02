"""
IGP SmartRouter v2 — 智能路由
吸收自: 负载均衡 + 熔断器 + 灰度发布模式
纯标准库
"""
from __future__ import annotations
import time
import random
from collections import defaultdict, deque
from typing import Any, Dict, List, Optional, Tuple


class SmartRouter:
    """智能路由v2 — 4种策略 + 熔断器 + A/B + 灰度"""
    
    WEIGHTED = 'weighted'
    LRU = 'lru'
    LEAST = 'least_connections'
    RANDOM = 'random'
    
    def __init__(self, name: str = 'default'):
        self.name = name
        self._providers: Dict[str, dict] = {}
        self._connections: Dict[str, int] = defaultdict(int)
        self._lru_order: deque = deque()
        self._circuits: Dict[str, dict] = {}
        self._stats: Dict[str, dict] = {}
    
    def register(self, name: str, provider: Any, weight: float = 1.0, **meta) -> 'SmartRouter':
        self._providers[name] = {
            'name': name, 'provider': provider,
            'weight': max(0.1, weight), 'meta': meta,
            'healthy': True,
        }
        self._lru_order.append(name)
        if name not in self._stats:
            self._stats[name] = {'hits': 0, 'errors': 0, 'total_time': 0.0}
        return self
    
    def unregister(self, name: str) -> bool:
        return self._providers.pop(name, None) is not None
    
    def select(self, request: Any = None, strategy: str = 'weighted') -> Optional[Tuple[str, Any]]:
        healthy = [n for n in self._providers if self._check_circuit(n)]
        if not healthy:
            return None
        
        if strategy == self.WEIGHTED:
            return self._weighted(healthy)
        elif strategy == self.LRU:
            return self._lru(healthy)
        elif strategy == self.LEAST:
            return self._least_conn(healthy)
        else:  # RANDOM
            name = random.choice(healthy)
            return (name, self._providers[name]['provider'])
    
    def route(self, request: Any = None, strategy: str = 'weighted') -> Any:
        sel = self.select(request, strategy)
        return sel[1] if sel else None
    
    def circuit_breaker(self, name: str, threshold: int = 5, timeout: float = 30.0) -> 'SmartRouter':
        self._circuits[name] = {'state': 'closed', 'failures': 0, 'threshold': threshold, 'timeout': timeout, 'opened_at': 0}
        return self
    
    def _check_circuit(self, name: str) -> bool:
        cb = self._circuits.get(name)
        if not cb:
            return True
        if cb['state'] == 'open':
            if time.time() - cb['opened_at'] > cb['timeout']:
                cb['state'] = 'half-open'
                return True
            return False
        return True
    
    def record_success(self, name: str, duration_ms: float = 0):
        self._stats.setdefault(name, {'hits': 0, 'errors': 0, 'total_time': 0.0})
        s = self._stats[name]
        s['hits'] += 1
        s['total_time'] += duration_ms
        cb = self._circuits.get(name)
        if cb:
            cb['failures'] = 0
            cb['state'] = 'closed'
    
    def record_failure(self, name: str):
        self._stats.setdefault(name, {'hits': 0, 'errors': 0, 'total_time': 0.0})
        self._stats[name]['errors'] += 1
        cb = self._circuits.get(name)
        if cb:
            cb['failures'] += 1
            if cb['failures'] >= cb['threshold']:
                cb['state'] = 'open'
                cb['opened_at'] = time.time()
    
    def ab_test(self, variant_a: str, variant_b: str, ratio: float = 0.5) -> Any:
        if random.random() < ratio:
            return self._providers.get(variant_b, {}).get('provider')
        return self._providers.get(variant_a, {}).get('provider')
    
    def canary(self, stable: str, canary: str, ratio: float = 0.1) -> Any:
        return self.ab_test(stable, canary, ratio)
    
    def statistics(self) -> dict:
        return dict(self._stats)
    
    def provider_count(self) -> int:
        return len(self._providers)
    
    def circuit_status(self) -> dict:
        return {k: v['state'] for k, v in self._circuits.items()}
    
    def _weighted(self, healthy: list) -> Tuple[str, Any]:
        total = sum(self._providers[n].get('weight', 1.0) for n in healthy)
        r = random.uniform(0, total)
        upto = 0.0
        for name in healthy:
            upto += self._providers[name].get('weight', 1.0)
            if r <= upto:
                return (name, self._providers[name]['provider'])
        name = healthy[-1]
        return (name, self._providers[name]['provider'])
    
    def _lru(self, healthy: list) -> Tuple[str, Any]:
        for name in list(self._lru_order):
            if name in healthy:
                self._lru_order.remove(name)
                self._lru_order.appendleft(name)
                return (name, self._providers[name]['provider'])
        return self._weighted(healthy)
    
    def _least_conn(self, healthy: list) -> Tuple[str, Any]:
        best = min(healthy, key=lambda n: self._connections[n])
        return (best, self._providers[best]['provider'])
