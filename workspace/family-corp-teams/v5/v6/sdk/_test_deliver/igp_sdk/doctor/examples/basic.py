"""BugDoctor SDK 使用示例"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from igp_sdk.doctor import BugDoctor
d = BugDoctor()
d.scan_directory(".")
report = d.get_report()
print(f"Found {len(report)} issues")
