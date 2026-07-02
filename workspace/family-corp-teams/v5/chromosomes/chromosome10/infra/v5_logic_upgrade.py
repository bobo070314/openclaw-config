"""
v5 Logic Reasoner Upgrade — chromosome10

Modules: SymbolicEngineV2, ContractDecoratorV2, KnowledgeBase, LogicReasonerV2
"""
import os, sys, json, time, itertools, hashlib
from collections import defaultdict

# ============================================================
# KnowledgeBase: persistent fact/rule storage
# ============================================================
class KnowledgeBase:
    """Persistent fact/rule knowledge base backed by JSON file"""
    
    def __init__(self, path=None):
        self.path = path or os.path.join(os.path.dirname(__file__), 'kb_store.json')
        self.facts = {}    # {fact_id: {predicate, args, timestamp, confidence}}
        self.rules = []    # [{antecedent: [...], consequent: {...}, name, weight}]
        self._load()
    
    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.facts = data.get('facts', {})
                self.rules = data.get('rules', [])
    
    def _save(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump({'facts': self.facts, 'rules': self.rules}, f, indent=2, ensure_ascii=False)
    
    def add_fact(self, predicate, *args, confidence=1.0):
        """Add a fact with optional confidence score"""
        fid = hashlib.md5(f"{predicate}({','.join(str(a) for a in args)})".encode()).hexdigest()[:12]
        self.facts[fid] = {
            'predicate': predicate,
            'args': list(args),
            'confidence': confidence,
            'timestamp': time.time(),
        }
        self._save()
        return fid
    
    def add_rule(self, antecedents, consequent, name='', weight=1.0):
        """Add an inference rule: if ALL antecedents match, THEN consequent"""
        rule = {
            'id': hashlib.md5(f"rule_{name}_{time.time()}".encode()).hexdigest()[:8],
            'name': name,
            'antecedents': antecedents,  # list of {predicate, args}
            'consequent': consequent,      # {predicate, args}
            'weight': weight,
        }
        self.rules.append(rule)
        self._save()
        return rule['id']
    
    def query(self, predicate=None):
        """Query facts by predicate"""
        if predicate:
            return {fid: f for fid, f in self.facts.items() if f['predicate'] == predicate}
        return dict(self.facts)
    
    def clear(self):
        self.facts.clear()
        self.rules.clear()
        self._save()


# ============================================================
# SymbolicEngine v2: string/bool/set constraints + backtracking
# ============================================================
class SymbolicEngineV2:
    """Symbolic constraint solver supporting int, string, bool, set types"""
    
    def __init__(self):
        self.variables = {}  # {name: {type, domain, constraints}}
        self.backtrack_limit = 10000
    
    def declare(self, name, var_type='int', domain=None):
        """Declare a symbolic variable"""
        self.variables[name] = {
            'type': var_type,
            'domain': domain or self._default_domain(var_type),
            'constraints': [],
        }
    
    def _default_domain(self, var_type):
        return {
            'int': list(range(-100, 101)),
            'bool': [True, False],
            'string': [],
            'set': [],
        }.get(var_type, [])
    
    def add_constraint(self, expr):
        """Add a constraint expression (lambda or string)"""
        for var_info in self.variables.values():
            var_info['constraints'].append(expr)
    
    def solve(self, max_solutions=1):
        """Solve constraints via backtracking"""
        var_names = list(self.variables.keys())
        if not var_names:
            return [{}]
        
        solutions = []
        domains = [self.variables[n]['domain'][:] for n in var_names]
        
        def backtrack(idx, assignment):
            if len(solutions) >= max_solutions:
                return
            if idx == len(var_names):
                # Check all constraints
                for var_info in self.variables.values():
                    for c in var_info['constraints']:
                        try:
                            if callable(c):
                                if not c(assignment):
                                    return
                        except Exception:
                            return
                solutions.append(dict(assignment))
                return
            
            name = var_names[idx]
            for val in domains[idx][:min(len(domains[idx]), self.backtrack_limit // len(var_names or 1))]:
                assignment[name] = val
                backtrack(idx + 1, assignment)
                del assignment[name]
                if len(solutions) >= max_solutions:
                    return
        
        backtrack(0, {})
        return solutions


# ============================================================
# ContractDecorator v2: forall/exists + batch validation
# ============================================================
class ContractDecoratorV2:
    """Design-by-contract: pre/post/invariant with quantifiers"""
    
    def __init__(self):
        self.contracts = []
        self.invariants = []
    
    def precondition(self, condition, description=''):
        """Decorator: check condition before function executes"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not condition(*args, **kwargs):
                    raise AssertionError(f"Precondition failed: {description}")
                return func(*args, **kwargs)
            wrapper.__name__ = func.__name__
            return wrapper
        return decorator
    
    def postcondition(self, condition, description=''):
        """Decorator: check condition on return value"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if not condition(result, *args, **kwargs):
                    raise AssertionError(f"Postcondition failed: {description}")
                return result
            wrapper.__name__ = func.__name__
            return wrapper
        return decorator
    
    def invariant(self, condition, description=''):
        """Register a class invariant"""
        self.invariants.append((condition, description))
    
    def check_invariants(self, instance):
        """Batch check all invariants on an instance"""
        failures = []
        for cond, desc in self.invariants:
            try:
                if not cond(instance):
                    failures.append(desc)
            except Exception as e:
                failures.append(f"{desc}: {e}")
        return failures
    
    def forall(self, iterable, condition):
        """Forall quantifier: ALL elements satisfy condition"""
        return all(condition(x) for x in iterable)
    
    def exists(self, iterable, condition):
        """Exists quantifier: at least ONE element satisfies condition"""
        return any(condition(x) for x in iterable)


# ============================================================
# LogicReasoner v2: depth-unlimited inference + KB
# ============================================================
class LogicReasonerV2:
    """First-order logic reasoner with unlimited depth and persistent KB"""
    
    def __init__(self, kb=None):
        self.kb = kb or KnowledgeBase()
        self.max_depth = 1000  # essentially unlimited
    
    def forward_chain(self, max_iterations=100):
        """Forward chaining: apply rules to derive new facts"""
        derived = []
        for _ in range(min(max_iterations, self.max_depth)):
            new_facts = 0
            for rule in self.kb.rules:
                antecedents = rule['antecedents']
                consequent = rule['consequent']
                # Check if ALL antecedents match existing facts
                match = True
                for ant in antecedents:
                    matching_facts = self.kb.query(ant['predicate'])
                    if not matching_facts:
                        match = False
                        break
                if match:
                    # Add consequent as fact
                    fid = self.kb.add_fact(consequent['predicate'], *consequent.get('args', []), confidence=rule['weight'])
                    derived.append(fid)
                    new_facts += 1
            if new_facts == 0:
                break
        return derived
    
    def backward_chain(self, goal_predicate, goal_args=None, depth=0):
        """Backward chaining: find proof for a goal"""
        if depth > self.max_depth:
            return None
        
        goal_args = goal_args or []
        # Check if goal is already a fact
        matching = self.kb.query(goal_predicate)
        for fid, fact in matching.items():
            if fact['args'] == list(goal_args) and fact['confidence'] > 0:
                return [fid]
        
        # Search rules whose consequent matches goal
        for rule in self.kb.rules:
            cons = rule['consequent']
            if cons['predicate'] == goal_predicate:
                # Try to prove all antecedents
                proof = []
                for ant in rule['antecedents']:
                    sub_proof = self.backward_chain(ant['predicate'], ant.get('args', []), depth + 1)
                    if sub_proof is None:
                        break
                    proof.extend(sub_proof)
                else:
                    # All antecedents proven
                    derived = self.kb.add_fact(goal_predicate, *goal_args, confidence=rule['weight'])
                    proof.append(derived)
                    return proof
        return None
    
    def explain(self, fact_id):
        """Explain how a fact was derived"""
        fact = self.kb.facts.get(fact_id)
        if not fact:
            return "Fact not found"
        matching_rules = []
        for rule in self.kb.rules:
            cons = rule['consequent']
            if cons['predicate'] == fact['predicate']:
                matching_rules.append(rule)
        if matching_rules:
            return {
                'fact': fact,
                'derived_by': [r['name'] for r in matching_rules],
            }
        return {'fact': fact, 'derived_by': 'axiom'}


if __name__ == '__main__':
    # Quick self-test
    print("Testing LogicReasonerV2...")
    
    # Test KB
    kb = KnowledgeBase(path=os.path.join(os.path.dirname(__file__), 'kb_test.json'))
    kb.clear()
    kb.add_fact('mortal', 'socrates', confidence=1.0)
    kb.add_fact('human', 'socrates', confidence=1.0)
    kb.add_rule(
        [{'predicate': 'human', 'args': ['X']}],
        {'predicate': 'mortal', 'args': ['X']},
        name='all_humans_are_mortal',
        weight=0.9
    )
    
    # Test SymbolicEngineV2
    se = SymbolicEngineV2()
    se.declare('x', 'int')
    se.declare('y', 'int')
    se.variables['x']['domain'] = list(range(10))
    se.variables['y']['domain'] = list(range(10))
    se.add_constraint(lambda a: a['x'] + a['y'] == 10)
    se.add_constraint(lambda a: a['x'] > a['y'])
    sols = se.solve(max_solutions=3)
    print(f"  SymbolicEngine: {len(sols)} solutions (x+y=10, x>y)")
    
    # Test ContractDecoratorV2
    cd = ContractDecoratorV2()
    
    @cd.precondition(lambda x, y: x >= 0 and y >= 0, 'x and y must be non-negative')
    @cd.postcondition(lambda r, x, y: r >= 0, 'result must be non-negative')
    def add_positive(x, y):
        return x + y
    
    assert add_positive(3, 4) == 7
    try:
        add_positive(-1, 5)
        print("  WARNING: precondition should have failed!")
    except AssertionError:
        print("  ContractDecorator: precondition check OK")
    
    # Test forward chaining
    lr = LogicReasonerV2(kb)
    derived = lr.forward_chain()
    print(f"  Forward chaining: derived {len(derived)} new facts")
    
    # Test backward chaining
    proof = lr.backward_chain('mortal', ['socrates'])
    print(f"  Backward chaining: proof {'found' if proof else 'failed'}")
    
    # Cleanup test KB
    kb.clear()
    if os.path.exists(kb.path):
        os.remove(kb.path)
    
    print("=== [DONE] Logic Reasoner UPGRADE ===")
