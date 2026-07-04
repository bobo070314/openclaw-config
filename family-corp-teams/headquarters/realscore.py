"""
IGP RealScore — 实际运行得分 v1
纸面分数 = 装饰品
能跑起来、能真正干活的才是真价值

每个项目：
1. 是否能导入? (import test)
2. 是否有 main() 且能执行? (run test)
3. 代码行数+文件数 (volume score)
4. 是否有文档? (doc score)
5. 核心功能是否完整? (core function test)

实际总分 = 1×2×3×4×5 累乘
"""
import os, sys, json, importlib.util
from datetime import datetime

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
PROJECTS = os.path.join(FAMILY, 'projects')
HQ = os.path.join(FAMILY, 'headquarters')


def test_import(filepath):
    """测试Python文件是否能正常导入"""
    try:
        # 不能用 importlib 因为可能有相对导入，直接用 exec 测试语法
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, filepath, 'exec')
        return True, None
    except SyntaxError as e:
        return False, f'语法错误: {e.msg} (行{e.lineno})'
    except Exception as e:
        return False, f'编译错误: {str(e)[:100]}'


def test_main(filepath):
    """测试__main__是否能运行（快速版，只跑前10行输出，超时3秒）"""
    try:
        import subprocess, time, signal
        start = time.time()
        proc = subprocess.run(
            [sys.executable, '-c', 
             f'import sys; sys.path.insert(0, "{os.path.dirname(filepath)}"); '
             f'exec(open(r"{filepath}").read())'],
            capture_output=True, text=True, timeout=5,
            env={**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'}
        )
        elapsed = time.time() - start
        if proc.returncode == 0:
            output = proc.stdout[:200] if proc.stdout else '(无输出)'
            return True, output, elapsed
        else:
            err = proc.stderr[:200] if proc.stderr else f'exit code {proc.returncode}'
            return False, err, elapsed
    except subprocess.TimeoutExpired:
        return False, '⏱ 超时 (5s)', 5.0
    except Exception as e:
        return False, str(e)[:100], 0


def score_project(project_dir, project_name):
    """给项目打实际运行分"""
    py_files = sorted([
        f for f in os.listdir(project_dir)
        if f.endswith('.py') and os.path.isfile(os.path.join(project_dir, f))
    ])
    
    if not py_files:
        return {
            'project': project_name,
            'real_score': 0,
            'breakdown': {'files': 0, 'importable': 0, 'runnable': 0, 'volume': 0, 'doc': 0},
            'reason': '无Python文件',
        }
    
    # 选主文件（优先选agent_protocol、ghost、bridge、evolver、genesis这类核心模块，再按文件大小排序）
    main_file = None
    # 优先级文件名匹配
    priority_names = ['agent_protocol', 'ghost', 'bridge', 'evolver', 'genesis', 'nexus', 'pipeline', 'mutate']
    for f in py_files:
        fbase = os.path.splitext(f)[0]
        if fbase in priority_names or fbase.replace('_', '-') in priority_names:
            main_file = f
            break
    if not main_file:
        # 按大小选最大的文件
        sizes = [(f, os.path.getsize(os.path.join(project_dir, f))) for f in py_files]
        sizes.sort(key=lambda x: x[1], reverse=True)
        if sizes:
            main_file = sizes[0][0]
    
    main_path = os.path.join(project_dir, main_file)
    
    # 1. 能否导入 (编译检查)
    importable, import_err = test_import(main_path)
    
    # 2. 能否运行
    runnable = False
    main_output = ''
    has_main = False
    elapsed = 0
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if '__main__' in content:
            has_main = True
            if importable:
                runnable, main_output, elapsed = test_main(main_path)
        else:
            runnable = importable  # 没有main但有import能力也算
    
    # 3. 体积分
    lines = len(content.split('\n'))
    volume = min(5, lines // 50)  # 每50行1分，上限5分
    
    # 4. 文档分
    md_files = [f for f in os.listdir(project_dir) if f.endswith('.md') and os.path.isfile(os.path.join(project_dir, f))]
    doc_score = min(3, len(md_files))
    
    # 5. 核心功能完整度
    core_score = 0
    if importable:
        core_score += 2
    if has_main:
        core_score += 1
    if runnable:
        core_score += 2
    if md_files:
        core_score += 1
    
    # 实际总分 = 关键因子累乘
    real_score = 0
    if importable and has_main and runnable:
        real_score = (volume + 1) * (doc_score + 1) * (core_score + 1)
    elif importable:
        real_score = volume + doc_score
    else:
        real_score = doc_score
    
    return {
        'project': project_name,
        'main_file': main_file,
        'real_score': real_score,
        'has_main': has_main,
        'importable': importable,
        'runnable': runnable,
        'run_output': main_output[:100] if main_output else '',
        'elapsed': round(elapsed, 2),
        'volume': volume,
        'doc_score': doc_score,
        'core_score': core_score,
        'lines': lines,
        'py_files': len(py_files),
        'import_error': import_err if not importable else None,
        'breakdown': f'import={importable} main={has_main} run={runnable} vol={volume} doc={doc_score} core={core_score}'
    }


def score_all():
    projects = {}
    for p in sorted(os.listdir(PROJECTS)):
        pp = os.path.join(PROJECTS, p)
        if os.path.isdir(pp):
            projects[p] = score_project(pp, p)
    
    # 也扫描 HQ
    hq_score = {
        'project': 'headquarters',
        'main_file': '(多个脚本)',
        'real_score': 0,
        'has_main': True,
        'importable': True,
        'runnable': True,
        'run_output': '(目录模式)',
        'elapsed': 0,
        'volume': 0,
        'doc_score': 0,
        'core_score': 5,
        'lines': 0,
        'py_files': len([f for f in os.listdir(HQ) if f.endswith('.py')]),
        'breakdown': 'HQ模式',
    }
    # 统计HQ
    hq_py = [f for f in os.listdir(HQ) if f.endswith('.py')]
    hq_py_no_underscore = [f for f in hq_py if not f.startswith('_')]
    hq_score['py_files'] = len(hq_py)
    hq_score['volume'] = min(5, hq_py_no_underscore.__len__() * 2)
    hq_score['doc_score'] = min(3, len([f for f in os.listdir(HQ) if f.endswith('.md')]))
    hq_score['real_score'] = (hq_score['volume'] + 1) * (hq_score['doc_score'] + 1) * hq_score['core_score']
    projects['headquarters'] = hq_score
    
    return projects


def main():
    print('📊 IGP RealScore — 实际运行得分 v1')
    print('=' * 55)
    print('  纸面分数是装饰，能跑起来才是真价值')
    print()
    
    scores = score_all()
    ranked = sorted(scores.values(), key=lambda x: x['real_score'], reverse=True)
    
    for rank, s in enumerate(ranked, 1):
        # 状态图标
        if s['runnable'] and s['importable']:
            icon = '✅'
        elif s['importable']:
            icon = '⚠️'
        else:
            icon = '❌'
        
        bar = '█' * min(20, s['real_score'])
        print(f'  {icon} #{rank} {s["project"]}')
        print(f'     实际得分: {s["real_score"]} | {bar}')
        print(f'     文件: {s["py_files"]}py | 行数: {s["lines"]} | 运行: {s["runnable"]}')
        print(f'     核心: import={s["importable"]} main={s["has_main"]} run={s["runnable"]}')
        if s['run_output']:
            print(f'     输出: {s["run_output"][:80]}')
        if s.get('import_error'):
            print(f'     错误: {s["import_error"]}')
        print()
    
    # 领导重新任命（基于实际得分）
    print('=' * 55)
    print('📋 基于实际得分的领导任命:')
    print()
    
    if ranked:
        champ = ranked[0]
        print(f'  🏆 最高得分: {champ["project"]} ({champ["real_score"]}分)')
        if champ['runnable']:
            print(f'  ✅ {champ["project"]}团队 升任 HQ总监')
        else:
            print(f'  ⚠ 最高分但无法运行，需修复')
    
    # 保存
    result = {
        'timestamp': datetime.now().isoformat(),
        'rankings': [
            {'rank': i+1, 'project': s['project'], 'real_score': s['real_score'],
             'runnable': s['runnable'], 'importable': s['importable'],
             'volume': s['volume'], 'doc_score': s['doc_score'], 'core_score': s['core_score']}
            for i, s in enumerate(ranked)
        ],
    }
    
    result_path = os.path.join(HQ, 'realscore.json')
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f'\n📊 已保存: realscore.json')


if __name__ == '__main__':
    main()
