"""
IGP仪表盘 - 实时部门状态
ASCII终端UI 0依赖
"""
import os, json, shutil

FAMILY = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams"
PROJECTS = os.path.join(FAMILY, 'projects')

def render():
    width = min(shutil.get_terminal_size().columns, 60)
    print(chr(61) * width)
    print("  IGP DASHBOARD - Department Status")
    print(chr(61) * width)
    for p in sorted(os.listdir(PROJECTS)):
        pp = os.path.join(PROJECTS, p)
        if not os.path.isdir(pp):
            continue
        py_files = [f for f in os.listdir(pp) if f.endswith('.py')]
        total = sum(len(open(os.path.join(pp, f), encoding='utf-8').read().split(chr(10))) for f in py_files)
        has_m = any('__main__' in open(os.path.join(pp, f), encoding='utf-8').read() for f in py_files)
        status = 'OK' if (has_m and total > 50) else '--'
        bar = chr(9608) * (total // 100)
        print(f"  {status} {p:18s} | {total:>5d}行 {bar}")
    print()

if __name__ == '__main__':
    render()
