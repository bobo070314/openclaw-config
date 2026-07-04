"""
IGP Federation Bridge — 联邦桥 v1
连接国内版(18789)和国际版(18791)的 OpenClaw 实例

0 依赖，纯 Python 3.14
"""
import os, json, http.client, socket
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
PROJECTS = os.path.join(FAMILY, 'projects')
FED_DIR = os.path.join(PROJECTS, 'igp-federation')
os.makedirs(FED_DIR, exist_ok=True)

INSTANCES = [
    {'name': '国内版', 'host': 'localhost', 'port': 18789, 'type': 'china'},
    {'name': '国际版', 'host': 'localhost', 'port': 18791, 'type': 'global'},
]


class FederationBridge:
    """联邦桥"""

    def __init__(self):
        self.instances = []
        self.status = {}

    def check_instance(self, host, port, name):
        """检查实例是否存活"""
        try:
            conn = http.client.HTTPConnection(host, port, timeout=3)
            conn.request('GET', '/v1/health')
            resp = conn.getresponse()
            body = resp.read().decode('utf-8')[:200]
            conn.close()
            return {
                'ok': resp.status == 200,
                'name': name,
                'host': host,
                'port': port,
                'status_code': resp.status,
                'response': body.strip(),
            }
        except Exception as e:
            return {
                'ok': False,
                'name': name,
                'host': host,
                'port': port,
                'error': str(e)[:100],
            }

    def scan_all(self):
        """扫描所有实例"""
        results = []
        for inst in INSTANCES:
            result = self.check_instance(inst['host'], inst['port'], inst['name'])
            results.append(result)
            self.status[inst['name']] = result
        return results

    def bridge_status(self):
        """桥接状态"""
        scan = self.scan_all()
        alive = sum(1 for s in scan if s['ok'])
        return {
            'timestamp': datetime.now().isoformat(),
            'instances': len(INSTANCES),
            'alive': alive,
            'dead': len(INSTANCES) - alive,
            'details': scan,
        }

    def cross_ping(self):
        """跨实例 ping"""
        report = self.bridge_status()
        
        # 建立跨桥数据包
        bridge_packet = {
            'protocol': 'IGP-FED/v1',
            'from': 'federation-bridge',
            'timestamp': datetime.now().isoformat(),
            'carrying': {
                'projects_count': self._count_projects(),
                'agents_count': self._count_agents(),
                'total_loc': self._count_loc(),
            }
        }
        
        report['bridge_packet'] = bridge_packet
        return report

    def _count_projects(self):
        proj_dir = os.path.join(FAMILY, 'projects')
        if not os.path.isdir(proj_dir):
            return 0
        return len([p for p in os.listdir(proj_dir) if os.path.isdir(os.path.join(proj_dir, p))])

    def _count_agents(self):
        genesis = os.path.join(PROJECTS, 'igp-genesis')
        if os.path.isdir(genesis):
            return len([f for f in os.listdir(genesis) if f.endswith('.py') and f != 'genesis.py']) + 1
        return 1

    def _count_loc(self):
        total = 0
        for root, _, files in os.walk(FAMILY):
            for f in files:
                if f.endswith('.py'):
                    fp = os.path.join(root, f)
                    try:
                        with open(fp, 'r', encoding='utf-8') as fh:
                            total += len(fh.readlines())
                    except:
                        pass
        return total


def main():
    bridge = FederationBridge()

    print('🌉 IGP Federation Bridge — 联邦桥 v1')
    print('=' * 55)

    # 扫描
    print('\n📡 扫描 OpenClaw 实例:')
    for inst in INSTANCES:
        result = bridge.check_instance(inst['host'], inst['port'], inst['name'])
        sym = '✅' if result['ok'] else '❌'
        print(f'  {sym} {result["name"]} ({result["host"]}:{result["port"]})')
        if result.get('error'):
            print(f'     {result["error"]}')
    
    # 跨桥
    print('\n🔗 跨桥连接:')
    report = bridge.cross_ping()
    if report['alive'] > 0:
        print(f'  存活: {report["alive"]}/{report["instances"]}')
        print(f'  桥包已生成:')
        bp = report['bridge_packet']
        print(f'    项目: {bp["carrying"]["projects_count"]} 个')
        print(f'    Agent: {bp["carrying"]["agents_count"]} 个')
        print(f'    代码:  {bp["carrying"]["total_loc"]} 行')
    else:
        print('  无实例在线，桥未建立')
    
    # 保存
    report_path = os.path.join(FED_DIR, 'federation_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f'\n📋 报告已保存: federation_report.json')
    print(f'\n🏆 联邦状态: {"已建立 ✅" if report["alive"] > 0 else "离线 ❌"}')

    return report


if __name__ == '__main__':
    main()
