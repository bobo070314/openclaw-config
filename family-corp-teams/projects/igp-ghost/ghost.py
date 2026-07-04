"""
IGP Ghost — 幽灵哨兵 v2
从"只检测"升级为"检测 + 自愈 + 报警 + 日志到记忆"
0 第三方依赖
"""
import os, sys, json, subprocess, shutil, time
from datetime import datetime

WORKSPACE = r'D:\bobo\openclaw-foreign\workspace'
FAMILY = os.path.join(WORKSPACE, 'family-corp-teams')
MEMORY = os.path.join(WORKSPACE, 'memory')
LOG_FILE = os.path.join(MEMORY, 'ghost_alert.json')

os.makedirs(MEMORY, exist_ok=True)

# ============================================================
# 检测模块
# ============================================================

def check_python_env():
    issues = []
    if sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
        issues.append(f'stdout编码: {sys.stdout.encoding} (期望UTF-8)')
    if sys.getdefaultencoding().lower() not in ('utf-8', 'utf8'):
        issues.append(f'默认编码: {sys.getdefaultencoding()} (期望UTF-8)')
    return {
        'ok': len(issues) == 0,
        'python': sys.version,
        'encoding_stdout': sys.stdout.encoding,
        'encoding_fs': sys.getfilesystemencoding(),
        'issues': issues
    }

def check_powershell():
    result = {'ok': True, 'issues': []}
    try:
        r = subprocess.run(
            ['powershell', '-Command', 'Write-Host ps_ok'],
            capture_output=True, text=True, timeout=5,
            encoding='utf-8', errors='replace'
        )
        if r.returncode != 0:
            result['issues'].append(f'PowerShell不可用: {r.stderr[:100]}')
            result['ok'] = False
    except Exception as e:
        result['issues'].append(f'PowerShell执行异常: {str(e)[:100]}')
        result['ok'] = False
    return result

def check_subagents():
    depts = ['frontend', 'backend', 'infra', 'ai', 'mobile', 'design',
             'quality', 'pmo', 'growth', 'data', 'tech-support', 'compliance']
    alive = []
    dead = []
    for d in depts:
        dp = os.path.join(FAMILY, d)
        if os.path.isdir(dp):
            alive.append(d)
        else:
            dead.append(d)
    return {
        'ok': len(dead) == 0,
        'total': len(depts),
        'alive': len(alive),
        'dead': len(dead),
        'alive_list': alive,
        'dead_list': dead
    }

def check_igp_heartbeat():
    result = {'ok': False, 'issues': []}
    hb = os.path.join(FAMILY, 'igp_heartbeat.py')
    if not os.path.exists(hb):
        result['issues'].append('igp_heartbeat.py 缺失')
        return result
    try:
        r = subprocess.run(
            [sys.executable, hb],
            capture_output=True, text=True, timeout=15,
            encoding='utf-8', errors='replace',
            env={**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'}
        )
        if r.returncode == 0:
            result['ok'] = True
        else:
            result['issues'].append(f'heartbeat运行失败: {r.stderr[:100]}')
    except Exception as e:
        result['issues'].append(f'heartbeat异常: {str(e)[:100]}')
    return result

def check_disk_space():
    path = WORKSPACE
    try:
        usage = shutil.disk_usage(path)
        free_gb = usage.free / (1024**3)
        total_gb = usage.total / (1024**3)
        pct = usage.used / usage.total * 100
        return {
            'ok': free_gb > 1,
            'total_gb': round(total_gb, 1),
            'free_gb': round(free_gb, 1),
            'used_pct': round(pct, 1),
            'issues': [] if free_gb > 1 else [f'磁盘空间不足: 剩余{free_gb:.1f}GB']
        }
    except:
        return {'ok': True, 'issues': ['disk_usage 不可用']}

# ============================================================
# 自愈模块 (v2 新增)
# ============================================================

def heal_issues(report):
    """尝试自动修复可修复的问题"""
    fixes = []
    
    # 修复1: Python 编码问题
    if not report['python']['ok']:
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
            ctypes.windll.kernel32.SetConsoleCP(65001)
            fixes.append('自愈: SetConsoleOutputCP(65001)')
            report['python']['ok'] = True
        except Exception as e:
            fixes.append(f'失败: 无法设置控制台编码 - {str(e)[:50]}')
    
    # 修复2: 部门目录缺失 → 重建
    for d in ['frontend', 'backend', 'infra', 'ai', 'mobile', 'design',
              'quality', 'pmo', 'growth', 'data', 'tech-support', 'compliance']:
        dp = os.path.join(FAMILY, d)
        if not os.path.isdir(dp):
            try:
                os.makedirs(dp)
                fixes.append(f'自愈: 重建部门目录 {d}')
            except Exception as e:
                fixes.append(f'失败: 无法重建 {d} - {str(e)[:50]}')
    
    # 修复3: memory 目录缺失
    if not os.path.exists(MEMORY):
        try:
            os.makedirs(MEMORY)
            fixes.append('自愈: 重建 memory 目录')
        except Exception as e:
            fixes.append(f'失败: 无法重建 memory - {str(e)[:50]}')
    
    # 修复4: 重建检查后，标记subagents为ok
    report['subagents'] = check_subagents()
    
    return fixes

# ============================================================
# 报警模块 (v2 新增)
# ============================================================

def alert(report, fixes):
    """生成报警日志 → 留档到 memory 和 D2A 消息"""
    alert_data = {
        'timestamp': datetime.now().isoformat(),
        'status': report['status'],
        'fixes': fixes,
        'issues': []
    }
    
    for check_name, check_result in report.items():
        if isinstance(check_result, dict) and not check_result.get('ok', True):
            issues = check_result.get('issues', ['unknown'])
            alert_data['issues'].extend([f'{check_name}: {i}' for i in issues])
    
    if alert_data['issues'] or fixes:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(alert_data, f, ensure_ascii=False, indent=2)
        # 同时写到 D2A 兼容格式
        d2a = {
            'id': 'ghost-' + datetime.now().strftime('%H%M%S'),
            'ts': alert_data['timestamp'],
            'from': 'ghost-sentinel',
            'to': 'hq-SWAT',
            'action': 'report',
            'data': alert_data
        }
        d2a_file = os.path.join(FAMILY, 'headquarters', '_ghost_report.json')
        with open(d2a_file, 'w', encoding='utf-8') as f:
            json.dump(d2a, f, ensure_ascii=False, indent=2)
    
    return alert_data

# ============================================================
# 主流程
# ============================================================

def run_all():
    print(f'👻 IGP Ghost v2 — 幽灵哨兵')
    print(f'   时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('='*50)
    
    # 检测
    report = {
        'timestamp': datetime.now().isoformat(),
        'python': check_python_env(),
        'powershell': check_powershell(),
        'subagents': check_subagents(),
        'heartbeat': check_igp_heartbeat(),
        'disk': check_disk_space()
    }
    
    check_items = [v for v in report.values() if isinstance(v, dict)]
    all_ok = all(v.get('ok', False) for v in check_items)
    report['status'] = 'OK' if all_ok else 'ALERT'
    
    print(f'\n📊 状态: {report["status"]}')
    for name, result in report.items():
        if isinstance(result, dict):
            sym = '✅' if result.get('ok', False) else '❌'
            print(f'  {sym} {name}')
            for i in result.get('issues', []):
                print(f'     ⚠ {i}')
    
    # 自愈
    fixes = []
    if report['status'] == 'ALERT':
        print(f'\n🔧 自愈模块启动...')
        fixes = heal_issues(report)
        for fix in fixes:
            print(f'  {fix}')
    else:
        print(f'\n🔧 无需自愈')
    
    # 报警
    alert_data = alert(report, fixes)
    if alert_data['issues'] or fixes:
        print(f'\n📡 报警已记录到: {LOG_FILE}')
        print(f'📡 D2A消息已发送到: headquarters/_ghost_report.json')
    
    print(f'\n✅ Ghost v2 运行完成')
    return report

if __name__ == '__main__':
    run_all()
