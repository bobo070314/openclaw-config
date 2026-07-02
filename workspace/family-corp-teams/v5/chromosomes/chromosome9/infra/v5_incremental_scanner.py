"""
IGP IncrementalScanner v2 — 增量变更追踪
吸收自: git diff解析 + AST对比分析 + 文件监视模式
纯标准库
"""
from __future__ import annotations
import os as _os
import time
import ast
import hashlib
import threading
from typing import Callable, Dict, List, Optional
from collections import defaultdict
from datetime import datetime, timezone


class Change:
    """单次代码变更"""
    
    def __init__(self, path: str, ctype: str, lines: List[int] = None,
                 old_hash: str = '', new_hash: str = ''):
        self.path = path
        self.ctype = ctype  # added/modified/deleted
        self.lines = lines or []
        self.old_hash = old_hash
        self.new_hash = new_hash
        self.ts = datetime.now(timezone.utc).isoformat()
        self.ast_diff: Optional[dict] = None


class IncrementalScanner:
    """增量扫描器v2 — diff/scan/watch/report"""
    
    def __init__(self):
        self._changes: List[Change] = []
        self._snapshots: Dict[str, str] = {}
        self._watch_stop = threading.Event()
        self._watch_thread: Optional[threading.Thread] = None
    
    def _file_hash(self, path: str) -> str:
        try:
            with open(path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except (FileNotFoundError, PermissionError):
            return ''
    
    def scan_diff(self, diff_text: str, base_dir: str = '.') -> List[Change]:
        changes = []
        current_file = None
        current_lines = []
        
        for line in diff_text.split('\n'):
            if line.startswith('diff --git'):
                if current_file:
                    changes.append(Change(current_file, 'modified', current_lines))
                current_file = line.split(' b/')[-1] if ' b/' in line else line
                current_lines = []
            elif line.startswith('@@'):
                parts = line.split(' ')
                np = parts[1] if '+' in parts[1] else (parts[2] if len(parts) > 2 else '')
                current_lines.append(np)
            elif line.startswith('+') and not line.startswith('+++'):
                current_lines.append(len(current_lines) + 1)
        
        if current_file:
            changes.append(Change(current_file, 'modified', current_lines))
        self._changes.extend(changes)
        return changes
    
    def scan_file(self, path: str, last_version: str = None) -> Optional[Change]:
        if not _os.path.exists(path):
            old = self._snapshots.get(path, '')
            if old:
                c = Change(path, 'deleted')
                c.old_hash = old
                self._changes.append(c)
                self._snapshots.pop(path, None)
                return c
            return None
        
        new_hash = self._file_hash(path)
        old_hash = last_version or self._snapshots.get(path, '')
        
        if old_hash and old_hash == new_hash:
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (FileNotFoundError, PermissionError):
            return None
        
        c = Change(path, 'modified' if old_hash else 'added')
        c.old_hash = old_hash
        c.new_hash = new_hash
        
        # AST分析
        try:
            tree = ast.parse(content)
            classes = []
            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    pass
            c.ast_diff = {'classes': classes, 'total_nodes': sum(1 for _ in ast.walk(tree))}
        except SyntaxError:
            c.ast_diff = {'classes': [], 'total_nodes': 0}
        
        self._changes.append(c)
        self._snapshots[path] = new_hash
        return c
    
    def track_change(self, path: str, ctype: str, lines: List[str] = None):
        c = Change(path, ctype, [i + 1 for i, _ in enumerate(lines or [])])
        self._changes.append(c)
        return c
    
    def watch(self, directory: str, recursive: bool = True,
              interval: float = 2.0, callback: Callable = None):
        old_hashes = {}
        for root, dirs, files in _os.walk(directory):
            if not recursive and root != directory:
                break
            for f in files:
                if f.endswith('.py'):
                    old_hashes[_os.path.join(root, f)] = self._file_hash(_os.path.join(root, f))
        
        self._watch_stop.clear()
        
        def watcher():
            while not self._watch_stop.is_set():
                time.sleep(interval)
                for root, dirs, files in _os.walk(directory):
                    if not recursive and root != directory:
                        break
                    for f in files:
                        if not f.endswith('.py'):
                            continue
                        fp = _os.path.join(root, f)
                        nh = self._file_hash(fp)
                        oh = old_hashes.get(fp, '')
                        if nh and nh != oh:
                            c = self.scan_file(fp)
                            old_hashes[fp] = nh
                            if c and callback:
                                callback(c)
        
        self._watch_thread = threading.Thread(target=watcher, daemon=True)
        self._watch_thread.start()
        return self
    
    def stop_watch(self):
        self._watch_stop.set()
        if self._watch_thread:
            self._watch_thread.join(timeout=3)
    
    def report(self, fmt: str = 'markdown') -> str:
        if fmt == 'markdown':
            lines = [
                f'# Incremental Scan Report',
                f'Generated: {datetime.now(timezone.utc).isoformat()}',
                f'Changes: {len(self._changes)}',
                '',
            ]
            for i, c in enumerate(self._changes[-20:], 1):
                lines.append(f'### {i}. {_os.path.basename(c.path)} ({c.ctype})')
                lines.append(f'- Path: `{c.path}`')
                if c.ast_diff:
                    lines.append(f'- AST: {len(c.ast_diff.get("classes", []))} classes, {c.ast_diff.get("total_nodes", 0)} nodes')
                lines.append('')
            
            summary = defaultdict(int)
            for c in self._changes:
                summary[c.ctype] += 1
            lines.append('## Summary')
            for k, v in sorted(summary.items()):
                lines.append(f'- {k}: {v}')
            return '\n'.join(lines)
        
        return f'{len(self._changes)} changes recorded'
    
    def clear(self):
        """清空变更记录"""
        self._changes.clear()
        self._snapshots.clear()
    
    def recent(self, count: int = 10) -> List[Change]:
        return self._changes[-count:]
