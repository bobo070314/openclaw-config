'''v5_contract_decorators.py - Contract programming decorators inspired by deal'''

from typing import Callable, Dict, Any

def pre_condition(condition: Callable[[Any], bool]) -> Callable:
    """Decorator to enforce a pre-condition"""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            if not condition(*args, **kwargs):
                raise ValueError(f"Pre-condition failed for {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def post_condition(condition: Callable[[Any], bool]) -> Callable:
    """Decorator to enforce a post-condition"""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not condition(result):
                raise ValueError(f"Post-condition failed for {func.__name__}")
            return result
        return wrapper
    return decorator

def invariant(condition: Callable[[Any], bool]) -> Callable:
    """Decorator to enforce an invariant"""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            obj = args[0]  # Assume first argument is the object
            if not condition(obj):
                raise ValueError(f"Invariant failed for {func.__name__}")
            result = func(*args, **kwargs)
            if not condition(obj):
                raise ValueError(f"Invariant failed for {func.__name__}")
            return result
        return wrapper
    return decorator