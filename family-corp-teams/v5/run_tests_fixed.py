import os
import sys
import shutil
import subprocess

base = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5"
os.chdir(base)

# Copy silicon_memory to root as a proper package
pkg_dir = os.path.join(base, "silicon_memory_pkg")
if os.path.exists(pkg_dir):
    shutil.rmtree(pkg_dir)
shutil.copytree(os.path.join(base, "v6", "silicon_memory"), pkg_dir)

# Ensure __init__.py exists
init_path = os.path.join(pkg_dir, "__init__.py")
if not os.path.exists(init_path):
    with open(init_path, "w") as f:
        f.write("from .v5_silicon_memory import *\nfrom .v5_silicon_indexer import *\nfrom .v5_silicon_tools import *\n")

sys.path.insert(0, pkg_dir)

result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_silicon_indexer.py", "tests/test_silicon_tools.py", "-v"],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.stderr:
    print(result.stderr)
sys.exit(result.returncode)
