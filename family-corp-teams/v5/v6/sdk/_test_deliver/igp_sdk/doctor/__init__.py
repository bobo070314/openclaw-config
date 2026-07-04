"""BugDoctor SDK v1.0.0 — 10种bug pattern检测：死锁/竞态/内存泄露/N+1/注入等"""
from .source.v5_bug_doctor import BugDoctor
from .version import VERSION, NAME

__all__ = ['BugDoctor']
