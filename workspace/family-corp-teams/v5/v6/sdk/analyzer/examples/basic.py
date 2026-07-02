"""CodeAnalyzer SDK 使用示例"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from igp_sdk.analyzer import CodeAnalyzer
ca = CodeAnalyzer(".")
ca.scan_refactoring()
ca.scan_bad_patterns()
ca.scan_mutation_opportunity()
print(ca.report())
