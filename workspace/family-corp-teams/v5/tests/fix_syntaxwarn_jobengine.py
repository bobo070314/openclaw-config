"""修复 v5_job_engine.py 的 SyntaxWarning"""
import re

path = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\absorb\docagent\v5_job_engine.py'
src = open(path, 'r', encoding='utf-8').read()

# 找到所有非raw字符串中的无效转义
lines = src.split('\n')
bad_lines = []
for i, line in enumerate(lines):
    stripped = line.strip()
    # 检查是否在字符串内且有 \w \S \d \o 等无效转义
    # 非 raw 字符串 (以 ' 或 " 开头但不是 r' 或 r")
    in_string = False
    string_char = None
    raw = False
    j = 0
    while j < len(stripped):
        c = stripped[j]
        if not in_string:
            if c in ("'", '"'):
                in_string = True
                string_char = c
                raw = j > 0 and stripped[j-1] in ('r', 'R')
        elif c == string_char and (j == 0 or stripped[j-1] != '\\'):
            in_string = False
        elif c == '\\' and not raw and j < len(stripped) - 1:
            next_c = stripped[j+1]
            if next_c in ('w', 'S', 'D', 'o', 's'):
                bad_lines.append((i, stripped))
                break
        j += 1

# 全局替换
replacements = [('\\w', '\\\\w'), ('\\S', '\\\\S'), ('\\d', '\\\\d'), ('\\o', '\\\\o'), ('\\D', '\\\\D')]
for bad, good in replacements:
    src = src.replace(bad, good)

open(path, 'w', encoding='utf-8').write(src)
print(f"Fixed {len(bad_lines)} lines with invalid escape sequences")
for li, line in bad_lines:
    print(f"  L{li+1}: {line[:60]}")
