"""PRDQueue SDK 使用示例"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from igp_sdk.prd import PRDQueue
q = PRDQueue(".")
prd = q.submit(department="market", product="BugDoctor",
               title="需要TypeScript支持", priority="high")
print(f"PRD: {prd['id']}")
