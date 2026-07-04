"""
IGP Nexus — 融合中枢
把 Ghost(监控) + D2A(通信) + CLI(入口) + Design(UI) 全部连接成一个系统

0 第三方依赖，纯 Python 3.14
"""
import os, sys, json, importlib, time
from datetime import datetime

WORKSPACE = r'D:\bobo\openclaw-foreign\workspace'
FAMILY = os.path.join(WORKSPACE, 'family-corp-teams')
PROJECTS = os.path.join(FAMILY, 'projects')

class IGPNexus:
    """IGP 融合中枢"""

    def __init__(self):
        self.modules = {}
        self.status = {}
        self._load_modules()

    def _load_modules(self):
        """加载所有可用模块"""
        checks = {
            'ghost': os.path.join(PROJECTS, 'igp-ghost', 'ghost.py'),
            'd2a': os.path.join(PROJECTS, 'igp-d2a', 'agent_protocol.py'),
            'v4_engine': os.path.join(FAMILY, 'upgrade-v4', 'igp_engine.py'),
            'v4_bridge': os.path.join(FAMILY, 'upgrade-v4', 'igp_a2a_bridge.py'),
            'heartbeat': os.path.join(FAMILY, 'igp_heartbeat.py'),
            'policy': os.path.join(FAMILY, 'igp_core_policy_v3.json'),
        }
        for name, path in checks.items():
            self.modules[name] = {
                'path': path,
                'exists': os.path.exists(path),
                'size': os.path.getsize(path) if os.path.exists(path) else 0,
            }

    def scan_all(self):
        """全模块扫描"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'nexus_version': 'v1',
            'modules': {},
            'projects': {},
            'departments': {},
            'd2a_compatible': True,
        }

        # 1. 检查核心模块
        for name, info in self.modules.items():
            report['modules'][name] = {
                'ok': info['exists'] and info['size'] > 0,
                'size_kb': round(info['size'] / 1024, 1),
            }

        # 2. 检查项目目录
        projects_dir = PROJECTS
        if os.path.exists(projects_dir):
            for p in os.listdir(projects_dir):
                pp = os.path.join(projects_dir, p)
                if os.path.isdir(pp):
                    files = [f for f in os.listdir(pp) if os.path.isfile(os.path.join(pp, f))]
                    report['projects'][p] = {
                        'files': len(files),
                        'file_list': files[:10],
                    }

        # 3. 检查12部门
        depts = ['frontend', 'backend', 'infra', 'ai', 'mobile', 'design',
                 'quality', 'pmo', 'growth', 'data', 'tech-support', 'compliance']
        for d in depts:
            dp = os.path.join(FAMILY, d)
            report['departments'][d] = {
                'alive': os.path.isdir(dp),
                'reports': [f for f in os.listdir(dp) if '_report' in f or 'report' in f] if os.path.isdir(dp) else [],
            }

        # 4. 整体状态
        all_modules_ok = all(v['ok'] for v in report['modules'].values())
        all_depts_alive = all(v['alive'] for v in report['departments'].values())
        report['status'] = 'OK' if (all_modules_ok and all_depts_alive) else 'ALERT'
        report['score'] = sum(1 for v in report['modules'].values() if v['ok'])
        report['score_max'] = len(report['modules'])

        self.status = report
        return report

    def run_all_agents(self):
        """模拟运行所有D2A Agent之间的通信"""
        sys.path.insert(0, os.path.join(PROJECTS, 'igp-d2a'))
        try:
            from agent_protocol import IGP_Agent, AgentMessage

            agents = {
                'nexus': IGP_Agent('nexus-core', 'headquarters'),
                'ghost': IGP_Agent('ghost-sentinel', 'ghost-team'),
                'd2a': IGP_Agent('d2a-broker', 'infra'),
                'swat': IGP_Agent('hq-SWAT', 'headquarters'),
            }

            # Nexus 广播状态
            for name, agent in agents.items():
                if name != 'nexus' and name != 'swat':
                    msg = agents['nexus'].send(f'{name}', 'request', {'what': 'status'})
                    agents[name].receive(msg.to_dict())
                    result = agents[name].process_all()
                    agents['nexus'].receive(result[0])

            # Ghost 汇报检测结果
            ghost_report = agents['ghost'].send('hq-SWAT', 'report', {
                'detections': 12,
                'alerts': 0,
                'status': 'OK'
            })
            agents['swat'].receive(ghost_report.to_dict())
            agents['swat'].process_all()

            return {
                'agents_count': len(agents),
                'messages_exchanged': sum(a.status()['total_logs'] for a in agents.values()),
                'agents': {k: v.status() for k, v in agents.items()},
            }
        except Exception as e:
            return {'error': str(e)}

    def generate_unified_report(self):
        """生成统一的系统报告"""
        scan = self.scan_all()
        agents = self.run_all_agents()

        report = {
            'unified_report': {
                'generated': datetime.now().isoformat(),
                'name': 'IGP NEXUS — 融合系统报告',
            },
            'scan': scan,
            'agents': agents,
        }

        report_path = os.path.join(FAMILY, 'headquarters', '_nexus_report.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return report


def main():
    nexus = IGPNexus()
    
    print('🌐 IGP Nexus — 融合中枢 v1')
    print('=' * 50)
    
    # 1. 全模块扫描
    print('\n📡 全模块扫描:')
    scan = nexus.scan_all()
    for name, info in scan['modules'].items():
        sym = '✅' if info['ok'] else '❌'
        print(f'  {sym} {name} ({info["size_kb"]} KB)')

    print(f'\n📊 部门存活:')
    for name, info in scan['departments'].items():
        sym = '✅' if info['alive'] else '❌'
        print(f'  {sym} {name}')

    # 2. Agent 通信
    print('\n🔗 D2A Agent 通信模拟:')
    agents_result = nexus.run_all_agents()
    if 'error' in agents_result:
        print(f'  ❌ {agents_result["error"]}')
    else:
        print(f'  ✅ {agents_result["agents_count"]} 个Agent, {agents_result["messages_exchanged"]} 条消息')
        for name, s in agents_result.get('agents', {}).items():
            print(f'     {name}: {s["total_logs"]}条日志')

    # 3. 生成统一报告
    print('\n📋 生成统一报告...')
    report = nexus.generate_unified_report()
    print(f'  ✅ 报告已写入: headquarters/_nexus_report.json')
    
    # 4. 最终状态
    score = scan['score']
    max_score = scan['score_max']
    print(f'\n🏆 融合系统评分: {score}/{max_score}')
    if score == max_score:
        print('   全部模块就绪 ✅')
    else:
        missing = [k for k, v in scan['modules'].items() if not v['ok']]
        print(f'   缺失: {", ".join(missing)}')

    return scan


if __name__ == '__main__':
    main()
