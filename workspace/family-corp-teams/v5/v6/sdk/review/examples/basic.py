"""ReviewAgents SDK 使用示例"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from igp_sdk.review import review_file
result = review_file("module.py")
print(f"Score: {result['total_score']}/30 {'PASS' if result['passed'] else 'FAIL'}")
