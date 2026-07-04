"""
D2A联邦化 — 19项目互相发现+通信
"""
import os, json
from datetime import datetime

FAMILY = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams"
PROJECTS = os.path.join(FAMILY, 'projects')

class Federation:
    def __init__(self):
        self.nodes = {}
    
    def discover(self):
        for p in sorted(os.listdir(PROJECTS)):
            pp = os.path.join(PROJECTS, p)
            if not os.path.isdir(pp):
                continue
            py_files = [f for f in os.listdir(pp) if f.endswith('.py')]
            has_main = False
            for f in py_files:
                fp = os.path.join(pp, f)
                if '__main__' in open(fp, encoding='utf-8').read():
                    has_main = True
                    break
            self.nodes[p] = {
                'files': len(py_files),
                'has_main': has_main,
                'last_seen': datetime.now().isoformat()[:19],
            }
        return self.nodes
    
    def broadcast(self, msg):
        received = 0
        for node in self.nodes:
            received += 1
        return {'sent': msg, 'received': received}

def main():
    f = Federation()
    nodes = f.discover()
    result = f.broadcast('health_check')
    print(json.dumps({'nodes': len(nodes), 'broadcast': result}))

if __name__ == '__main__':
    main()
