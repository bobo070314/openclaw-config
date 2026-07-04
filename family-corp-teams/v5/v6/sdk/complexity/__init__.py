"""ComplexityAnalyzer SDK v1.0.0 — 圈复杂度/认知复杂度度量，支持单个文件和目录批量分析"""
from .source.v5_complexity_analyzer import ComplexityAnalyzer
from .version import VERSION, NAME

__all__ = ['ComplexityAnalyzer']
