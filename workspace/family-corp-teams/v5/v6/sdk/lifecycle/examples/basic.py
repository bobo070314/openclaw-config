"""Lifecycle SDK 使用示例"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from igp_sdk.lifecycle import LifecycleManager
lm = LifecycleManager("product_registry.json")
s = lm.summary()
print(f"Total products: {s['total']}")
