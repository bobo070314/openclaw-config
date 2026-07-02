"""
IGP 研发部 V6 — 三Agent评审引擎
三位独立评审Agent：架构/安全/兼容
纯AST+模式匹配，0 LLM依赖
"""
from __future__ import annotations
import ast
import os
import sys
from typing import Any, Dict, List, Tuple


class ArchitectureAgent:
    """架构Agent — 检查设计模式、耦合度、职责单一"""
    
    def __init__(self, name: str = "Architecture-Agent"):
        self.name = name
    
    def review(self, filepath: str) -> Dict:
        """评审一个文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                src = f.read()
            tree = ast.parse(src)
        except Exception as e:
            return {"score": 0, "issues": [f"Parse error: {e}"]}
        
        issues = []
        
        # 检查类大小
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                if len(methods) > 15:
                    issues.append(f"Large class '{node.name}' has {len(methods)} methods — consider splitting")
        
        # 检查函数复杂度
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                body_lines = node.end_lineno - node.lineno
                if body_lines > 80:
                    issues.append(f"Long function '{node.name}' ({body_lines} lines) — consider extracting")
        
        # 检查全局变量使用
        for node in ast.walk(tree):
            if isinstance(node, ast.Global):
                issues.append(f"Uses global at line {node.lineno} — prefer encapsulation")
        
        score = max(1, min(10, 10 - len(issues) * 2))
        return {"agent": self.name, "score": score, "issues": issues}
    
    def name(self) -> str:
        return self.name


class SecurityAgent:
    """安全Agent — 检查恶意模式、注入、敏感操作"""
    
    def __init__(self, name: str = "Security-Agent"):
        self.name = name
    
    def review(self, filepath: str) -> Dict:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                src = f.read()
            tree = ast.parse(src)
            lines = src.split('\n')
        except Exception as e:
            return {"score": 0, "issues": [f"Parse error: {e}"]}
        
        issues = []
        
        for node in ast.walk(tree):
            # bare except
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                ctx = lines[node.lineno - 1].strip() if node.lineno <= len(lines) else ""
                issues.append(f"Bare except at line {node.lineno}: {ctx}")
            
            # eval/exec
            if isinstance(node, ast.Call):
                func = ""
                if isinstance(node.func, ast.Name):
                    func = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func = node.func.attr
                if func in ("eval", "exec", "compile", "__import__"):
                    ctx = lines[node.lineno - 1].strip() if node.lineno <= len(lines) else ""
                    severity = "CRITICAL" if func in ("eval", "exec") else "HIGH"
                    issues.append(f"[{severity}] '{func}' at line {node.lineno}: {ctx}")
            
            # os.system/subprocess with shell
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    attr = node.func.attr
                    if attr in ("system", "popen", "call") and isinstance(node.func.value, ast.Name):
                        if node.func.value.id in ("os", "subprocess"):
                            ctx = lines[node.lineno - 1].strip() if node.lineno <= len(lines) else ""
                            issues.append(f"[HIGH] '{attr}' shell call at line {node.lineno}: {ctx}")
        
        score = max(1, min(10, 10 - len(issues) * 2))
        return {"agent": self.name, "score": score, "issues": issues}
    
    def name(self) -> str:
        return self.name


class CompatibilityAgent:
    """兼容Agent — 检查API变更、签名diff"""
    
    def __init__(self, name: str = "Compatibility-Agent"):
        self.name = name
    
    def extract_signatures(self, filepath: str) -> Dict[str, str]:
        """提取公共API签名"""
        sigs = {}
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                src = f.read()
            tree = ast.parse(src)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith('_'):
                    args = [a.arg for a in node.args.args]
                    sigs[node.name] = f"def {node.name}({', '.join(args)})"
                elif isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and not n.name.startswith('_')]
                    sigs[f"class {node.name}"] = f"class {node.name}({', '.join(methods)})"
        except Exception:
            pass
        return sigs
    
    def review(self, filepath: str) -> Dict:
        """检查当前文件API清晰度"""
        sigs = self.extract_signatures(filepath)
        issues = []
        
        total = len(sigs)
        if total == 0:
            issues.append("No public API detected")
        
        # 检查方法命名清晰度
        for name in sigs:
            if len(name) < 3:
                issues.append(f"Short name '{name}' — consider more descriptive")
            if name.startswith('_'):
                issues.append(f"Private name '{name}' in public API")
        
        score = max(1, min(10, 10 - len(issues)))
        return {"agent": self.name, "score": score, "issues": issues, "api_count": total}
    
    def name(self) -> str:
        return self.name


def review_file(filepath: str) -> Dict:
    """三Agent联合评审一个文件"""
    agents = [
        ArchitectureAgent(),
        SecurityAgent(),
        CompatibilityAgent(),
    ]
    
    results = []
    for agent in agents:
        r = agent.review(filepath)
        results.append(r)
    
    total_score = sum(r["score"] for r in results)
    all_issues = []
    for r in results:
        for i in r.get("issues", []):
            all_issues.append(f"[{r['agent']}] {i}")
    
    passed = total_score >= 18  # 阈值: 平均6分
    
    return {
        "file": os.path.basename(filepath),
        "total_score": total_score,
        "max_score": 30,
        "passed": passed,
        "agents": results,
        "all_issues": all_issues,
    }


if __name__ == '__main__':
    import sys
    
    target = sys.argv[1] if len(sys.argv) > 1 else r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\v6_lifecycle.py'
    
    if os.path.isfile(target):
        result = review_file(target)
        print(f"三Agent评审报告: {result['file']}")
        print(f"总分: {result['total_score']}/{result['max_score']} {'✅ PASS' if result['passed'] else '❌ FAIL'}")
        for r in result['agents']:
            print(f"\n  [{r['agent']}] Score: {r['score']}/10")
            for i in r['issues']:
                print(f"    ⚠ {i}")
        if result['all_issues']:
            print(f"\n总问题数: {len(result['all_issues'])}")
    elif os.path.isdir(target):
        results = []
        for root, dirs, files in os.walk(target):
            for f in files:
                if f.endswith('.py'):
                    fp = os.path.join(root, f)
                    r = review_file(fp)
                    results.append(r)
                    status = '✅' if r['passed'] else '❌'
                    print(f"{status} {r['file']:30} {r['total_score']}/{r['max_score']}")
        
        passed = [r for r in results if r['passed']]
        failed = [r for r in results if not r['passed']]
        print(f"\n总计: {len(results)} 文件 | ✅ PASS {len(passed)} | ❌ FAIL {len(failed)}")
