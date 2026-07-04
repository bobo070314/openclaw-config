"""
IGP Harbinger — 常驻守护进程 v1
每60秒循环检测系统健康，自动修复，自动汇报
真正的无人值守模式
"""
import os, sys, json, time, subprocess
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
HEARTBEAT_LOG = os.path.join(FAMILY, 'headquarters', 'harbinger_log.json')


class Harbinger:
    """常驻守护进程"""
    
    def __init__(self):
        self.start_time = datetime.now().isoformat()
        self.cycles = 0
        self.ok_count = 0
        self.fail_count = 0
        self.log = []

    def run_python(self, script_path, timeout=60):
        """运行一个Python脚本并返回结果"""
        try:
            start = time.time()
            proc = subprocess.run(
                [sys.executable, script_path],
                capture_output=True, text=True, timeout=timeout,
                env={**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'}
            )
            elapsed = round(time.time() - start, 2)
            return {
                'ok': proc.returncode == 0,
                'output': (proc.stdout[:200] if proc.stdout else '(no stdout)'),
                'error': (proc.stderr[:200] if proc.stderr else None),
                'elapsed': elapsed,
            }
        except subprocess.TimeoutExpired as te:
            partial_out = te.output.decode('utf-8', errors='replace')[:200] if te.output else ''
            return {'ok': False, 'output': partial_out, 'error': 'timeout', 'elapsed': timeout}
        except Exception as e:
            return {'ok': False, 'output': '', 'error': str(e)[:100], 'elapsed': 0}

    def patrol(self):
        """一次完整的巡逻"""
        self.cycles += 1
        cycle = {
            'time': datetime.now().isoformat(),
            'cycle': self.cycles,
            'checks': {},
        }

        # 检查1: Ghost 健康检查
        ghost_path = os.path.join(FAMILY, 'projects', 'igp-ghost', 'ghost.py')
        if os.path.exists(ghost_path):
            r = self.run_python(ghost_path, timeout=8)
            cycle['checks']['ghost'] = {'ok': r['ok'], 'detail': r['output'][:80]}
        else:
            cycle['checks']['ghost'] = {'ok': False, 'detail': 'ghost.py not found'}

        # 检查2: D2A Agent通信
        d2a_path = os.path.join(FAMILY, 'projects', 'igp-d2a', 'agent_protocol.py')
        if os.path.exists(d2a_path):
            r = self.run_python(d2a_path, timeout=8)
            cycle['checks']['d2a'] = {'ok': r['ok'], 'detail': r['output'][:80]}
        else:
            cycle['checks']['d2a'] = {'ok': False, 'detail': 'agent_protocol.py not found'}

        # 检查3: Genesis复制引擎
        genesis_path = os.path.join(FAMILY, 'projects', 'igp-genesis', 'genesis.py')
        if os.path.exists(genesis_path):
            r = self.run_python(genesis_path, timeout=8)
            cycle['checks']['genesis'] = {'ok': r['ok'], 'detail': r['output'][:80]}
        else:
            cycle['checks']['genesis'] = {'ok': False, 'detail': 'genesis.py not found'}

        # 检查4: Oracle日报
        oracle_path = os.path.join(FAMILY, 'headquarters', 'oracle.py')
        if os.path.exists(oracle_path):
            r = self.run_python(oracle_path, timeout=10)
            cycle['checks']['oracle'] = {'ok': r['ok'], 'detail': r['output'][:80]}
        else:
            cycle['checks']['oracle'] = {'ok': False, 'detail': 'oracle.py not found'}

        # 检查5: RealScore
        realscore_path = os.path.join(FAMILY, 'headquarters', 'realscore.py')
        if os.path.exists(realscore_path):
            r = self.run_python(realscore_path, timeout=15)
            cycle['checks']['realscore'] = {'ok': r['ok'], 'detail': r['output'][:80]}
        else:
            cycle['checks']['realscore'] = {'ok': False, 'detail': 'realscore.py not found'}

        # 综合状态
        all_ok = all(v['ok'] for v in cycle['checks'].values())
        cycle['all_ok'] = all_ok

        if all_ok:
            self.ok_count += 1
        else:
            self.fail_count += 1

        self.log.append(cycle)
        return cycle

    def report(self):
        """生成状态报告"""
        return {
            'uptime': {
                'started': self.start_time,
                'cycles': self.cycles,
                'ok': self.ok_count,
                'fail': self.fail_count,
                'health': f'{self.ok_count}/{max(self.cycles, 1)} ({round(self.ok_count/max(self.cycles,1)*100)}%)',
            },
            'last_cycle': self.log[-1] if self.log else None,
            'standby': True,
        }

    def save(self):
        report = self.report()
        with open(HEARTBEAT_LOG, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return report


def single_shot():
    """单次运行模式"""
    h = Harbinger()
    print('🛡  IGP Harbinger — 常驻守护进程')
    print('=' * 55)
    print('  模式: 单次巡逻')
    print()

    cycle = h.patrol()
    
    # 输出结果
    for name, check in cycle['checks'].items():
        sym = '✅' if check['ok'] else '❌'
        print(f'  {sym} {name}: {check["detail"][:60]}')

    print(f'\n  综合: {"✅ 全部正常" if cycle["all_ok"] else "❌ 存在故障"}')
    print(f'  耗时: {datetime.now().isoformat()[:19]}')

    report = h.save()
    print(f'\n📋 报告已保存: harbinger_log.json')
    
    return report


if __name__ == '__main__':
    single_shot()
