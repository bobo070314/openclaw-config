"""
IGP Harbinger Daemon — 持续循环版
每60秒巡逻一次，日志持续写入
Ctrl+C 停止
"""
import os, sys, time, json, subprocess
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
DAEMON_LOG = os.path.join(FAMILY, 'headquarters', 'daemon_log.json')


def single_patrol():
    """单次巡逻，调用 harbinger.py"""
    try:
        proc = subprocess.run(
            [sys.executable, os.path.join(FAMILY, 'headquarters', 'harbinger.py')],
            capture_output=True, text=True, timeout=120,
            env={**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'}
        )
        passed = '[✅] 全部正常' in proc.stdout or '全部正常' in proc.stdout
        return {
            'ok': passed,
            'time': datetime.now().isoformat()[:19],
            'output': proc.stdout[:100],
        }
    except Exception as e:
        return {
            'ok': False,
            'time': datetime.now().isoformat()[:19],
            'error': str(e)[:80],
        }


def run_daemon(cycles=5, interval=60):
    """持续运行"""
    history = []
    
    print('🛡  IGP Harbinger Daemon — 持续守护')
    print(f'  循环: {cycles} 次, 间隔: {interval}s')
    print(f'  开始: {datetime.now().isoformat()[:19]}')
    print('=' * 50)
    print()
    
    try:
        for i in range(cycles):
            print(f'[{i+1}/{cycles}] 巡逻中...', end=' ', flush=True)
            result = single_patrol()
            history.append(result)
            
            if result['ok']:
                print(f'✅ 通过 ({result["time"]})')
            else:
                print(f'❌ 失败: {result.get("error", "未知")}')
            
            if i < cycles - 1:
                print(f'  等待 {interval}s...')
                time.sleep(interval)
    
    except KeyboardInterrupt:
        print('\n  手动停止')
    
    # 统计
    total = len(history)
    ok_count = sum(1 for h in history if h['ok'])
    fail_count = total - ok_count
    health = f'{round(ok_count/total*100)}%' if total else 'N/A'
    
    print(f'\n{"=" * 50}')
    print(f'📊 守护报告:')
    print(f'  总巡逻: {total} 次')
    print(f'  通过: {ok_count}  |  失败: {fail_count}')
    print(f'  健康度: {health}')
    
    # 保存
    report = {
        'session': datetime.now().isoformat(),
        'cycles': total,
        'ok': ok_count,
        'fail': fail_count,
        'health': health,
        'history': history,
    }
    with open(DAEMON_LOG, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f'  日志: daemon_log.json')
    
    return report


if __name__ == '__main__':
    run_daemon(cycles=3, interval=5)  # 快速版：3次巡逻，5秒间隔
