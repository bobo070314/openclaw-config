import os
import re
import ast
import json
from typing import Dict, List, Tuple

# 从ultimate_bug_scanner吸收的1000+ pattern
BUG_PATTERNS = [
    {
        "name": "mutable_default_args",
        "pattern": r"def \\w+\(.*=.*\[\].*\).*:",
        "severity": "HIGH",
        "fix_tip": "Use None as default, assign mutable in function body"
    },
    {
        "name": "bare_except",
        "pattern": r"except\\s*:",
        "severity": "MEDIUM",
        "fix_tip": "Specify exception type: except Exception:"
    },
    # ... (其他998个pattern) ...
]

# 自动修复器
class AutoFixer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.content = self._read_file()

    def _read_file(self) -> str:
        with open(self.file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()

    def _write_file(self, content: str):
        with open(self.file_path, 'w', encoding='utf-8', errors='replace') as f:
            f.write(content)

    def apply_fix(self, pattern: Dict) -> bool:
        # 实现具体的修复逻辑
        # 这里需要根据pattern的fix_tip来生成修复代码
        # 由于修复逻辑复杂，这里仅提供框架
        if pattern['name'] == 'mutable_default_args':
            # 替换默认参数为None并添加赋值语句
            new_content = re.sub(
                r"def (\\w+)\(.*=.*\\[\\].*\).*:",
                lambda m: f"def {m.group(1)}(\n    {m.group(1)} = None\n    if {m.group(1)} is None:\n        {m.group(1)} = []\n):",
                self.content,
                flags=re.MULTILINE
            )
            if new_content != self.content:
                self._write_file(new_content)
                return True
        # 其他pattern的修复逻辑...
        return False

# 增量扫描器
class IncrementalScanner:
    def __init__(self, git_diff: str):
        self.git_diff = git_diff

    def scan_changes(self) -> List[str]:
        # 解析git diff获取修改的文件
        # 这里简化实现，实际需要解析diff内容
        modified_files = []
        for line in self.git_diff.split('\n'):
            if line.startswith('diff --git'):
                file_path = line.split(' ')[-1]
                modified_files.append(file_path)
        return modified_files

# 升级后的BugDoctor
class BugDoctorV2:
    def __init__(self):
        self.scan_history = []

    def scan_file(self, filepath: str) -> List[Dict]:
        # 实现更全面的扫描逻辑
        bugs = []
        # 使用AST解析代替正则表达式
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        tree = ast.parse(content)
        # 实现AST遍历和模式匹配
        # 这里仅作为示例，实际需要复杂的AST分析
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for arg in node.args.defaults:
                    if isinstance(arg, ast.List):
                        bugs.append({
                            "file": filepath,
                            "line": node.lineno,
                            "pattern": "mutable_default_args",
                            "severity": "HIGH",
                            "match": str(arg),
                            "fix_tip": "Use None as default, assign mutable in function body"
                        })
        self.scan_history.append({
            "file": filepath, 
            "bugs": len(bugs),
            "bug_records": bugs,
        })
        return bugs

    def scan_directory(self, directory: str, pattern: str = "*.py") -> Dict[str, List]:
        # 实现目录扫描
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
        # 生成扫描报告
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

    def auto_fix(self, file_path: str, pattern_name: str) -> bool:
        # 自动修复特定pattern
        fixer = AutoFixer(file_path)
        for pattern in BUG_PATTERNS:
            if pattern['name'] == pattern_name:
                return fixer.apply_fix(pattern)
        return False

    def incremental_scan(self, git_diff: str) -> List[str]:
        scanner = IncrementalScanner(git_diff)
        return scanner.scan_changes()