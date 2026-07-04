"""
IGP Pipeline — 监控→通信→报警→自愈 流水线

将 Ghost (监控) → D2A (通信) → Nexus (中央) 串联成一条完整的流水线
"""
import os, sys, json
from datetime import datetime

WORKSPACE = r'D:\bobo\openclaw-foreign\workspace'
FAMILY = os.path.join(WORKSPACE, 'family-corp-teams')
PROJECTS = os.path.join(FAMILY, 'projects')
LOG_FILE = os.path.join(WORKSPACE, 'memory', 'pipeline_log.json')

os.makedirs(os.path.join(WORKSPACE, 'memory'), exist_ok=True)


def step1_monitor():
    """Step 1: 监控 — 运行 Ghost 检测"""
    print('  [Step 1] 监控  ── Ghost 检测中...')
    sys.path.insert(0, os.path.join(PROJECTS, 'igp-ghost'))
    from ghost import check_python_env, check_powershell, check_subagents, check_disk_space, heal_issues

    report = {
        'python': check_python_env(),
        'powershell': check_powershell(),
        'subagents': check_subagents(),
        'disk': check_disk_space(),
    }
    
    # 尝试自愈
    fixes = heal_issues(report)
    
    all_ok = all(
        isinstance(v, dict) and v.get('ok', True)
        for v in report.values()
    )
    
    result = {
        'status': 'OK' if all_ok else 'ALERT',
        'checks': {k: v.get('ok', False) for k, v in report.items()},
        'details': report,
        'fixes': fixes,
    }
    print(f'          状态: {result["status"]} | 自愈: {len(fixes)}项')
    return result


def step2_communicate(monitor_result):
    """Step 2: 通信 — Ghost → D2A Agent 发送状态"""
    print('  [Step 2] 通信  ── Ghost → D2A Agent...')
    sys.path.insert(0, os.path.join(PROJECTS, 'igp-d2a'))
    from agent_protocol import IGP_Agent

    ghost_agent = IGP_Agent('ghost-sentinel', 'ghost-team')
    nexus_agent = IGP_Agent('nexus-core', 'headquarters')
    swat_agent = IGP_Agent('hq-SWAT', 'headquarters')

    # Ghost 发送检测报告给 Nexus
    msg1 = ghost_agent.send('nexus-core', 'report', {
        'pipeline_step': 'monitor',
        'status': monitor_result['status'],
        'checks_ok': sum(1 for v in monitor_result['checks'].values() if v),
        'checks_total': len(monitor_result['checks']),
        'fixes': monitor_result['fixes'],
    })
    nexus_agent.receive(msg1.to_dict())
    nexus_result = nexus_agent.process_all()

    # Nexus 转发报警到 SWAT（如果有问题）
    if monitor_result['status'] == 'ALERT':
        msg2 = nexus_agent.send('hq-SWAT', 'alert', {
            'origin': 'ghost-sentinel',
            'type': 'system_health',
            'details': monitor_result['details'],
        })
        swat_agent.receive(msg2.to_dict())
        swat_agent.process_all()
        alert_triggered = True
    else:
        alert_triggered = False

    log = {
        'agents_count': 3,
        'messages': sum(a.status()['total_logs'] for a in [ghost_agent, nexus_agent, swat_agent]),
    }
    print(f'          消息流转: {log["messages"]}条 | 报警触发: {alert_triggered}')
    return log


def step3_heal(monitor_result, comm_log):
    """Step 3: 自愈 — 根据检测结果自动修复"""
    print('  [Step 3] 自愈  ── 自动化修复...')
    fixes = []
    details = monitor_result.get('details', {})

    # 自愈 Python 编码
    if not details.get('python', {}).get('ok', True):
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
            fixes.append('SetConsoleOutputCP(65001) ✓')
        except Exception as e:
            fixes.append(f'编码修复失败: {e}')

    # 自愈部门目录
    if not details.get('subagents', {}).get('ok', True):
        depts = ['frontend', 'backend', 'infra', 'ai', 'mobile', 'design',
                 'quality', 'pmo', 'growth', 'data', 'tech-support', 'compliance']
        rebuilt = 0
        for d in depts:
            dp = os.path.join(FAMILY, d)
            if not os.path.isdir(dp):
                try:
                    os.makedirs(dp)
                    rebuilt += 1
                except:
                    pass
        if rebuilt > 0:
            fixes.append(f'重建 {rebuilt} 个部门目录 ✓')

    print(f'          执行自愈: {len(fixes)}项')
    for f in fixes:
        print(f'            {f}')
    return fixes


def step4_report(monitor_result, comm_log, fixes):
    """Step 4: 汇报 — 输出流水线日志"""
    print('  [Step 4] 汇报  ── 写入流水线日志...')
    
    pipeline_report = {
        'timestamp': datetime.now().isoformat(),
        'pipeline': 'monitor → communicate → heal → report',
        'status': monitor_result['status'],
        'steps': {
            'monitor': {
                'status': monitor_result['status'],
                'checks_ok': sum(1 for v in monitor_result['checks'].values() if v),
                'checks_total': len(monitor_result['checks']),
            },
            'communicate': {
                'messages': comm_log['messages'],
                'alert_triggered': comm_log.get('alert_triggered', False),
            },
            'heal': {
                'fixes_applied': len(fixes),
                'fixes': fixes,
            },
        },
        'summary': '',
    }

    # 摘要
    if monitor_result['status'] == 'OK' and not fixes:
        pipeline_report['summary'] = '系统健康，无需干预'
    elif fixes:
        pipeline_report['summary'] = f'检测到问题 → 自动修复 {len(fixes)} 项'
    else:
        pipeline_report['summary'] = '检测到问题，但无法自动修复（需人工介入）'

    # 写入日志
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(pipeline_report, f, ensure_ascii=False, indent=2)

    # 同时写入 D2A 兼容格式到 HQ
    d2a_report = {
        'id': f'pipeline-{datetime.now().strftime("%H%M%S")}',
        'ts': pipeline_report['timestamp'],
        'from': 'pipeline-orchestrator',
        'to': 'hq-SWAT',
        'action': 'report',
        'data': pipeline_report,
    }
    d2a_path = os.path.join(FAMILY, 'headquarters', '_pipeline_report.json')
    with open(d2a_path, 'w', encoding='utf-8') as f:
        json.dump(d2a_report, f, ensure_ascii=False, indent=2)

    print(f'          日志: memory/pipeline_log.json')
    print(f'          D2A:  headquarters/_pipeline_report.json')
    print(f'          摘要: {pipeline_report["summary"]}')
    return pipeline_report


def main():
    print('=' * 55)
    print('  ⚡ IGP Pipeline — 监控→通信→报警→自愈')
    print('=' * 55)

    # 全流程
    print()
    monitor = step1_monitor()
    print()
    comm = step2_communicate(monitor)
    print()
    fixes = step3_heal(monitor, comm)
    print()
    report = step4_report(monitor, comm, fixes)

    print()
    print('=' * 55)
    print(f'  🏆 流水线状态: {report["status"]}')
    print(f'     摘要: {report["summary"]}')
    print('=' * 55)

    return report


if __name__ == '__main__':
    main()
