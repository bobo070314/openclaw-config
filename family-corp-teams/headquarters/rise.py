"""IGP RISE — 全自动工单系统
自动scan所有部门产出，自动派发工单，自动追踪进度
"""
import os, sys, json, subprocess, hashlib
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
HQ = os.path.join(FAMILY, 'headquarters')
PROJECTS = os.path.join(FAMILY, 'projects')
TICKET_FILE = os.path.join(HQ, 'tickets.json')


class TicketEngine:
    """全自动工单系统"""
    
    def __init__(self):
        self.tickets = self._load()
    
    def _load(self):
        if os.path.exists(TICKET_FILE):
            with open(TICKET_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'version': 1, 'tickets': [], 'counter': 0}
    
    def _save(self):
        with open(TICKET_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.tickets, f, ensure_ascii=False, indent=2)
    
    def create(self, title, priority=3, assignee='auto'):
        self.tickets['counter'] += 1
        tid = f'TICKET-{self.tickets["counter"]:04d}'
        ticket = {
            'id': tid,
            'title': title,
            'priority': priority,
            'assignee': assignee,
            'status': 'open',
            'created': datetime.now().isoformat()[:19],
            'updated': datetime.now().isoformat()[:19],
        }
        self.tickets['tickets'].append(ticket)
        self._save()
        return ticket
    
    def close(self, tid):
        for t in self.tickets['tickets']:
            if t['id'] == tid:
                t['status'] = 'closed'
                t['updated'] = datetime.now().isoformat()[:19]
                self._save()
                return True
        return False
    
    def list_open(self):
        return [t for t in self.tickets['tickets'] if t['status'] == 'open']


class AutoScanner:
    """自动扫描器"""
    
    def scan_projects(self):
        """扫描所有项目"""
        projects = {}
        if not os.path.exists(PROJECTS):
            return projects
        
        for p in sorted(os.listdir(PROJECTS)):
            pp = os.path.join(PROJECTS, p)
            if not os.path.isdir(pp):
                continue
            
            py_files = [f for f in os.listdir(pp) if f.endswith('.py')]
            md_files = [f for f in os.listdir(pp) if f.endswith('.md')]
            total_lines = 0
            for pyf in py_files:
                try:
                    with open(os.path.join(pp, pyf), encoding='utf-8') as f:
                        total_lines += len(f.readlines())
                except:
                    pass
            
            # 检查能否运行
            has_main = False
            for pyf in py_files:
                try:
                    with open(os.path.join(pp, pyf), encoding='utf-8') as f:
                        content = f.read()
                        if '__main__' in content:
                            has_main = True
                            break
                except:
                    pass
            
            projects[p] = {
                'py_files': len(py_files),
                'docs': len(md_files),
                'lines': total_lines,
                'has_main': has_main,
                'last_modified': datetime.fromtimestamp(os.path.getmtime(pp)).isoformat()[:19],
            }
        
        return projects
    
    def scan_errors(self, projects):
        """扫描问题"""
        issues = []
        for name, info in projects.items():
            if info['py_files'] == 0:
                issues.append(f'{name}: 无Python文件')
            if not info['has_main'] and info['py_files'] > 0:
                issues.append(f'{name}: 无__main__入口')
            if info['docs'] == 0:
                issues.append(f'{name}: 无文档')
        return issues


class AutoDeploy:
    """全自动部署"""
    
    def __init__(self):
        self.ticket = TicketEngine()
        self.scanner = AutoScanner()
    
    def run(self):
        print('IGP RISE — 自动巡检部署系统')
        print('=' * 50)
        print()
        
        # 1. 扫描项目
        print('扫描项目...')
        projects = self.scanner.scan_projects()
        print(f'  发现 {len(projects)} 个项目')
        
        for name, info in sorted(projects.items()):
            mark = '' if info['has_main'] else ''
            print(f'  {mark} {name:20s} | {info["py_files"]}py {info["docs"]}docs {info["lines"]}行')
        print()
        
        # 2. 检查问题
        print('检查问题...')
        issues = self.scanner.scan_errors(projects)
        if issues:
            for issue in issues:
                print(f'  {issue}')
                self.ticket.create(f'修复: {issue}', priority=2)
        else:
            print('  无问题')
        print()
        
        # 3. 统计
        open_tickets = self.ticket.list_open()
        print(f'工单: {len(open_tickets)} 个待处理')
        
        total_lines = sum(p['lines'] for p in projects.values())
        total_py = sum(p['py_files'] for p in projects.values())
        
        report = {
            'timestamp': datetime.now().isoformat()[:19],
            'projects': len(projects),
            'py_files': total_py,
            'lines': total_lines,
            'issues': len(issues),
            'open_tickets': len(open_tickets),
        }
        
        print()
        print('=' * 50)
        print(f'部署报告:')
        print(f'  项目: {report["projects"]}')
        print(f'  Python文件: {report["py_files"]}')
        print(f'  总行数: {report["lines"]}')
        print(f'  问题: {report["issues"]}')
        print(f'  待处理工单: {report["open_tickets"]}')
        
        return report


def main():
    deploy = AutoDeploy()
    deploy.run()


if __name__ == '__main__':
    main()
