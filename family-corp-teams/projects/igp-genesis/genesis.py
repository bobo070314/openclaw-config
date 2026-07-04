"""
IGP Genesis — Agent 自我复制引擎 v1

灵感: 生物细胞分裂 → Agent可以从模板自动生成新Agent
行业突破点: 不是手动创建每个部门，而是一个Agent自动复制出整个组织

0 依赖，纯 Python 3.14
"""
import os, sys, json, shutil
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
PROJECTS = os.path.join(FAMILY, 'projects')
GENESIS_DIR = os.path.join(PROJECTS, 'igp-genesis')
os.makedirs(GENESIS_DIR, exist_ok=True)


AGENT_TEMPLATE = '''"""
{agent_name} — 由 IGP Genesis 自我复制生成
母体: {parent}
生成时间: {timestamp}
"""
import os, sys, json
from datetime import datetime

class {class_name}:
    """{description}"""
    
    def __init__(self):
        self.name = "{agent_name}"
        self.parent = "{parent}"
        self.created = "{timestamp}"
        self.status = "active"
        self.task_list = {tasks_json}
    
    def identify(self):
        return {{
            "name": self.name,
            "parent": self.parent,
            "generation": {generation},
            "status": self.status,
            "tasks": len(self.task_list)
        }}
    
    def work(self):
        result = {{
            "agent": self.name,
            "action": "auto_generated_work",
            "tasks_completed": 0,
            "status": "ok"
        }}
        return result

if __name__ == "__main__":
    agent = {class_name}()
    print(json.dumps(agent.identify(), indent=2))
    print(json.dumps(agent.work(), indent=2))
'''


class GenesisEngine:
    """Agent 自我复制引擎"""

    def __init__(self):
        self.generation = 0
        self.agents = {}
        self._load_lineage()

    def _load_lineage(self):
        lineage_path = os.path.join(GENESIS_DIR, 'lineage.json')
        if os.path.exists(lineage_path):
            with open(lineage_path, 'r', encoding='utf-8') as f:
                self.agents = json.load(f)
                self.generation = max(
                    (a.get('generation', 0) for a in self.agents.values()),
                    default=0
                )
        else:
            # 第一个 Agent — 原初
            self.agents['nexus-core'] = {
                'name': 'nexus-core',
                'parent': 'bigbang',
                'generation': 0,
                'created': datetime.now().isoformat(),
                'description': 'IGP 原初 Agent — 万物起点',
            }
            self._save_lineage()

    def _save_lineage(self):
        lineage_path = os.path.join(GENESIS_DIR, 'lineage.json')
        with open(lineage_path, 'w', encoding='utf-8') as f:
            json.dump(self.agents, f, ensure_ascii=False, indent=2)

    def spawn(self, name, parent, description, tasks=None):
        """从母体 Agent 生成一个新 Agent"""
        if parent not in self.agents:
            return {'error': f'母体 {parent} 不存在'}

        parent_info = self.agents[parent]
        new_gen = parent_info['generation'] + 1

        # 生成类名
        class_name = ''.join(w.capitalize() for w in name.replace('-', ' ').split())

        # 生成代码
        code = AGENT_TEMPLATE.format(
            agent_name=name,
            parent=parent,
            timestamp=datetime.now().isoformat(),
            class_name=class_name,
            description=description,
            generation=new_gen,
            tasks_json=json.dumps(tasks or ['self_diagnose']),
        )

        # 写入文件
        file_name = name.replace('-', '_') + '.py'
        file_path = os.path.join(GENESIS_DIR, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)

        # 注册到谱系
        self.agents[name] = {
            'name': name,
            'parent': parent,
            'generation': new_gen,
            'created': datetime.now().isoformat(),
            'description': description,
            'file': file_name,
        }
        self._save_lineage()

        return {
            'status': 'spawned',
            'name': name,
            'generation': new_gen,
            'parent': parent,
            'file': file_path,
        }

    def spawn_many(self, agent_defs):
        """批量生成多个 Agent"""
        results = []
        for ad in agent_defs:
            result = self.spawn(**ad)
            results.append(result)
        return results

    def status(self):
        total = len(self.agents)
        max_gen = max(a['generation'] for a in self.agents.values())
        return {
            'agents': total,
            'generations': max_gen,
            'lineage': self.agents,
        }


def main():
    engine = GenesisEngine()

    print('🧬 IGP Genesis — Agent 自我复制引擎')
    print('=' * 50)

    # 当前状态
    status = engine.status()
    print(f'\n当前谱系: {status["agents"]} 个 Agent, {status["generations"]} 代')
    for name, info in status['lineage'].items():
        gen = info['generation']
        bar = '█' * (gen + 1) + '░' * (5 - gen)
        print(f'  Gen{gen} {bar} {name} ← {info["parent"]}')

    # 第1波复制: Nexus → 12部门 Agent
    print(f'\n🚀 第1波复制: Nexus → 12部门 Agent')
    dept_agents = [
        {'name': f'dept-{d}', 'parent': 'nexus-core',
         'description': f'{d} 部门自动生成 Agent',
         'tasks': [f'process_{d}_tasks', 'self_diagnose', 'report_to_nexus']}
        for d in ['frontend', 'backend', 'infra', 'ai', 'mobile', 'design',
                  'quality', 'pmo', 'growth', 'data', 'tech-support', 'compliance']
    ]
    results = engine.spawn_many(dept_agents)

    ok = sum(1 for r in results if 'error' not in r)
    fail = sum(1 for r in results if 'error' in r)
    print(f'  成功: {ok} / 失败: {fail}')
    for r in results:
        if 'error' not in r:
            print(f'    ✅ Gen{r["generation"]} {r["name"]} ← {r["parent"]}')
        else:
            print(f'    ❌ {r["error"]}')

    # 验证每个生成的 Agent 可执行
    print(f'\n🧪 验证: 随机测试 3 个新 Agent...')
    import random
    test_samples = random.sample([r for r in results if 'error' not in r], min(3, ok))
    for sample in test_samples:
        file_path = os.path.join(GENESIS_DIR, sample['name'].replace('-', '_') + '.py')
        r = os.system(f'"{sys.executable}" "{file_path}" >nul 2>&1')
        sym = '✅' if r == 0 else '❌'
        print(f'  {sym} {sample["name"]} (exit: {r})')

    final_status = engine.status()
    print(f'\n🏆 最终谱系:')
    print(f'  Total: {final_status["agents"]} Agents')
    print(f'  Generations: {final_status["generations"]}')
    print(f'  自我复制: {"已实现 ✅" if ok > 0 else "失败 ❌"}')
    print(f'  目录: {GENESIS_DIR}')
    print(f'  文件数: {len([f for f in os.listdir(GENESIS_DIR) if f.endswith(".py")])} 个 Agent 文件')


if __name__ == '__main__':
    main()
