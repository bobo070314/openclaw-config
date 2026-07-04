"""
IGP-D2A: Digest-to-Act Agent通信协议 v1
0第三方依赖，纯Python 3.14
灵感: Google A2A Protocol (Linux Foundation, 2025/04)
实现: JSON消息 + HTTP本地通信
"""
import json, uuid, os, sys
from datetime import datetime

class AgentMessage:
    """Agent间消息体"""
    def __init__(self, sender, receiver, action, payload=None):
        self.id = str(uuid.uuid4())[:8]
        self.timestamp = datetime.now().isoformat()
        self.sender = sender  # department:team
        self.receiver = receiver  # department:team
        self.action = action  # request/response/report/alert
        self.payload = payload or {}

    def to_dict(self):
        return {
            'id': self.id,
            'ts': self.timestamp,
            'from': self.sender,
            'to': self.receiver,
            'action': self.action,
            'data': self.payload
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

class IGP_Agent:
    """IGP部门Agent节点"""
    def __init__(self, name, dept='unknown'):
        self.name = name
        self.dept = dept
        self.inbox = []
        self.log = []

    def send(self, receiver, action, payload=None):
        """发送消息给另一个Agent"""
        msg = AgentMessage(self.name, receiver, action, payload)
        self.log.append({'type': 'send', 'msg': msg.to_dict()})
        return msg

    def receive(self, msg_dict):
        """接收消息"""
        self.inbox.append(msg_dict)
        self.log.append({'type': 'receive', 'msg': msg_dict})
        return msg_dict['action']

    def process_all(self):
        """处理所有收件箱消息"""
        results = []
        while self.inbox:
            msg = self.inbox.pop(0)
            action = msg['action']
            sender = msg['from']
            if action == 'request':
                reply = self.send(sender, 'response', {'status': 'ok', 'result': f'{self.name} processed'})
                results.append(reply.to_dict())
            elif action == 'report':
                results.append({'ack': f'{self.name} received report from {sender}'})
            elif action == 'alert':
                results.append({'ack': f'{self.name} acknowledged alert from {sender}'})
        return results

    def status(self):
        return {
            'agent': self.name,
            'dept': self.dept,
            'inbox_size': len(self.inbox),
            'total_logs': len(self.log)
        }


def simulate_igp_communication():
    """
    模拟IGP内部3个Agent通信:
    quality-team1 → infra-team2 (请求检查环境)
    infra-team2 → quality-team1 (返回检查结果)
    quality-team1 → hq-SWAT (汇报总结)
    """
    print('\nIGP-D2A Agent通信模拟:')
    print('-'*40)

    # 创建3个Agent
    qa = IGP_Agent('quality-team1', 'quality')
    infra = IGP_Agent('infra-team2', 'infra')
    swat = IGP_Agent('hq-SWAT', 'headquarters')

    # Step 1: quality → infra 请求环境检查
    msg1 = qa.send('infra-team2', 'request', {'check': 'python_encoding'})
    infra.receive(msg1.to_dict())
    result1 = infra.process_all()
    print(f'  quality → infra: 请求环境检查')
    print(f'    req: {msg1.id} [{msg1.action}]')
    print(f'    resp: {result1[0]["action"]} | status={result1[0]["data"]["status"]}')

    # Step 2: quality 收集infra结果 → 汇报SWAT
    report_payload = {
        'check_results': {
            'python_ok': True,
            'powershell_ok': True,
            'departments_alive': 12
        }
    }
    msg2 = qa.send('hq-SWAT', 'report', report_payload)
    swat.receive(msg2.to_dict())
    result2 = swat.process_all()
    print(f'  quality → SWAT: 汇报系统状态')
    print(f'    report: {msg2.id} [{msg2.action}]')

    # 最终状态
    print('\n  Agent最终状态:')
    for agent in [qa, infra, swat]:
        s = agent.status()
        print(f'    {s["agent"]}: {s["total_logs"]}条日志')

    return {
        'agents': [qa.status(), infra.status(), swat.status()],
        'messages_count': sum(a.status()['total_logs'] for a in [qa, infra, swat])
    }
