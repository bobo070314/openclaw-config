"""
染色体7 Agent OS — 填充空方法
升级: 内核消息/停止/预算 + 调度器预算
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from collections import deque


class AgentOSKernel:
    """Agent OS内核 — IO/路由/预算管理"""
    
    def __init__(self, name: str = 'kernel'):
        self.name = name
        self._inbox: deque = deque()
        self._outbox: deque = deque()
        self._agents: Dict[str, Any] = {}
        self._running = True
        self._token_budget = 1000000
        self._tokens_used = 0
    
    def register_agent(self, agent_id: str, handler) -> 'AgentOSKernel':
        self._agents[agent_id] = handler
        return self
    
    def send_message(self, to: str, msg: str, sender: str = 'kernel') -> Dict:
        """发送消息到指定Agent"""
        self._outbox.append({
            'to': to, 'sender': sender, 'body': msg,
            'ts': datetime.now(timezone.utc).isoformat(),
        })
        handler = self._agents.get(to)
        if handler and callable(handler):
            try:
                return handler(msg, sender=sender)
            except Exception as e:
                return {'error': str(e), 'to': to}
        return {'queued': True, 'to': to, 'sender': sender}
    
    def receive(self) -> Optional[Dict]:
        """接收下一条消息"""
        if self._inbox:
            return self._inbox.popleft()
        return None
    
    def stop(self) -> Dict:
        """停止内核"""
        self._running = False
        return {
            'kernel': self.name,
            'stopped': True,
            'pending_inbox': len(self._inbox),
            'pending_outbox': len(self._outbox),
            'tokens_used': self._tokens_used,
        }
    
    def _manage_token_budget(self, max_budget: int = 1000000) -> Dict:
        """管理token预算"""
        self._token_budget = max_budget
        available = max(0, self._token_budget - self._tokens_used)
        return {'budget': self._token_budget, 'used': self._tokens_used, 'available': available}
    
    def status(self) -> Dict:
        return {
            'name': self.name,
            'running': self._running,
            'agents': len(self._agents),
            'inbox': len(self._inbox),
            'outbox': len(self._outbox),
            'tokens': self._tokens_used,
        }


class AgentOSScheduler:
    """Agent OS调度器 — 任务调度/预算管理"""
    
    def __init__(self):
        self._tasks: Dict[str, Dict] = {}
        self._token_budget = 500000
        self._tokens_used = 0
    
    def add_task(self, task_id: str, func, priority: int = 0) -> 'AgentOSScheduler':
        self._tasks[task_id] = {
            'func': func, 'priority': priority, 'status': 'pending', 'created': datetime.now(timezone.utc).isoformat(),
        }
        return self
    
    def _manage_token_budget(self, max_budget: int = 500000) -> Dict:
        """管理调度器的token预算"""
        self._token_budget = max_budget
        return {'budget': self._token_budget, 'used': self._tokens_used, 'available': max(0, self._token_budget - self._tokens_used)}
    
    def run_pending(self) -> int:
        count = 0
        for tid, task in sorted(self._tasks.items(), key=lambda x: -x[1]['priority']):
            if task['status'] == 'pending':
                task['status'] = 'running'
                self._tokens_used += 100
                count += 1
        return count


class AgentOSShell:
    """Agent OS Shell — CLI/帮助"""
    
    def __init__(self, kernel: AgentOSKernel = None):
        self.kernel = kernel or AgentOSKernel()
        self._history: List[str] = []
    
    def run_command(self, cmd: str) -> str:
        self._history.append(cmd)
        if cmd in ('help', '-h', '--help'):
            return self._show_help()
        return f'Unknown: {cmd}'
    
    def _show_help(self) -> str:
        """显示帮助"""
        return '\n'.join([
            'AgentOS Shell Commands:',
            '  help / -h / --help   Show this help',
            '  status               Kernel status',
            '  stop                 Stop kernel',
            '',
            'Available Agents: ' + ', '.join(getattr(self.kernel, '_agents', {}).keys() or ['none']),
        ])
