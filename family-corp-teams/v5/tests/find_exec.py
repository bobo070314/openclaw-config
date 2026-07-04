"""Find exec calls in v5_job_engine.py"""
import ast

path = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\absorb\docagent\v5_job_engine.py'
src = open(path, 'r', encoding='utf-8').read()
tree = ast.parse(src)

for n in ast.walk(tree):
    if isinstance(n, ast.Call):
        func = getattr(n, 'func', None)
        if func:
            name = getattr(func, 'id', None) or getattr(func, 'attr', None)
            if name and 'exec' in name.lower():
                lineno = getattr(n, 'lineno', '?')
                for kid in ast.walk(n):
                    if isinstance(kid, ast.Constant) and isinstance(kid.value, str) and len(kid.value) > 20:
                        # Check for bad escapes
                        import re
                        bads = re.findall(r"(?<![rR])['\"]\S*\\[wWsSdDo]", kid.value)
                        if bads:
                            print(f"Line {lineno}: exec with bad escapes: {bads}")
                            print(f"  snippet: {kid.value[:100]}")
                        else:
                            print(f"Line {lineno}: exec call (no bad escapes found in first 100)")
