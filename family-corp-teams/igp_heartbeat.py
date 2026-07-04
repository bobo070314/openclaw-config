import json
import os

# 检查 pending_tickets.json 中的活跃工单
pending_tickets_path = 'pending_tickets.json'

if os.path.exists(pending_tickets_path):
    with open(pending_tickets_path, 'r', encoding='utf-8') as f:
        tickets = json.load(f)
        active_tickets = [t for t in tickets if t['status'] == 'active']
        print(f'活跃工单数量: {len(active_tickets)}')
else:
    print('没有找到 pending_tickets.json 文件')