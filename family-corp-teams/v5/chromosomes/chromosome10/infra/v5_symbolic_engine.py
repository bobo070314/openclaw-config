"""
染色体10: 逻辑推理部 🧠 
吸收: Z3符号推理 + deal契约式编程
补: V5缺陷6 — 纯函数/推理层缺失
"""
import os, sys, ast, re
from typing import Dict, List, Tuple, Any, Optional


class SymbolicEngine:
    """纯Python符号推理引擎（从Z3吸收核心思想）
    
    支持: 符号变量、约束求解、范围推断、布尔推理
    0外部依赖，纯Python标准库
    """
    
    def __init__(self):
        self.constraints = []
        self.variables = {}
    
    def add_var(self, name: str, vtype: str = 'int', bounds: tuple = None):
        """声明符号变量"""
        self.variables[name] = {'type': vtype, 'bounds': bounds}
    
    def add_constraint(self, expr: str):
        """添加约束条件"""
        self.constraints.append(expr)
    
    def solve(self) -> Dict[str, Any]:
        """简单约束求解器（区间传播）"""
        result = {}
        for var_name, info in self.variables.items():
            low, high = info.get('bounds', (None, None))
            if info['type'] == 'int':
                low = low if low is not None else -2**31
                high = high if high is not None else 2**31
            elif info['type'] == 'float':
                low = float(low) if low is not None else -1e308
                high = float(high) if high is not None else 1e308
            
            # 从约束推断更紧的边界
            for c in self.constraints:
                if var_name in c:
                    m = re.search(rf'{var_name}\s*[<>=!]+\s*(-?\d+)', c)
                    if m:
                        val = int(m.group(1))
                        if '<=' in c or '<' in c:
                            high = min(high, val)
                        if '>=' in c or '>' in c:
                            low = max(low, val)
            result[var_name] = (low, high)
        return result
    
    def check(self) -> bool:
        """检查当前约束是否可满足"""
        solution = self.solve()
        for var_name, (low, high) in solution.items():
            if low is not None and high is not None and low > high:
                return False
        return True
    
    def infer_return_type(self, func) -> Dict[str, str]:
        """从函数体推断返回类型"""
        try:
            source = func.__code__
            # Simple inference from annotations
            hints = func.__annotations__
            if 'return' in hints:
                return {'type': str(hints['return']), 'source': 'annotation'}
        except Exception:
            pass
        return {'type': 'Any', 'source': 'unknown'}


class ContractDecorator:
    """从deal吸收的契约式编程装饰器
    
    支持: 前置条件(precondition)、后置条件(postcondition)、不变量(invariant)
    """
    
    @staticmethod
    def precondition(check_func):
        """前置条件装饰器"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not check_func(*args, **kwargs):
                    raise ValueError(f"Precondition failed: {check_func.__doc__ or 'condition not met'}")
                return func(*args, **kwargs)
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            return wrapper
        return decorator
    
    @staticmethod
    def postcondition(check_func):
        """后置条件装饰器"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if not check_func(result):
                    raise ValueError(f"Postcondition failed: {check_func.__doc__ or 'result check failed'}")
                return result
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            return wrapper
        return decorator
    
    @staticmethod
    def invariant(check_func):
        """类不变量装饰器"""
        def decorator(cls):
            original_init = cls.__init__
            def new_init(self, *args, **kwargs):
                original_init(self, *args, **kwargs)
                if not check_func(self):
                    raise ValueError(f"Invariant failed: {check_func.__doc__ or 'object invariant'}")
            cls.__init__ = new_init
            return cls
        return decorator


class LogicReasoner:
    """逻辑推理引擎 — 规则匹配 + 变量替换推理链
    
    支持简单的一阶逻辑推理:
    - 规则: premise -> conclusion (如 man(X) -> mortal(X))
    - 事实: man(Socrates)
    - 查询: mortal(Socrates) -> True (通过变量替换 X=Socrates)
    """
    
    def __init__(self):
        self.rules = []  # [(name, premise, conclusion)]
        self.facts = set()
    
    def add_rule(self, rule_name: str, premise: str, conclusion: str):
        """添加推理规则: 如果premise成立则conclusion成立"""
        self.rules.append((rule_name, premise, conclusion))
    
    def add_fact(self, fact: str):
        """添加已知事实"""
        self.facts.add(fact)
    
    def _substitute(self, template: str, var: str, value: str) -> str:
        """替换变量 (如 man(X) + X=Socrates -> man(Socrates))"""
        return template.replace(f'({var})', f'({value})').replace(f'({var},', f'({value},').replace(f',{var})', f',{value})').replace(f',{var},', f',{value},')
    
    def reason(self, query: str) -> Tuple[bool, List[str]]:
        """前向推理: 能否证明query成立
        
        步骤:
        1. 解析规则: man(X) -> mortal(X)
        2. 从事实提取变量: man(Socrates) -> variable X=Socrates
        3. 替结论: mortal(Socrates)
        4. 重复直到无法推导出新事实
        """
        derived = set(self.facts)
        chain = []
        
        changed = True
        while changed:
            changed = False
            for name, premise, conclusion in self.rules:
                # 解析规则中的变量 (大写开头的单词)
                rule_vars = []
                for token in premise.replace('(', ' ').replace(')', ' ').replace(',', ' ').split():
                    if token and token[0].isupper():
                        rule_vars.append(token)
                
                if not rule_vars:
                    # 无变量规则: 直接匹配
                    parts = [p.strip() for p in premise.split(' AND ')]
                    if all(p in derived for p in parts):
                        if conclusion not in derived:
                            derived.add(conclusion)
                            chain.append(f"{name}: {premise} -> {conclusion}")
                            changed = True
                else:
                    # 有变量规则: 对每个已知事实尝试匹配
                    for fact in list(derived):
                        for var in rule_vars:
                            # 检查premise模板是否能匹配已知事实
                            pred_name = premise.split('(')[0] if '(' in premise else premise
                            if fact.startswith(pred_name):
                                # 提取事实中的具体值
                                val = fact.split('(')[1].rstrip(')') if '(' in fact else ''
                                if val:
                                    # 替换结论中的变量
                                    sub_conclusion = conclusion.replace(f'({var})', f'({val})')
                                    if sub_conclusion not in derived:
                                        derived.add(sub_conclusion)
                                        chain.append(f"{name}({var}={val}): {premise} -> {conclusion}")
                                        changed = True
        
        return query in derived, chain


if __name__ == '__main__':
    print("🧠 染色体10 逻辑推理部 验证")
    
    # 1. SymbolicEngine测试
    eng = SymbolicEngine()
    eng.add_var('x', 'int', (0, 100))
    eng.add_var('y', 'int', (0, 100))
    eng.add_constraint('x <= 50')
    eng.add_constraint('y >= 20')
    eng.add_constraint('x + y <= 80')
    sol = eng.solve()
    print(f"  SymbolicEngine: x in {sol.get('x')}, y in {sol.get('y')}")
    assert sol['x'][1] <= 50, "Constraint inference failed"
    
    # 2. Contract测试
    check = ContractDecorator.precondition(lambda x: x > 0)
    
    @check
    def sqrt_approx(x):
        return x ** 0.5
    
    result = sqrt_approx(4)
    print(f"  Contract: sqrt_approx(4) = {result}")
    try:
        sqrt_approx(-1)
        print("  Contract: ❌ should have raised ValueError")
    except ValueError:
        print("  Contract: ✅ precondition enforced")
    
    # 3. LogicReasoner测试
    lr = LogicReasoner()
    lr.add_fact("man(Socrates)")
    lr.add_rule("mortal_rule", "man(X)", "mortal(X)")
    proved, chain = lr.reason("mortal(Socrates)")
    print(f"  Logic: mortal(Socrates) = {proved}")
    print(f"  Chain: {' -> '.join(chain)}")
    assert proved, "Logic reasoner failed"
    
    print("\n✅ 染色体10 逻辑推理部 验证通过")
