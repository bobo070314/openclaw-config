"""
IGP Design - ASCII视觉方案
控制台UI / 排行榜 / 进度条
"""
import os

def progress_bar(c, t, w=30):
    f = int(w * c / t) if t else 0
    bar = chr(9608) * f + chr(9617) * (w - f)
    return f'[{bar}] {c}/{t}'

def rank_bar(n, s, ms=200, w=40):
    f = int(w * s / ms)
    bar = chr(9608) * f + ' ' * (w - f)
    return f'{n:18s} |{bar}| {s:3d}'

def main():
    print('IGP Design System\n')
    print('Progress Bar Test:')
    for i in range(0, 101, 25):
        print(f'  {progress_bar(i, 100)}')
    print('\nRank Bar Test:')
    scores = [('DocMind', 168), ('Ghost', 105), ('D2A', 42), ('Evolver', 30)]
    for n, s in scores:
        print(f'  {rank_bar(n, s)}')

if __name__ == '__main__':
    main()
