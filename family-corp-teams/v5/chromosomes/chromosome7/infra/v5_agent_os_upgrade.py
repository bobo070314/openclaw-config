"""
v5 Agent OS Upgrade — chromosome7

Modules: ProcessScheduler, IPCChannel, TokenBudget, KernelV2
"""
import os, sys, json, threading, queue, time, hashlib
from collections import defaultdict, deque
from datetime import datetime, timezone

# ============================================================
# ProcessScheduler: priority + time-slice scheduling
# ============================================================
class ProcessScheduler:
    """Multi-level priority scheduler with thread pool"""
    
    PRIORITY_LEVELS = [0, 1, 2]  # 0=high, 1=medium, 2=low
    TIME_SLICE_MS = [100, 200, 500]
    
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.queues = {p: deque() for p in self.PRIORITY_LEVELS}
        self.running = {}
        self.completed = {}
        self._lock = threading.Lock()
        self._counter = 0
        
    def submit(self, func, args=(), priority=1, name=None):
        """Submit a task to the scheduler"""
        pid = f"p{self._counter}_{int(time.time()*1000)}"
        self._counter += 1
        task = {
            'id': pid,
            'name': name or func.__name__,
            'func': func,
            'args': args,
            'priority': priority,
            'submitted': time.time(),
        }
        with self._lock:
            self.queues[priority].append(pid)
            self.running[pid] = task
        return pid
    
    def run_once(self):
        """Execute one cycle: drain queues by priority"""
        for p in self.PRIORITY_LEVELS:
            q = self.queues[p]
            for _ in range(min(len(q), self.max_workers)):
                pid = q.popleft() if q else None
                if pid is None: continue
                task = self.running.get(pid)
                if not task: continue
                try:
                    result = task['func'](*task['args'])
                    task['result'] = result
                    task['status'] = 'completed'
                except Exception as e:
                    task['error'] = str(e)
                    task['status'] = 'failed'
                task['ended'] = time.time()
                self.completed[pid] = task
        return len(self.completed)
    
    def get_status(self):
        """Return snapshot of scheduler state"""
        with self._lock:
            return {
                'queued': {p: len(q) for p, q in self.queues.items()},
                'running': len(self.running),
                'completed': len(self.completed),
            }


# ============================================================
# IPCChannel: message queue + event bus
# ============================================================
class IPCChannel:
    """Inter-process communication via message queues and event bus"""
    
    def __init__(self):
        self._msg_queues = defaultdict(queue.Queue)
        self._event_bus = defaultdict(list)
        self._lock = threading.Lock()
        
    def send(self, channel, message, sender='system'):
        """Send a message to a channel queue"""
        msg = {
            'sender': sender,
            'channel': channel,
            'body': message,
            'ts': time.time(),
            'id': hashlib.md5(f"{sender}{channel}{time.time()}".encode()).hexdigest()[:8],
        }
        self._msg_queues[channel].put_nowait(msg)
        self._publish('message', msg)
        return msg['id']
    
    def receive(self, channel, timeout=1.0):
        """Receive from a channel queue (blocking with timeout)"""
        try:
            return self._msg_queues[channel].get(timeout=timeout)
        except queue.Empty:
            return None
    
    def subscribe(self, event_type, callback):
        """Subscribe to event bus notifications"""
        with self._lock:
            self._event_bus[event_type].append(callback)
            return len(self._event_bus[event_type]) - 1
    
    def _publish(self, event_type, data):
        with self._lock:
            for cb in self._event_bus.get(event_type, []):
                try:
                    cb(data)
                except Exception:
                    pass
    
    def stats(self):
        """Return queue depth per channel"""
        return {c: q.qsize() for c, q in self._msg_queues.items()}


# ============================================================
# TokenBudget: per-agent/per-task allocation
# ============================================================
class TokenBudget:
    """Token budget manager with real-time tracking"""
    
    def __init__(self, default_limit=10000):
        self.default_limit = default_limit
        self._agents = {}
        self._tasks = {}
        self._lock = threading.Lock()
        
    def register_agent(self, agent_id, limit=None):
        """Register an agent with a token budget"""
        with self._lock:
            self._agents[agent_id] = {
                'limit': limit or self.default_limit,
                'used': 0,
                'allocated': 0,
            }
    
    def allocate(self, agent_id, task_id, tokens):
        """Allocate tokens to a task for an agent"""
        with self._lock:
            agent = self._agents.get(agent_id)
            if not agent:
                return False, 'agent not found'
            available = agent['limit'] - agent['allocated']
            if tokens > available:
                return False, f'over budget: need {tokens}, have {available}'
            agent['allocated'] += tokens
            self._tasks[task_id] = {
                'agent': agent_id,
                'tokens': tokens,
                'used': 0,
                'created': time.time(),
            }
            return True, 'ok'
    
    def consume(self, task_id, tokens):
        """Consume tokens from a task allocation"""
        with self._lock:
            task = self._tasks.get(task_id)
            if not task: return False, 'task not found'
            remaining = task['tokens'] - task['used']
            if tokens > remaining:
                tokens = remaining
            task['used'] += tokens
            self._agents[task['agent']]['used'] += tokens
            return True, 'ok'
    
    def get_usage(self, agent_id=None):
        """Return usage report for agent or all"""
        with self._lock:
            if agent_id:
                a = self._agents.get(agent_id)
                return {
                    'agent': agent_id,
                    'limit': a['limit'],
                    'used': a['used'],
                    'allocated': a['allocated'],
                    'percent': round(a['used'] / a['limit'] * 100, 1) if a['limit'] else 0,
                } if a else None
            return {aid: self._agents[aid]['used'] for aid in self._agents}
    
    def reset(self, agent_id=None):
        """Reset budgets for agent or all"""
        with self._lock:
            targets = [agent_id] if agent_id else list(self._agents.keys())
            for aid in targets:
                if aid in self._agents:
                    self._agents[aid]['used'] = 0
                    self._agents[aid]['allocated'] = 0


# ============================================================
# Kernel v2: lifecycle + process monitor + watchdog
# ============================================================
class KernelV2:
    """Agent OS Kernel v2 — process management, monitoring, watchdog"""
    PROC_STATES = ['created', 'running', 'paused', 'stopped', 'crashed']
    
    def __init__(self):
        self.scheduler = ProcessScheduler()
        self.ipc = IPCChannel()
        self.token_budget = TokenBudget()
        self._processes = {}
        self._watchdog_interval = 5.0
        self._running = False
        self._watchdog_thread = None
        self._metrics = defaultdict(int)
        
    def spawn(self, name, func, args=(), priority=1, token_limit=None):
        """Spawn a new process"""
        pid = self.scheduler.submit(func, args, priority, name)
        self._processes[pid] = {
            'name': name,
            'state': 'created',
            'pid': pid,
            'created': time.time(),
            'priority': priority,
            'token_limit': token_limit,
        }
        if token_limit:
            self.token_budget.register_agent(pid, token_limit)
        self._metrics['spawned'] += 1
        return pid
    
    def start_watchdog(self):
        """Start the watchdog monitor thread"""
        if self._running: return
        self._running = True
        
        def _watch():
            while self._running:
                try:
                    self.scheduler.run_once()
                    # Check for stalled processes
                    now = time.time()
                    for pid, proc in list(self._processes.items()):
                        if proc['state'] == 'running' and now - proc.get('created', now) > 30:
                            proc['state'] = 'crashed'
                            self._metrics['crashed'] += 1
                            self._metrics['watchdog_recover'] += 1
                except Exception:
                    pass
                time.sleep(0.1)
        
        self._watchdog_thread = threading.Thread(target=_watch, daemon=True)
        self._watchdog_thread.start()
    
    def stop_watchdog(self):
        self._running = False
    
    def get_monitor(self):
        """Return full system monitor snapshot"""
        return {
            'processes': len(self._processes),
            'states': {s: sum(1 for p in self._processes.values() if p['state'] == s) for s in self.PROC_STATES},
            'scheduler': self.scheduler.get_status(),
            'ipc_channels': self.ipc.stats(),
            'metrics': dict(self._metrics),
        }
    
    def kill(self, pid):
        """Kill a process by pid"""
        if pid in self._processes:
            self._processes[pid]['state'] = 'stopped'
            self._metrics['killed'] += 1
            return True
        return False


if __name__ == '__main__':
    # Quick self-test
    import time
    print("Testing KernelV2...")
    kernel = KernelV2()
    kernel.start_watchdog()
    
    def dummy_task(name):
        time.sleep(0.05)
        return f"{name} done"
    
    p1 = kernel.spawn('task_a', dummy_task, ('A',), priority=0)
    p2 = kernel.spawn('task_b', dummy_task, ('B',), priority=1)
    p3 = kernel.spawn('task_c', dummy_task, ('C',), priority=2)
    
    time.sleep(0.3)
    
    monitor = kernel.get_monitor()
    assert monitor['processes'] == 3, f"Expected 3, got {monitor['processes']}"
    
    # Test IPC
    kernel.ipc.send('test', {'msg': 'hello'})
    msg = kernel.ipc.receive('test', timeout=0.5)
    assert msg is not None, "IPC receive failed"
    
    # Test TokenBudget
    kernel.token_budget.register_agent('agent1', 1000)
    ok, _ = kernel.token_budget.allocate('agent1', 'task1', 500)
    assert ok, "Allocation failed"
    usage = kernel.token_budget.get_usage('agent1')
    assert usage['percent'] == 0, f"Expected 0%, got {usage['percent']}%"
    
    kernel.stop_watchdog()
    print("=== [DONE] Agent OS layer UPGRADE ===")
