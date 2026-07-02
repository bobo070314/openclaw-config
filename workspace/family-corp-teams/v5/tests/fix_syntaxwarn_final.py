"""Find SyntaxWarning lines in v5_job_engine.py"""
import re

path = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\absorb\docagent\v5_job_engine.py'
src = open(path, 'r', encoding='utf-8').read()
lines = src.split('\n')

# Python 3.14+ 会在非raw字符串中出现\\w \\S 等时抛出SyntaxWarning
# 检测：在常规字符串(非raw)中，有 \w \S \d 等
# raw字符串特征: r'...' r"..."
hits = []
for i, line in enumerate(lines):
    s = line.strip()
    # 跳过注释
    if s.startswith('#'):
        continue
    
    # 查找非raw字符串中的无效转义
    in_string = False
    string_char = None
    raw = False
    j = 0
    while j < len(s):
        c = s[j]
        if not in_string:
            if c in ("'", '"'):
                in_string = True
                string_char = c
                raw = j > 0 and s[j-1] in ('r', 'R')
            j += 1
        elif c == string_char and (j == 0 or s[j-1] != '\\'):
            in_string = False
            j += 1
        elif c == '\\' and not raw and j < len(s) - 1:
            next_c = s[j+1]
            if next_c in ('w', 'W', 's', 'S', 'd', 'D', 'o'):
                # 确认是在字符串内部
                hits.append((i + 1, s))
                break
            j += 2
        else:
            j += 1

print(f"Found {len(hits)} SyntaxWarning lines:")
for lno, txt in hits:
    print(f"  L{lno}: {txt[:100]}")

# 修复: 在字符串前加 r
if hits:
    fixed = []
    for line in lines:
        s = line.strip()
        # 跳过注释行
        if not s or s.startswith('#'):
            fixed.append(line)
            continue
        
        needs_fix = False
        new_line = line
        
        # 对每个命中行，找到字符串前缀加r
        # 简单策略：替换 "\\S" -> "\\\\S", "\\w" -> "\\\\w"
        for bad in ['\\w', '\\W', '\\s', '\\S', '\\d', '\\D', '\\o']:
            # 只替换在字符串引号内的，且非raw字符串
            # 安全做法：全局替换 \\S -> \\\\S (双反斜杠)
            new_line = new_line.replace(bad, '\\' + bad)
        
        if new_line != line:
            needs_fix = True
            fixed.append(new_line)
        else:
            fixed.append(line)
    
    src2 = '\n'.join(fixed)
    open(path, 'w', encoding='utf-8').write(src2)
    print(f"\nFixed {sum(1 for i in range(len(lines)) if fixed[i] != lines[i])} lines")
else:
    print("No SyntaxWarning found")
