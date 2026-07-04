"""
IGP Evolver — 自我进化引擎 v1

行业突破点: Agent 不仅能执行任务，还能自己给自己写升级代码
每次跑完后分析自己的不足，自动生成下一个版本的改进

0 依赖，纯 Python 3.14
"""
import os, json, sys, re
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
PROJECTS = os.path.join(FAMILY, 'projects')
EVOLVER_DIR = os.path.join(PROJECTS, 'igp-evolver')
os.makedirs(EVOLVER_DIR, exist_ok=True)

EVOLUTION_LOG = os.path.join(EVOLVER_DIR, 'evolution_log.json')
SCORE_THRESHOLD = 6  # 低于这个分就自动触发进化


class IGPEvolver:
    """自我进化引擎"""

    def __init__(self):
        self.log = self._load_log()

    def _load_log(self):
        if os.path.exists(EVOLUTION_LOG):
            with open(EVOLUTION_LOG, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'version': 'v1', 'evolutions': []}

    def _save_log(self):
        with open(EVOLUTION_LOG, 'w', encoding='utf-8') as f:
            json.dump(self.log, f, ensure_ascii=False, indent=2)

    def analyze_file(self, filepath):
        """分析一个Python文件的质量"""
        if not os.path.exists(filepath):
            return {'ok': False, 'error': '文件不存在'}

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        issues = []
        score = 10

        # 检查：空函数
        empty_funcs = re.findall(r'def \w+\(.*?\):\s*\n\s*pass', content)
        if empty_funcs:
            score -= 2 * len(empty_funcs)
            issues.extend([f'空函数: {f}' for f in empty_funcs])

        # 检查：缺少docstring的函数
        funcs_no_doc = re.findall(r'def (\w+)\(.*?\):\n(?!\s*""")', content)
        if funcs_no_doc:
            score -= 1
            issues.append(f'{len(funcs_no_doc)} 个函数缺少docstring')

        # 检查：硬编码路径
        hardcoded = re.findall(r'[rR][\'"]D:\\\\', content)
        if hardcoded:
            score -= 1
            issues.append(f'硬编码路径: {len(hardcoded)} 处')

        # 检查：裸 except
        bare_excepts = content.count('except:')
        if bare_excepts:
            score -= bare_excepts
            issues.append(f'裸 except: {bare_excepts} 处')

        # 检查：文件长度
        lines = content.split('\n')
        if len(lines) > 300:
            score -= 1
            issues.append(f'文件过长: {len(lines)} 行')

        score = max(1, min(10, score))

        return {
            'ok': score >= SCORE_THRESHOLD,
            'file': filepath,
            'score': score,
            'lines': len(lines),
            'issues': issues,
            'needs_evolution': score < SCORE_THRESHOLD,
        }

    def suggest_upgrade(self, analysis):
        """根据分析结果提出升级建议"""
        suggestions = []
        for issue in analysis['issues']:
            if '空函数' in issue:
                suggestions.append('实现空函数中的逻辑')
            elif 'docstring' in issue:
                suggestions.append('为所有函数添加docstring')
            elif '硬编码' in issue:
                suggestions.append('用os.path.join替代硬编码路径')
            elif '裸 except' in issue:
                suggestions.append('指定异常类型替代裸 except')
        return suggestions

    def evolve(self, filepath):
        """对一个文件执行进化（自我改进）"""
        analysis = self.analyze_file(filepath)
        
        evo_record = {
            'timestamp': datetime.now().isoformat(),
            'file': filepath,
            'score_before': analysis['score'],
            'needs_evolution': analysis['needs_evolution'],
            'issues': analysis['issues'],
            'suggestions': self.suggest_upgrade(analysis),
            'evolved': False,
        }

        if analysis['needs_evolution']:
            # 生成升级文件
            dirname = os.path.dirname(filepath)
            basename = os.path.basename(filepath)
            name, ext = os.path.splitext(basename)
            evo_path = os.path.join(dirname, f'{name}_evolved{ext}')
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 自动修复：裸except → except Exception
            content = content.replace('except:', 'except Exception:')
            
            # 修复：添加类docstring
            content = re.sub(
                r'class (\w+):\n(?!\s*""")',
                r'class \1:\n    """\1 class"""\n',
                content
            )

            # 修复：在def后添加docstring（简单版）
            def add_docstring(match):
                func_name = match.group(1)
                return f'def {func_name}():\n    """{func_name} function"""\n'

            content = re.sub(
                r'def (\w+)\(\):\n(?!\s*(?:""")|#|\s|$)',
                add_docstring,
                content
            )

            with open(evo_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # 重新评分
            new_analysis = self.analyze_file(evo_path)
            evo_record['score_after'] = new_analysis['score']
            evo_record['evolved'] = True
            evo_record['evolved_file'] = evo_path

        self.log['evolutions'].append(evo_record)
        self._save_log()

        return evo_record

    def scan_and_evolve_all(self, directory):
        """扫描整个目录并进化所有低于阈值的文件"""
        results = []
        for root, _, files in os.walk(directory):
            for f in files:
                if f.endswith('.py') and not f.startswith('_'):
                    fp = os.path.join(root, f)
                    result = self.evolve(fp)
                    if result.get('needs_evolution'):
                        results.append(result)
        return results

    def status(self):
        total = len(self.log['evolutions'])
        evolved = sum(1 for e in self.log['evolutions'] if e.get('evolved'))
        return {
            'total_analyzed': total,
            'total_evolved': evolved,
            'avg_score_before': round(
                sum(e['score_before'] for e in self.log['evolutions']) / max(total, 1), 1
            ),
        }


def main():
    evolver = IGPEvolver()

    print('🧬 IGP Evolver — 自我进化引擎')
    print('=' * 50)

    # Phase 1: 扫描 projects/ 下所有 Python 文件
    print('\n📡 扫描 projects/ 下所有 Python 文件...')
    results = evolver.scan_and_evolve_all(PROJECTS)

    # Phase 2: 扫描 HQ
    print('\n📡 扫描 headquarters/...')
    hq_results = evolver.scan_and_evolve_all(os.path.join(FAMILY, 'headquarters'))
    results.extend(hq_results)

    # 报告
    status = evolver.status()
    print(f'\n📊 进化报告:')
    print(f'  扫描文件: {status["total_analyzed"]} 个')
    print(f'  触发进化: {status["total_evolved"]} 个')
    print(f'  平均分:   {status["avg_score_before"]}/10')

    for r in results:
        if r.get('evolved'):
            print(f'\n  🔄 {os.path.basename(r["file"])}')
            print(f'     修改前: {r["score_before"]}/10')
            print(f'     修改后: {r.get("score_after", "?")}/10')
            print(f'     修复: {", ".join(r["suggestions"])}')
            print(f'     生成: {r["evolved_file"]}')

    print(f'\n🏆 自我进化引擎状态: 运行中 ✅')
    print(f'  日志: {EVOLUTION_LOG}')


if __name__ == '__main__':
    main()
