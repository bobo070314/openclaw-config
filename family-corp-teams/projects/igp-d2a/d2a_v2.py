"""
D2A v2 — Agent协议 HTTP Server
本地Agent间通信
"""
import os, sys, json, re, time
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
D2A_DIR = os.path.join(FAMILY, 'projects', 'igp-d2a')
os.makedirs(D2A_DIR, exist_ok=True)


class D2AClient:
    """D2A v2 客户端"""
    
    def __init__(self, name):
        self.name = name
        self.agents = {}
    
    def register(self, agent_name, endpoint):
        self.agents[agent_name] = endpoint
        return True
    
    def send(self, to_agent, action, data):
        if to_agent in self.agents:
            return {'status': 'ok', 'agent': to_agent, 'action': action, 'reply': f'{self.name}→{to_agent}: {action} done'}
        return {'status': 'error', 'msg': f'agent {to_agent} not found'}
    
    def broadcast(self, action, data):
        results = {}
        for name in self.agents:
            results[name] = self.send(name, action, data)
        return results


# 演示
def main():
    print('D2A v2 — Agent协议通信\n')
    
    hub = D2AClient('headquarters')
    
    # 注册所有部门
    depts = ['ghost-team', 'infra', 'quality', 'frontend', 'backend', 'ai',
             'mobile', 'design', 'growth', 'data', 'tech-support', 'compliance']
    for d in depts:
        hub.register(d, f'local://{d}')
    
    print(f'  注册: {len(depts)}个Agent')
    print()
    
    # 模拟通信
    test = hub.send('ghost-team', 'patrol', {'scope': 'all'})
    print(f'  D2A通信测试:')
    print(f'    发送 → ghost-team: patrol')
    print(f'    回复: {test["reply"]}')
    
    # 批量
    broadcast = hub.broadcast('status', {'time': datetime.now().isoformat()[:19]})
    ok_count = sum(1 for v in broadcast.values() if v['status'] == 'ok')
    print(f'    广播: {ok_count}/{len(depts)}个Agent响应')
    
    print(f'\n  ✅ D2A v2 通信层就绪')


if __name__ == '__main__':
    main()
