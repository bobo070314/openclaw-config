"""ComplexityAnalyzer SDK 使用示例"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from igp_sdk.complexity import ComplexityAnalyzer
ca = ComplexityAnalyzer()
result = ca.analyze_file("module.py")
print(f"Score: {result.get('score')}")
