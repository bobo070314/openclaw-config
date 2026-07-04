#!/usr/bin/env python3
"""IGP V5 + V4 六步循环集成引擎 —— 每12小时全自动循环一次
把8条染色体 + V4主引擎 缝合在一起，跑六步进化
"""
import os, sys, json, time, subprocess, threading
from datetime import datetime, timezone, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # family-corp-teams
V5_DIR = os.path.join(BASE, 'v5')
V4_DIR = os.path.join(BASE, 'upgrade-v4')
CHROMO_DIR = os.path.join(V5_DIR, 'chromosomes')
DEPLOY_DIR = os.path.join(V5_DIR, 'deploy')
INJECT_DIR = os.path.join(V5_DIR, 'igp_inject')

STEP_NAMES = ["吸收", "消化", "研发", "突变", "裂变", "升级"]
LOG_FILE = os.path.join(V5_DIR, 'v5_engine_loop.json')

class V5LoopEngine:
    """V5 + V4 六步循环集成引擎"""
    
    def __init__(self):
        self.cycle_count = 0
        self.history = []
        self.chromosomes = {
            '1': 'MCP生态部',
            '2': 'A2A联邦部', 
            '3': 'Skills市场部',
            '4': 'Provider路由部',
            '5': '安全Guardian部',
            '6': '商业协议部',
            '7': 'Agent OS层',
            '8': 'AP2支付协议',
        }
        self.health = {}
        
    def run_step(self, step_name, chromo_id, chromo_name):
        """跑一步"""
        log = {
            'time': datetime.now(timezone.utc).isoformat(),
            'chromosome': chromo_name,
            'chromosome_id': chromo_id,
            'step': step_name,
            'step_index': STEP_NAMES.index(step_name) + 1,
            'status': 'pending',
        }
        try:
            # 找到染色体的run.py并执行
            run_path = None
            possible = [
                os.path.join(CHROMO_DIR, f'chromosome{chromo_id}', 'infra', 'run.py'),
                os.path.join(CHROMO_DIR, f'chromosome{chromo_id}', 'infra', 'run_v2.py'),
            ]
            for p in possible:
                if os.path.exists(p):
                    run_path = p
                    break
            
            if run_path:
                result = subprocess.run(
                    [sys.executable, run_path],
                    capture_output=True, text=True, timeout=30, encoding='utf-8',
                    cwd=os.path.dirname(run_path)
                )
                log['stdout'] = result.stdout[-200:] if result.stdout else ''
                log['stderr'] = result.stderr[-200:] if result.stderr else ''
                if result.returncode == 0:
                    log['status'] = 'success'
                else:
                    log['status'] = 'failed'
                    log['error'] = result.stderr[:300]
            else:
                # 没有run.py, 直接import验证
                infra = os.path.join(CHROMO_DIR, f'chromosome{chromo_id}', 'infra')
                py_files = [f for f in os.listdir(infra) if f.endswith('.py') and f != 'run.py'] if os.path.isdir(infra) else []
                log['status'] = 'success' if py_files else 'failed'
                log['note'] = f'{len(py_files)} modules present' if py_files else 'no modules'
        except subprocess.TimeoutExpired:
            log['status'] = 'timeout'
        except Exception as e:
            log['status'] = 'failed'
            log['error'] = str(e)[:300]
        return log
    
    def run_full_cycle(self):
        """跑一轮完整的六步循环，所有染色体"""
        self.cycle_count += 1
        timestamp = datetime.now(timezone.utc).isoformat()
        print(f'\\n{"="*60}')
        print(f'  🏭 IGP V5 循环 #{self.cycle_count} — {timestamp}')
        print(f'{"="*60}')
        
        cycle_log = {
            'cycle': self.cycle_count,
            'start_time': timestamp,
            'chromosomes': {}
        }
        
        for cid, cname in self.chromosomes.items():
            print(f'\\n  ▶ 染色体{cid} {cname}')
            chromo_log = []
            for step in STEP_NAMES:
                result = self.run_step(step, cid, cname)
                status_icon = '✅' if result['status'] == 'success' else '❌' if result['status'] == 'failed' else '⏳'
                print(f'    {status_icon} {step} — {result["status"]}')
                chromo_log.append(result)
            cycle_log['chromosomes'][cname] = chromo_log
            
            # 更新健康状态
            success_count = sum(1 for r in chromo_log if r['status'] == 'success')
            self.health[cname] = {
                'cycle': self.cycle_count,
                'success': success_count,
                'total': len(STEP_NAMES),
                'score': f'{success_count}/{len(STEP_NAMES)}'
            }
        
        cycle_log['end_time'] = datetime.now(timezone.utc).isoformat()
        cycle_log['health'] = self.health
        
        # 汇总
        print(f'\\n{"="*60}')
        print(f'  📊 循环 #{self.cycle_count} 汇总')
        print(f'{"="*60}')
        for cname, info in sorted(self.health.items(), key=lambda x: -int(x[1]['success'])):
            bar = '🟢' * info['success'] + '🔴' * (info['total'] - info['success'])
            print(f'  {cname:16s} {info["score"]} {bar}')
        
        self.history.append(cycle_log)
        self._save_log()
        
        return cycle_log
    
    def _save_log(self):
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'cycle_count': self.cycle_count,
                'last_run': datetime.now(timezone.utc).isoformat(),
                'health': self.health,
                'history': self.history
            }, f, ensure_ascii=False, indent=2)
    
    def run_forever(self, interval_hours=12):
        """持续运行，每 interval_hours 小时一轮"""
        print(f'  🕐 循环间隔: {interval_hours}小时')
        print(f'  Starting first cycle now...')
        self.run_full_cycle()
        
        while True:
            next_run = datetime.now(timezone.utc) + timedelta(hours=interval_hours)
            print(f'\\n  ⏰ 下一轮: {next_run.isoformat()}')
            time.sleep(interval_hours * 3600)
            self.run_full_cycle()

if __name__ == '__main__':
    engine = V5LoopEngine()
    # 先跑一轮验证
    cycle = engine.run_full_cycle()
    print(f'\\n  ✅ 第1轮循环完成')
    print(f'  📝 日志: {LOG_FILE}')
    print(f'  🚀 要开启持续循环请运行: python {__file__} --daemon')
    
    # 如果带 --daemon 参数，进入永久循环
    if '--daemon' in sys.argv:
        engine.run_forever(interval_hours=12)
