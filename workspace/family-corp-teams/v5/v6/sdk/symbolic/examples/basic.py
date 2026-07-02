"""SymbolicEngine SDK 使用示例"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from igp_sdk.symbolic import SymbolicEngine
se = SymbolicEngine()
se.add_constraint("x > 5")
se.add_constraint("x < 10")
result = se.solve()
print(f"Solution: {result}")
