"""
IGP代码质量门禁 — pre-commit检查器
"""
import os, sys, re

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'

def check_file(fp):
    content = open(fp, encoding='utf-8').read()
    lines = content.split('\n')
    issues = []
    
    # 长度
    for i, l in enumerate(lines, 1):
        if len(l) > 200:
            issues.append(f'L{i}: 行过长({len(l)}字)')
    
    # 敏感信息
    patterns = [r'apiKey\s*=\s*["\'](?!\*|os\.)', r'password\s*=\s*["\']',
                r'token\s*=\s*["\'](?!\*|os\.|None)']
    for pat in patterns:
        m = re.search(pat, content, re.IGNORECASE)
        if m:
            issues.append(f'敏感信息泄露: {m.group()[:30]}')
    
    # main入口
    if '__main__' not in content:
        issues.append('缺__main__入口')
    
    return issues

def main():
    print('IGP质量门禁\n')
    total_issues = 0
    checked = 0
    for root, dirs, files in os.walk(os.path.join(FAMILY, 'projects')):
        for f in files:
            if not f.endswith('.py'):
                continue
            fp = os.path.join(root, f)
            issues = check_file(fp)
            if issues:
                rel = os.path.relpath(fp, FAMILY)
                print(f'  ❌ {rel}')
                for i in issues:
                    print(f'     - {i}')
                total_issues += len(issues)
            checked += 1
    print(f'\n  检查完成: {checked}文件 | {total_issues}问题')

if __name__ == '__main__':
    main()
