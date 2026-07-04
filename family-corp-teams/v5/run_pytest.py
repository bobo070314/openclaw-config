import os
import sys
import subprocess

os.chdir(r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5")
env = os.environ.copy()
env["PYTHONPATH"] = r"v6\silicon_memory"

result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_silicon_indexer.py", "tests/test_silicon_tools.py", "-v"],
    env=env,
    capture_output=True,
    text=True
)
print(result.stdout)
if result.stderr:
    print(result.stderr)
sys.exit(result.returncode)
