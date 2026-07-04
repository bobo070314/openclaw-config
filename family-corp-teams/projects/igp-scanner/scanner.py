"""
IGP生态扫描器 — 自动检测可吸收项目
基于词频分析IGP项目差异
"""
import os, sys, json, re
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'

def scan_ecosystem():
    profiles = {}
    for p in sorted(os.listdir(os.path.join(FAMILY, 'projects'))):
        pp = os.path.join(FAMILY, 'projects', p)
        if not os.path.isdir(pp):
            continue
        py_files = [f for f in os.listdir(pp) if f.endswith('.py')]
        if not py_files:
            continue
        text = ''
        for f in py_files:
            text += open(os.path.join(pp, f), encoding='utf-8').read() + '\n'
        
        words = re.findall(r'[a-zA-Z\u4e00-\u9fff]{2,}', text.lower())
        freq = {}
        for w in words:
            if len(w) >= 3:
                freq[w] = freq.get(w, 0) + 1
        
        profiles[p] = {
            'words': len(words),
            'unique': len(freq),
            'top_words': sorted(freq.items(), key=lambda x: -x[1])[:5],
        }
    return profiles

def main():
    print('IGP生态扫描器\n')
    profiles = scan_ecosystem()
    for p, info in sorted(profiles.items()):
        tops = ', '.join(f'{w}({c})' for w, c in info['top_words'])
        print(f'  {p:18s} | {info["words"]}词/{info["unique"]}唯一 | {tops}')
    print(f'\n  扫描完成: {len(profiles)}个项目')
    
    # 保存
    with open(os.path.join(FAMILY, 'headquarters', 'eco_scan.json'), 'w') as f:
        json.dump({'scanned_at': datetime.now().isoformat()[:19], 'projects': list(profiles.keys())}, f)

if __name__ == '__main__':
    main()
