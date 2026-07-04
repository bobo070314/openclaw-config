"""
IGP Data - 数据看板
JSON to ASCII可视化
"""
import os, json
from datetime import datetime

FAMILY = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams"

def patrol_report():
    log = os.path.join(FAMILY, 'projects', 'igp-ghost', 'patrol_log.json')
    if not os.path.exists(log):
        return 'No patrol data'
    data = json.load(open(log, encoding='utf-8'))
    if data:
        last = data[-1]
        return f'{last.get("type","?")} | issues:{last.get("total_issues",0)}'
    return 'Empty logs'

def main():
    print('IGP Data Dashboard\n')
    print(f'  Last patrol: {patrol_report()}')
    print(f'  Timestamp: {datetime.now().strftime("%H:%M:%S")}')
    print('\n  Data Dashboard OK')

if __name__ == '__main__':
    main()
