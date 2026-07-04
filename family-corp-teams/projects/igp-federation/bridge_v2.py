"""
IGP Federation Bridge v2 — 文件级联邦桥
不依赖 HTTP，用共享文件在两个 OpenClaw 实例间交换数据

原理：
  国内版 ←→ 共享JSON文件 ←→ 国际版
  只要两个实例共用一个磁盘，就能通过文件交换数据

0 依赖，纯 Python 3.14
"""
import os, json, shutil, subprocess
from datetime import datetime

WORKSPACE = r'D:\bobo\openclaw-foreign\workspace'
FAMILY = os.path.join(WORKSPACE, 'family-corp-teams')
PROJECTS = os.path.join(FAMILY, 'projects')
FED_DIR = os.path.join(PROJECTS, 'igp-federation')
SHARED_DIR = os.path.join(FED_DIR, 'shared')
os.makedirs(SHARED_DIR, exist_ok=True)


class FileFederation:
    """文件级联邦"""

    def __init__(self):
        self.identity = 'igp-global'
        self.partner_identity = 'igp-china'
        self.my_dir = os.path.join(SHARED_DIR, self.identity)
        self.partner_dir = os.path.join(SHARED_DIR, self.partner_identity)
        os.makedirs(self.my_dir, exist_ok=True)
        os.makedirs(self.partner_dir, exist_ok=True)

    def send_message(self, to_identity, action, payload):
        """发送消息到另一个实例"""
        target_dir = os.path.join(SHARED_DIR, to_identity)
        os.makedirs(target_dir, exist_ok=True)
        
        msg = {
            'from': self.identity,
            'to': to_identity,
            'action': action,
            'payload': payload,
            'timestamp': datetime.now().isoformat(),
        }
        
        msg_id = datetime.now().strftime('%H%M%S%f')[:10]
        msg_path = os.path.join(target_dir, f'msg_{msg_id}.json')
        
        with open(msg_path, 'w', encoding='utf-8') as f:
            json.dump(msg, f, ensure_ascii=False, indent=2)
        
        return msg_path

    def read_messages(self):
        """读取发往我们的消息"""
        messages = []
        for f in sorted(os.listdir(self.my_dir)):
            if f.startswith('msg_') and f.endswith('.json'):
                fp = os.path.join(self.my_dir, f)
                try:
                    with open(fp, 'r', encoding='utf-8') as fh:
                        messages.append(json.load(fh))
                    os.remove(fp)  # 读完删
                except:
                    pass
        return messages

    def sync_projects(self):
        """同步项目状态到共享区"""
        projects_info = {}
        for p in sorted(os.listdir(PROJECTS)):
            pp = os.path.join(PROJECTS, p)
            if os.path.isdir(pp):
                files = [f for f in os.listdir(pp) if os.path.isfile(os.path.join(pp, f))]
                py_lines = 0
                for f in files:
                    if f.endswith('.py'):
                        try:
                            with open(os.path.join(pp, f), 'r', encoding='utf-8') as fh:
                                py_lines += len(fh.readlines())
                        except:
                            pass
                projects_info[p] = {
                    'files': len(files),
                    'py_lines': py_lines,
                }
        
        sync = {
            'from': self.identity,
            'type': 'sync',
            'timestamp': datetime.now().isoformat(),
            'projects': projects_info,
            'total_projects': len(projects_info),
            'total_lines': sum(v['py_lines'] for v in projects_info.values()),
        }
        
        sync_path = os.path.join(self.my_dir, f'sync_{datetime.now().strftime("%H%M%S")}.json')
        with open(sync_path, 'w', encoding='utf-8') as f:
            json.dump(sync, f, ensure_ascii=False, indent=2)
        
        # 也复制一份到partner的inbox
        partner_inbox = os.path.join(SHARED_DIR, self.partner_identity)
        os.makedirs(partner_inbox, exist_ok=True)
        partner_path = os.path.join(partner_inbox, f'from_{self.identity}_sync.json')
        shutil.copy2(sync_path, partner_path)
        
        return sync

    def scan_partner(self):
        """检查对方实例是否在线（通过文件）"""
        partner_sync = None
        for f in os.listdir(self.partner_dir):
            if f.startswith('from_') and 'sync' in f:
                fp = os.path.join(self.partner_dir, f)
                try:
                    with open(fp, 'r', encoding='utf-8') as fh:
                        partner_sync = json.load(fh)
                    break
                except:
                    pass
        
        if partner_sync:
            ts = partner_sync.get('timestamp', 'unknown')
            try:
                age = (datetime.now() - datetime.fromisoformat(ts)).total_seconds()
                online = age < 300  # 5分钟内算在线
            except:
                online = False
            return {
                'online': online,
                'name': partner_sync.get('from', 'unknown'),
                'last_seen': ts,
                'projects': partner_sync.get('total_projects', 0),
                'lines': partner_sync.get('total_lines', 0),
            }
        return {'online': False, 'error': '没有同步文件'}

    def status(self):
        """联邦状态"""
        self.send_message(self.partner_identity, 'ping', {'msg': 'hello from global'})
        partner = self.scan_partner()
        my_sync = self.sync_projects()
        
        return {
            'identity': self.identity,
            'partner': partner,
            'local': {
                'projects': my_sync['total_projects'],
                'lines': my_sync['total_lines'],
            },
            'messages_sent': 1,
            'status': 'FEDERATED' if partner['online'] else 'STANDALONE',
        }


def main():
    fed = FileFederation()

    print('🌉 IGP Federation Bridge v2 — 文件级联邦')
    print('=' * 55)
    
    # 发送测试消息
    print('\n📡 同步状态到共享区...')
    sync = fed.sync_projects()
    print(f'  已同步: {sync["total_projects"]} 项目, {sync["total_lines"]} 行代码')
    
    # 发送消息
    print('\n📨 发送消息到对方实例...')
    msg_path = fed.send_message('igp-china', 'hello', {'from': 'igp-global', 'version': 'v1'})
    print(f'  消息已发送: {os.path.basename(msg_path)}')
    
    # 读取对方消息
    print('\n📩 读取收到消息...')
    msgs = fed.read_messages()
    if msgs:
        for msg in msgs:
            print(f'  来自 {msg["from"]}: {msg["action"]} → {msg["payload"]}')
    else:
        print('  收件箱为空')
    
    # 查找对方
    print('\n🔍 扫描对方实例...')
    partner = fed.scan_partner()
    if partner['online']:
        print(f'  ✅ {partner["name"]} 在线!')
        print(f'     项目: {partner["projects"]} 代码: {partner["lines"]}行')
    else:
        print(f'  ❌ 对方离线 ({partner.get("error", "无同步文件")})')
    
    # 联邦状态
    status = fed.status()
    print(f'\n🏆 联邦状态: {status["status"]}')
    print(f'  目录: shared/')
    print(f'  本地: {status["local"]["projects"]} 项目, {status["local"]["lines"]} 行')
    
    # 保存报告
    report_path = os.path.join(FED_DIR, 'federation_v2_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=2)
    print(f'📋 报告已保存: federation_v2_report.json')

    return status


if __name__ == '__main__':
    main()
