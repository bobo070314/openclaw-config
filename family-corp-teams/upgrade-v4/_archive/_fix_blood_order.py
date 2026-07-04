#!/usr/bin/env python3
"""修复血液循环函数定义顺序 — 移到__main__之前"""
import re

path = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\igp_engine.py"
with open(path, encoding="utf-8") as f:
    code = f.read()

# 找到 __main__ 保护的位置
main_pos = code.find('\nif __name__ == "__main__":')
if main_pos < 0:
    print("[FAIL] 找不到 __main__")
    exit(1)

# 找文件末尾的血液循环代码
blood_start = code.rfind("\n# ===== 血液循环系统 v2.0 - 血型注册与识别 =====")
blood_end = len(code)

if blood_start < 0:
    print("[FAIL] 找不到血液循环代码")
    exit(1)

# 提取血液循环代码
blood_code = code[blood_start:blood_end]

# 从末尾删除
code = code[:blood_start]

# 插到 __main__ 之前（但保留 __main__ 之前的空行/注释）
# 去掉main_pos前面可能有的尾部空白，插在这里
insert_pos = code.rfind("\n\n", 0, main_pos) + 2  # 保留两个换行

code = code[:insert_pos] + "\n" + blood_code + "\n" + code[insert_pos:]

try:
    compile(code, path, "exec")
    print("[OK] 编译通过")
except SyntaxError as e:
    print(f"[FAIL] 编译失败 line {e.lineno}: {e.msg}")
    lines = code.splitlines()
    for i in range(max(0, e.lineno-3), min(len(lines), e.lineno+2)):
        print(f"  {i+1}: {lines[i][:120]}")
    exit(1)

with open(path, "w", encoding="utf-8") as f:
    f.write(code)
print("[OK] 写入成功 - 血液循环代码已移到__main__前")
