"""Debug complexity test"""
import sys, os
V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
sys.path.insert(0, os.path.join(V5, 'chromosomes', 'chromosome11', 'infra'))
from v5_complexity_analyzer import ComplexityAnalyzer
ca = ComplexityAnalyzer()
result = ca.analyze_file(__file__)
print(f"type: {type(result).__name__}")
print(f"keys: {list(result.keys())}")
print(f"result: {result}")
