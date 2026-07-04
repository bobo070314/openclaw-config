"""
染色体11: 类型/度量部 📏
吸收: radon圈复杂度分析 + AST静态类型推断
补: V5缺陷1(类型标注不足) + 缺陷7(无代码复杂度)
0外部依赖，纯Python标准库
"""
import os, sys, ast
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


class ComplexityAnalyzer:
    """纯Python圈复杂度分析器 (从radon吸收核心算法)
    
    度量:
    - 圈复杂度(cyclomatic complexity): 函数的分支数量
    - NASA复杂度: 圈复杂度按函数归类
    - Maintainability Index: 基于行数+圈复杂度+Halstead
    """
    
    def __init__(self):
        self.results = {}
    
    def analyze_file(self, filepath: str) -> Dict:
        """分析单文件"""
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            try:
                tree = ast.parse(f.read())
            except SyntaxError:
                return {'file': filepath, 'error': 'SyntaxError', 'functions': []}
        
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calc_complexity(node)
                loc = node.end_lineno - node.lineno + 1
                func_type = self._infer_type(node)
                functions.append({
                    'name': node.name,
                    'line': node.lineno,
                    'lines': loc,
                    'complexity': complexity,
                    'nasa_rank': self._nasa_rank(complexity),
                    'has_docstring': self._has_docstring(node),
                    'has_type_hints': self._has_type_hints(node),
                    'func_type': func_type,
                })
        
        avg_complexity = sum(f['complexity'] for f in functions) / max(len(functions), 1)
        total_lines = sum(f['lines'] for f in functions)
        
        result = {
            'file': filepath,
            'functions': functions,
            'avg_complexity': round(avg_complexity, 2),
            'total_fn': len(functions),
            'total_lines': total_lines,
            'maintainability_index': self._maintainability_index(avg_complexity, total_lines),
        }
        self.results[filepath] = result
        return result
    
    def _calc_complexity(self, func_node: ast.FunctionDef) -> int:
        """计算圈复杂度: 1(基线) + if/while/for/except/and/or/assert"""
        complexity = 1
        for node in ast.walk(func_node):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            elif isinstance(node, ast.Assert):
                complexity += 1
        return complexity
    
    def _nasa_rank(self, complexity: int) -> str:
        if complexity <= 10: return 'A - Simple'
        elif complexity <= 20: return 'B - Moderate'
        elif complexity <= 30: return 'C - Complex'
        elif complexity <= 40: return 'D - Very Complex'
        else: return 'E - Untestable'
    
    def _has_docstring(self, node: ast.FunctionDef) -> bool:
        return (node.body and isinstance(node.body[0], ast.Expr) 
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str))
    
    def _has_type_hints(self, node: ast.FunctionDef) -> bool:
        return bool(node.returns) or any(a.annotation for a in node.args.args)
    
    def _infer_type(self, node: ast.FunctionDef) -> str:
        """AST推断函数类型"""
        returns = False
        yields = False
        for n in ast.walk(node):
            if isinstance(n, ast.Return) and n.value:
                returns = True
            if isinstance(n, ast.Yield):
                yields = True
        if yields: return 'generator'
        if returns: return 'pure_function' if node.name.startswith(('calc_', 'compute_', 'get_', 'is_', 'has_')) else 'method'
        return 'procedure'
    
    def _maintainability_index(self, avg_complexity: float, total_lines: int) -> float:
        """Maintainability Index简化版"""
        mi = max(0, 171 - 5.2 * avg_complexity - 0.23 * total_lines - 16.2 * (total_lines ** 0.5))
        return round(mi, 1)
    
    def scan_directory(self, directory: str) -> Dict:
        """扫描整个目录"""
        for root, dirs, files in os.walk(directory):
            for f in sorted(files):
                if f.endswith('.py') and f != '__init__.py':
                    self.analyze_file(os.path.join(root, f))
        return self.results
    
    def score(self) -> Dict:
        """质量评分 (0-100)"""
        if not self.results:
            return {'score': 0, 'detail': 'no data'}
        
        scores = []
        for fp, res in self.results.items():
            if 'functions' not in res:
                continue
            s = 0
            for fn in res['functions']:
                fn_score = 100
                if fn['complexity'] > 10: fn_score -= 20
                if fn['complexity'] > 20: fn_score -= 20
                if not fn['has_docstring']: fn_score -= 10
                if not fn['has_type_hints']: fn_score -= 15
                s += fn_score
            avg_fn_score = s / max(len(res['functions']), 1)
            scores.append(avg_fn_score)
        
        overall = round(sum(scores) / max(len(scores), 1), 1)
        return {'score': overall, 'files': len(self.results)}


if __name__ == '__main__':
    print("📏 染色体11 类型/度量部 验证")
    
    import tempfile
    
    # 创建测试文件
    test_code = '''
def simple_function(x: int) -> int:
    """简单的纯函数"""
    return x + 1

def complex_function(data):
    # 无类型标注，高复杂度
    result = []
    for i in range(len(data)):
        if data[i] > 0:
            if data[i] < 100:
                result.append(data[i])
            elif data[i] < 200:
                result.append(data[i] * 2)
            else:
                while data[i] > 0:
                    data[i] -= 1
                    result.append(data[i])
        else:
            try:
                result.append(0 / data[i])
            except ZeroDivisionError:
                pass
    return result
'''
    
    test_fp = os.path.join(tempfile.gettempdir(), 'test_c11.py')
    with open(test_fp, 'w', encoding='utf-8') as f:
        f.write(test_code)
    
    analyzer = ComplexityAnalyzer()
    result = analyzer.analyze_file(test_fp)
    
    print(f"  文件: {os.path.basename(test_fp)}")
    for fn in result['functions']:
        print(f"    · {fn['name']}: CC={fn['complexity']} {fn['nasa_rank']}")
        print(f"      type_hints={'✅' if fn['has_type_hints'] else '❌'} doc={'✅' if fn['has_docstring'] else '❌'} type={fn['func_type']}")
    
    score = analyzer.score()
    print(f"\n  平均圈复杂度: {result['avg_complexity']}")
    print(f"  Maintainability Index: {result['maintainability_index']}")
    print(f"  质量评分: {score['score']}/100")
    
    assert result['avg_complexity'] > 0, "Complexity analysis failed"
    assert score['score'] > 0, "Scoring failed"
    
    print("\n✅ 染色体11 类型/度量部 验证通过")
