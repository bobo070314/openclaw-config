"""CodeAnalyzer SDK v1.0.0 — 代码质量分析：死代码检测/重构机会/不良模式/杂交机会"""
from .source.v5_code_analyzer import CodeAnalyzer
from .version import VERSION, NAME

__all__ = ['CodeAnalyzer']
