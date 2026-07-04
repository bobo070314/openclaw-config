import os
import subprocess
import sys
import pathlib
from test_runner import TestRunner

# 配置
CODE_FILE = "D:/bobo/openclaw-foreign/workspace/family-corp-teams/upgrade-v3/igp_mcp_bridge.py"
TEST_FILE = CODE_FILE.replace(".py", "_test.py")

# 初始化测试运行器
runner = TestRunner()

# 生成测试
print("\n=== 生成测试 ===")
runner.generate_tests(CODE_FILE)

# 运行测试
print("\n=== 运行测试 ===")
result = subprocess.run(["pytest", TEST_FILE, "-v", "--tb=short"],
                        capture_output=True, text=True, timeout=30,
                        encoding="utf-8", errors="replace")

# 输出结果
print("\n=== 测试结果 ===")
print(f"测试文件: {TEST_FILE}")
print(f"通过: {'passed' in result.stdout or 'PASSED' in result.stdout}")
print(f"输出: {result.stdout[-500:]}" )