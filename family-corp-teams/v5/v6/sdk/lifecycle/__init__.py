"""Lifecycle SDK v1.0.0 — 产品生命周期管理：Research→Alpha→Beta→GA→Deprecated→EOL"""
from .source.v6_lifecycle import LifecycleManager
from .version import VERSION, NAME

__all__ = ['LifecycleManager']
