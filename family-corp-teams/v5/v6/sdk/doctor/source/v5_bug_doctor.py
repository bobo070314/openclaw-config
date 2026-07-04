#!/usr/bin/env python3
"""IGP V5 Bug Doctor —— 基于Ultimate Bug Scanner模式的自动修复"""

import os, sys, re, ast, json
from typing import Dict, List, Tuple

BUG_PATTERNS = [
    {
        "name": "mutable_default_args",
        "pattern": r"def \\\w+\(.*=.*\[\].*\).*:|def \\\w+\(.*=.*\{\}.*\)",
        "severity": "HIGH",
        "fix_tip": "Use None as default, assign mutable in function body"
    },
    {
        "name": "bare_except",
        "pattern": r"except\\s*:",
        "severity": "MEDIUM",
        "fix_tip": "Specify exception type: except Exception:"
    },
    {
        "name": "hardcoded_secret",
        "pattern": r"PASSWORD|SECRET_KEY|API_TOKEN\\s*=\\s*['\"][A-Za-z0-9]{8,}",
        "severity": "CRITICAL",
        "fix_tip": "Move to environment variable"
    },
    {
        "name": "sql_injection",
        "pattern": r"execute\(f['\"].*\{.*\}",
        "severity": "CRITICAL",
        "fix_tip": "Use parameterized queries"
    },
    {
        "name": "unsafe_eval",
        "pattern": r"eval\(|exec\(",
        "severity": "HIGH",
        "fix_tip": "Avoid eval/exec, use safer alternatives"
    },
    {
        "name": "missing_await",
        "pattern": r"asyncio\.run\(|loop\.run_until_complete",
        "severity": "MEDIUM",
        "fix_tip": "Use await in async context"
    },
    {
        "name": "insecure_pickle",
        "pattern": r"pickle\.loads|pickle\.load",
        "severity": "HIGH",
        "fix_tip": "Use json or safe serialization"
    },
    {
        "name": "shell_injection",
        "pattern": r"os\.system\(|subprocess\.call\(.*shell=True|subprocess\.Popen\(.*shell=True",
        "severity": "CRITICAL",
        "fix_tip": "Avoid shell=True, use list arguments"
    },
    {
        "name": "path_traversal",
        "pattern": r"open\(.*['\"]\.\.\/|os\.path\.join\(.*['\"]\.\.\/",
        "severity": "HIGH",
        "fix_tip": "Validate and sanitize file paths"
    },
    {
        "name": "exception_info_leak",
        "pattern": r"traceback\.print_exc|print\(.*e.*\)",
        "severity": "MEDIUM",
        "fix_tip": "Log exceptions, don't expose to users"
    },
]


class BugDoctor:
    """V5代码Bug扫描器"""
    
    def __init__(self):
        self.scan_history = []
    
    def scan_file(self, filepath: str) -> List[Dict]:
        """扫描单个文件，返回bugs列表"""
        bugs = []
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        for pattern in BUG_PATTERNS:
            matches = re.finditer(pattern["pattern"], content, re.MULTILINE)
            for m in matches:
                line_num = content[:m.start()].count('\n') + 1
                bugs.append({
                    "file": filepath,
                    "line": line_num,
                    "pattern": pattern["name"],
                    "severity": pattern["severity"],
                    "match": m.group()[:60],
                    "fix_tip": pattern["fix_tip"],
                })
        
        self.scan_history.append({
            "file": filepath, 
            "bugs": len(bugs),
            "bug_records": bugs,
        })
        return bugs
    
    def scan_directory(self, directory: str, pattern: str = "*.py") -> Dict[str, List]:
        """扫描整个目录"""
        results = {}
        for root, dirs, files in os.walk(directory):
            for f in sorted(files):
                if f.endswith('.py') and f != '__init__.py':
                    fp = os.path.join(root, f)
                    bugs = self.scan_file(fp)
                    if bugs:
                        results[fp] = bugs
        return results
    
    def get_report(self) -> Dict:
        """生成扫描报告"""
        total = 0
        by_severity = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for entry in self.scan_history:
            for bug in entry.get("bug_records", []):
                total += 1
                sev = bug.get("severity", "UNKNOWN")
                if sev in by_severity:
                    by_severity[sev] += 1
        return {
            "files_scanned": len(self.scan_history),
            "total_bugs": total,
            "by_severity": by_severity,
        }
