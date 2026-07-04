import re
path = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\upgrade-v4\_v4_absorb_and_upgrade.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 找到所有f-string里有emoji的替换掉
content = re.sub(r'print\(f\\s*\\S', 'print(f"', content)

# 具体修复已知行
content = content.replace('print(f"  ✅ 生成成功', 'print(f"  [OK] 生成成功')
content = content.replace('print(f"  ❌ 格式不对，尝试提取...")', '')
content = content.replace('print(f  ❌ 格式不对，尝试提取...")', '')
content = content.replace('print(f"  ❌ 提取失败")', 'print("  [FAIL] 提取失败")')
content = content.replace('print(f  ❌ 提取失败")', '')
content = content.replace('print(f ❌ Error: {e}")', 'print(f"  [ERR] {e}")')
content = content.replace('print(f"  ❌ Error: {e}")', 'print(f"  [ERR] {e}")')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed all emoji in f-strings")
