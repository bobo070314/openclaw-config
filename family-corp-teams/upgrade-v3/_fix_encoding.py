"""修复igp_engine.py中所有 GBK open() 问题"""
p = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\igp_engine.py"
content = open(p, encoding="utf-8").read()

patches = [
    ('with open(tickets_file, "w") as f:\n        json.dump(tickets, f, indent=2, ensure_ascii=False)\n    \n    print(f"🎫 [', 'with open(tickets_file, "w", encoding="utf-8") as f:\n        json.dump(tickets, f, indent=2, ensure_ascii=False)\n    \n    print(f"[{ticket_id}] 新工单 '),
]

# 替换1: dispatch_ticket读
content = content.replace(
    'def dispatch_ticket(ticket_id):\n    tickets_file = TEAMS_DIR / "pending_tickets.json"\n    with open(tickets_file) as f:',
    'def dispatch_ticket(ticket_id):\n    tickets_file = TEAMS_DIR / "pending_tickets.json"\n    with open(tickets_file, encoding="utf-8") as f:'
)

# 替换2: dispatch_ticket写
content = content.replace(
    '        json.dump(tickets, f, indent=2, ensure_ascii=False)\n    print(f"📦 [{ticket_id}] 已派发 ',
    '        json.dump(tickets, f, indent=2, ensure_ascii=False)\n    print(f"[{ticket_id}] 已派发 '
)

# 替换3: fast_review读
content = content.replace(
    'def fast_review(ticket_id):\n    """快速评审一个工单"""\n    data = load_evolution_data()\n    tickets_file = TEAMS_DIR / "pending_tickets.json"\n    with open(tickets_file) as f:',
    'def fast_review(ticket_id):\n    """快速评审一个工单"""\n    data = load_evolution_data()\n    tickets_file = TEAMS_DIR / "pending_tickets.json"\n    with open(tickets_file, encoding="utf-8") as f:'
)

# 替换4: fast_review写
content = content.replace(
    '    with open(tickets_file, "w") as f:\n        json.dump(tickets, f, indent=2, ensure_ascii=False)\n    \n    # ⚠️ 检查败者是否需要淘汰',
    '    with open(tickets_file, "w", encoding="utf-8") as f:\n        json.dump(tickets, f, indent=2, ensure_ascii=False)\n    \n    #'
)

# 替换5: create_ticket写+print
content = content.replace(
    '    with open(tickets_file, "w") as f:\n        json.dump(tickets, f, indent=2, ensure_ascii=False)\n    \n    print(f"🎫',
    '    with open(tickets_file, "w", encoding="utf-8") as f:\n        json.dump(tickets, f, indent=2, ensure_ascii=False)\n    \n    print(f"['
)

open(p, "w", encoding="utf-8").write(content)
print("Done: encoding patches applied")
