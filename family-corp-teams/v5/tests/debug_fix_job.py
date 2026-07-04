"""Debug why generate_report gets SyntaxWarning"""
import sys, os

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
sys.path.insert(0, V5)
sys.path.insert(0, os.path.join(V5, 'absorb', 'docagent'))
sys.path.insert(0, os.path.join(V5, 'absorb'))
sys.path.insert(0, os.path.join(V5, 'v6'))
sys.path.insert(0, os.path.join(V5, 'v6', 'hr'))

# 模拟generate_report的try块
try:
    from v5_job_engine import JobEngine
    print(f"import ok: {JobEngine}")
except ImportError as e:
    print(f"import failed: {e}")
except Exception as e:
    print(f"other error: {e}")

# 检查v5_job_engine.py的模块内容
import v5_job_engine
print(f"dir: {[n for n in dir(v5_job_engine) if not n.startswith('_')]}")
