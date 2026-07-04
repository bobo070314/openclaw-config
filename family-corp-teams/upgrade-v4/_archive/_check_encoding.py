#!/usr/bin/env python3
"""检查python环境和编码问题"""
import os, subprocess, sys

print("=== Python info ===")
print(f"Python: {sys.version}")
print(f"PYTHONIOENCODING: {os.environ.get('PYTHONIOENCODING', 'NOT SET')}")
print(f"PYTHONUTF8: {os.environ.get('PYTHONUTF8', 'NOT SET')}")
print(f"Encoding default: {sys.getdefaultencoding()}")
print(f"Encoding stdout: {sys.stdout.encoding}")
print(f"Encoding stderr: {sys.stderr.encoding}")

print("\n=== Test: 写中文文件 ===")
test_path = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\upgrade-v4\_test_encoding.txt"
with open(test_path, "w", encoding="utf-8") as f:
    f.write("中文测试 ✅ 42Team集体研究突破\n")
print(f"[OK] 写入成功: {test_path}")

print("\n=== Test: 读中文文件 ===")
with open(test_path, encoding="utf-8") as f:
    content = f.read()
print(f"[OK] 读取成功: {content}")

print("\n=== Done ===")
