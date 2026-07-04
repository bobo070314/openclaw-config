"""
D2A Server - 本地Agent通信Server
Python 0依赖
"""
import os, json
from datetime import datetime

FAMILY = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams"
PROJECTS = os.path.join(FAMILY, 'projects')

class D2AServer:
    def __init__(self):
        self.agents = {}
    def register(self, name):
        self.agents[name] = {'status': 'idle', 'last_seen': datetime.now().isoformat()[:19]}
        return {'status': 'ok', 'agent': name}
    def handle(self, source, target, action, data):
        if target not in self.agents:
            return {'status': 'error', 'msg': f'target {target} not found'}
        self.agents[target]['status'] = 'busy'
        self.agents[target]['last_seen'] = datetime.now().isoformat()[:19]
        return {'status': 'ok', 'from': source, 'to': target, 'action': action,
                'reply': f'{action} on {target} OK'}

def main():
    print('D2A Server v2\n')
    s = D2AServer()
    depts = ['infra', 'quality', 'frontend', 'backend', 'ai', 'ghost-team', 'data', 'design', 'mobile', 'growth']
    for d in depts:
        s.register(d)
    print(f'  Registered: {len(depts)} agents')
    r = s.handle('HQ', 'ghost-team', 'patrol', {'scope': 'all'})
    print(f'  Test: {r["status"]} - {r["reply"]}')

if __name__ == '__main__':
    main()
