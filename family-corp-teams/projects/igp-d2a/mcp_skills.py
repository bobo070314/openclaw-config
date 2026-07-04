"""
IGP-MCP Skills系统
标准化可安装技能包，兼容Agent Skills SKILL.md规范
"""
import os, json, sys
from datetime import datetime

FAMILY = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams"
PROJECTS = os.path.join(FAMILY, 'projects')

class SkillRegistry:
    """Skill注册中心"""
    
    def __init__(self):
        self.skills = {}
        self._discover()
    
    def _discover(self):
        """扫描所有项目，发现技能"""
        for p in sorted(os.listdir(PROJECTS)):
            pp = os.path.join(PROJECTS, p)
            if not os.path.isdir(pp):
                continue
            py_files = [f for f in os.listdir(pp) if f.endswith('.py')]
            for f in py_files:
                fp = os.path.join(pp, f)
                content = open(fp, encoding='utf-8').read()
                funcs = []
                for line in content.split('\n'):
                    s = line.strip()
                    if s.startswith('def '):
                        funcs.append(s.split('def ')[1].split('(')[0].strip())
                
                if funcs:
                    skill_name = f'{p}/{f.replace(".py","")}'
                    self.skills[skill_name] = {
                        'path': os.path.relpath(fp, FAMILY),
                        'functions': funcs,
                        'has_main': '__main__' in content,
                        'lines': len(content.split('\n')),
                    }
    
    def list_skills(self, filter_str=''):
        if filter_str:
            return {k: v for k, v in self.skills.items() if filter_str in k}
        return self.skills
    
    def get_skill(self, name):
        return self.skills.get(name, {})
    
    def search_function(self, func_name):
        results = {}
        for name, info in self.skills.items():
            if func_name in info['functions']:
                results[name] = info
        return results


def main():
    registry = SkillRegistry()
    skills = registry.list_skills()
    
    # 统计
    total_funcs = sum(len(s['functions']) for s in skills.values())
    print(json.dumps({
        'skills': len(skills),
        'functions': total_funcs,
        'projects': len(set(k.split('/')[0] for k in skills.keys())),
        'status': 'skills_ok',
    }))

if __name__ == '__main__':
    main()
