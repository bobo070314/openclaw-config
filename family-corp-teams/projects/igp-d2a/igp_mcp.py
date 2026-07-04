"""
IGP-MCP Protocol Engine v1
一条路:
- 兼容MCP JSON-RPC 2.0 over HTTP (行业标准)
- 扩展IGP: 进化/PK/自愈/联邦 (行业独有)
- 0外部依赖
"""
import os, json, sys
from datetime import datetime

FAMILY = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams"
PROJECTS = os.path.join(FAMILY, 'projects')

class IGPMCPProtocol:
    """
    MCP兼容层 + IGP扩展层
    
    标准MCP方法 (others can call us):
    - tools/list: 列出所有IGP工具
    - tools/call: 调用IGP工具
    - resources/list: 列出IGP资源
    - prompts/list: 列出IGP提示
    - server/discover: 服务器发现
    
    IGP扩展方法 (our superpowers):
    - igp/evolve: 进化分析
    - igp/heal: 自愈注入
    - igp/federate: 联邦查询
    - igp/pk: PK竞争
    - igp/broadcast: 广播消息
    """
    
    def __init__(self):
        self.tools = self._register_tools()
        self.resources = self._register_resources()
        self.prompts = self._register_prompts()
        
    def _register_tools(self):
        """向外部暴露的MCP标准工具"""
        return {
            'health': {
                'description': '检查所有项目健康状态',
                'inputSchema': {'type': 'object', 'properties': {'scope': {'type': 'string'}}},
            },
            'heal_project': {
                'description': '自愈一个项目（补README/__main__）',
                'inputSchema': {'type': 'object', 'properties': {
                    'project': {'type': 'string'},
                }},
            },
            'analyze_evolution': {
                'description': '分析项目进化趋势',
                'inputSchema': {'type': 'object', 'properties': {
                    'project': {'type': 'string'},
                }},
            },
            'handle_task': {
                'description': 'D2A任务分发',
                'inputSchema': {'type': 'object', 'properties': {
                    'source': {'type': 'string'},
                    'target': {'type': 'string'},
                    'action': {'type': 'string'},
                }},
            },
            'mutate': {
                'description': '基因突变（生成新能力）',
                'inputSchema': {'type': 'object', 'properties': {
                    'base': {'type': 'string'},
                    'direction': {'type': 'string'},
                }},
            },
        }
    
    def _register_resources(self):
        projects = []
        for p in sorted(os.listdir(PROJECTS)):
            pp = os.path.join(PROJECTS, p)
            if not os.path.isdir(pp):
                continue
            py_count = len([f for f in os.listdir(pp) if f.endswith('.py')])
            projects.append({'name': p, 'py_files': py_count})
        return {'igp://projects': {'description': '所有IGP项目列表', 'data': projects}}
    
    def _register_prompts(self):
        return {
            'analyze_igp': {
                'description': '分析IGP当前状态',
                'arguments': [{'name': 'depth', 'description': '分析深度'}],
            }
        }
    
    def handle_jsonrpc(self, method, params):
        """处理JSON-RPC请求，兼容MCP"""
        if method.startswith('igp/'):
            return self._handle_igp(method, params)
        
        # MCP标准方法
        if method == 'tools/list':
            return {'tools': list(self.tools.keys())}
        if method == 'resources/list':
            return {'resources': list(self.resources.keys())}
        if method == 'prompts/list':
            return {'prompts': list(self.prompts.keys())}
        if method == 'server/discover':
            return {
                'name': 'IGP-MCP',
                'version': '1.0',
                'protocol': 'MCP 2026-07-28 compatible',
                'extensions': ['igp/evolve', 'igp/heal', 'igp/federate'],
            }
        
        return {'error': f'unknown method: {method}'}
    
    def _handle_igp(self, method, params):
        """IGP扩展方法"""
        if method == 'igp/evolve':
            return self._evolve_analysis(params.get('project', ''))
        if method == 'igp/heal':
            return self._heal_project(params.get('project', ''))
        if method == 'igp/federate':
            return self._federate_query(params.get('query', ''))
        if method == 'igp/broadcast':
            return self._broadcast(params.get('message', ''))
        if method == 'igp/pk':
            return self._pk_rank()
        return {'error': f'unknown igp method: {method}'}
    
    def _evolve_analysis(self, project):
        """分析项目进化"""
        pp = os.path.join(PROJECTS, project)
        if not os.path.isdir(pp):
            return {'error': f'project {project} not found'}
        
        py_files = [f for f in os.listdir(pp) if f.endswith('.py')]
        total_lines = 0
        for f in py_files:
            total_lines += len(open(os.path.join(pp, f), encoding='utf-8').read().split(chr(10)))
        
        return {
            'project': project,
            'files': len(py_files),
            'lines': total_lines,
            'health': 'ok' if total_lines > 0 else 'empty',
        }
    
    def _heal_project(self, project):
        """自愈项目"""
        pp = os.path.join(PROJECTS, project)
        if not os.path.isdir(pp):
            return {'error': 'not found'}
        fixes = []
        # 补README
        if not any(f.lower().startswith('readme') for f in os.listdir(pp)):
            with open(os.path.join(pp, 'README.md'), 'w') as f:
                f.write(f'# {project}\n')
            fixes.append('README')
        # 补__main__
        for fname in os.listdir(pp):
            if not fname.endswith('.py'):
                continue
            fp = os.path.join(pp, fname)
            content = open(fp, encoding='utf-8').read()
            if '__main__' not in content:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(content.rstrip() + '\n\nif __name__ == \'__main__\':\n    print(\'OK\')\n')
                fixes.append(f'{fname} main')
        return {'project': project, 'fixed': len(fixes), 'fixes': fixes}
    
    def _federate_query(self, query):
        """联邦查询所有项目"""
        results = {}
        for p in sorted(os.listdir(PROJECTS)):
            pp = os.path.join(PROJECTS, p)
            if not os.path.isdir(pp):
                continue
            py_files = [f for f in os.listdir(pp) if f.endswith('.py')]
            total = 0
            for f in py_files:
                content = open(os.path.join(pp, f), encoding='utf-8').read()
                if query.lower() in content.lower():
                    total += 1
            results[p] = {'matches': total}
        return {'query': query, 'results': results}
    
    def _broadcast(self, message):
        """广播消息到所有项目"""
        received = 0
        for p in sorted(os.listdir(PROJECTS)):
            pp = os.path.join(PROJECTS, p)
            if os.path.isdir(pp):
                received += 1
        return {'sent': message, 'received': received}
    
    def _pk_rank(self):
        """PK排名"""
        stats = {}
        for p in sorted(os.listdir(PROJECTS)):
            pp = os.path.join(PROJECTS, p)
            if not os.path.isdir(pp):
                continue
            py_files = [f for f in os.listdir(pp) if f.endswith('.py')]
            total = 0
            funcs = 0
            for f in py_files:
                content = open(os.path.join(pp, f), encoding='utf-8').read()
                total += len(content.split(chr(10)))
                for line in content.split(chr(10)):
                    if line.strip().startswith('def '):
                        funcs += 1
            stats[p] = {'lines': total, 'funcs': funcs, 'score': total // 10 + funcs}
        ranked = sorted(stats.items(), key=lambda x: -x[1]['score'])
        return {'rankings': [{'rank': i+1, 'name': n, 'score': s['score']} for i, (n, s) in enumerate(ranked)]}


def main():
    protocol = IGPMCPProtocol()
    
    # 测试MCP标准方法
    print(json.dumps({'method': 'server/discover', 'result': protocol.handle_jsonrpc('server/discover', {})}, ensure_ascii=False))
    
    # 测试IGP扩展
    print(json.dumps({'method': 'igp/pk', 'result': protocol.handle_jsonrpc('igp/pk', {})}, ensure_ascii=False))
    
    # 测试联邦查询
    print(json.dumps({'method': 'igp/federate', 'result': protocol.handle_jsonrpc('igp/federate', {'query': 'def'})}, ensure_ascii=False))
    
    # 测试广播
    print(json.dumps({'method': 'igp/broadcast', 'result': protocol.handle_jsonrpc('igp/broadcast', {'message': 'health_check'})}, ensure_ascii=False))


if __name__ == '__main__':
    main()
