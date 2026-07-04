"""
IGP DocMind v3 — Pipeline集成版
把DocMind挂在IGP Pipeline上，变成自动文档处理

全链路：
  Oracle日报 → DocMind分析 → JSONL入库 → Ghost监控
"""
import os, sys, json
from datetime import datetime

# 路径硬编码（0依赖原则）
FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
DOCMIND_DIR = os.path.join(FAMILY, 'projects', 'igp-docmind')
ORACLE_DIR = os.path.join(FAMILY, 'headquarters')
MEMORY_DIR = r'D:\bobo\openclaw-foreign\workspace\memory'

# 引入v2引擎
sys.path.insert(0, DOCMIND_DIR)

# 手动加载（避免导入问题）
def load_docmind_v2():
    """动态加载docmind_v2.py"""
    v2_path = os.path.join(DOCMIND_DIR, 'docmind_v2.py')
    with open(v2_path, 'r', encoding='utf-8') as f:
        code = f.read()
    exec_globals = {'__name__': 'docmind_v2_loaded'}
    exec(code, exec_globals)
    return exec_globals['DocMindV2']()


class PipelineIntegrator:
    """
    DocMind → Pipeline 集成器
    
    Pipeline现有: Monitor → Communicate → Heal → Report
    新增: Analyze (DocMind插入在Monitor之后)
    
    新流水线:
      1. Ghost Monitor (检测状态)
      2. DocMind Analyze (分析日志/报告)
      3. D2A Communicate (通信)
      4. Autofix Heal (自愈)
      5. Oracle Report (报告)
    """
    
    def __init__(self):
        self.docmind = load_docmind_v2()
        self.analyzed_count = 0
    
    def scan_oracle_reports(self):
        """扫描Oracle日报"""
        found = []
        for f in os.listdir(ORACLE_DIR):
            if 'oracle' in f.lower() and f.endswith('.json'):
                found.append(os.path.join(ORACLE_DIR, f))
        return found
    
    def scan_memory_files(self):
        """扫描memory文件"""
        found = []
        if os.path.exists(MEMORY_DIR):
            for f in os.listdir(MEMORY_DIR):
                if f.endswith('.md'):
                    found.append(os.path.join(MEMORY_DIR, f))
        return found
    
    def analyze_file(self, filepath):
        """分析一个文件内容"""
        name = os.path.basename(filepath)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'file': name, 'ok': False, 'error': str(e)[:80]}
        
        if len(content) < 20:
            return {'file': name, 'ok': True, 'note': '文件过小，跳过分析'}
        
        # 用DocMind分析
        analysis = self.docmind.analyze(content[:10000])  # 限制10K避免爆炸
        
        self.analyzed_count += 1
        
        return {
            'file': name,
            'ok': True,
            'chars': len(content),
            'headers': analysis['structure']['headers'],
            'paragraphs': analysis['stats']['paragraphs'],
            'compressed': analysis['stats']['compressed_ratio'],
            'preview': analysis['content']['compressed'][:100],
        }
    
    def run(self):
        """全自动运行"""
        print('🤖 IGP DocMind Pipeline — 自动文档分析')
        print('=' * 50)
        print()
        
        results = {'analyzed': [], 'errors': []}
        
        # 1. 扫描Oracle报告
        print('📡 扫描Oracle报告...')
        oracle_files = self.scan_oracle_reports()
        if oracle_files:
            for f in oracle_files:
                r = self.analyze_file(f)
                if r['ok']:
                    results['analyzed'].append(r)
                    print(f'  ✅ {r["file"]} ({r["chars"]}字, {r["headers"]}标题)')
                else:
                    results['errors'].append(r)
                    print(f'  ❌ {r["file"]}: {r["error"]}')
        else:
            print('  ⏭ 无Oracle报告')
        print()
        
        # 2. 扫描memory文件
        print('📡 扫描Memory文件...')
        memory_files = self.scan_memory_files()
        if memory_files:
            for f in memory_files:
                r = self.analyze_file(f)
                if r['ok']:
                    results['analyzed'].append(r)
                    print(f'  ✅ {r["file"]} ({r["chars"]}字, {r["headers"]}标题)')
                else:
                    results['errors'].append(r)
                    print(f'  ❌ {r["file"]}: {r["error"]}')
        else:
            print('  ⏭ 无Memory文件')
        print()
        
        # 3. 扫描项目文档
        print('📡 扫描Projects文档...')
        projects_dir = os.path.join(FAMILY, 'projects')
        if os.path.exists(projects_dir):
            for proj in sorted(os.listdir(projects_dir)):
                proj_dir = os.path.join(projects_dir, proj)
                if not os.path.isdir(proj_dir):
                    continue
                # 找README / 文档
                for doc_file in ['README.md', 'BEST_PRACTICE.md', 'readme.md']:
                    doc_path = os.path.join(proj_dir, doc_file)
                    if os.path.exists(doc_path):
                        r = self.analyze_file(doc_path)
                        if r['ok']:
                            results['analyzed'].append(r)
                            print(f'  ✅ {proj}/{doc_file} ({r["chars"]}字)')
                        break
        print()
        
        # 统计
        total = self.analyzed_count
        print(f'📊 分析统计:')
        print(f'  总计: {total} 个文档')
        print(f'  成功: {len(results["analyzed"])}')
        print(f'  失败: {len(results["errors"])}')
        
        # 生产JSONL入库
        jsonl_path = os.path.join(DOCMIND_DIR, 'pipeline_knowledge.jsonl')
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for r in results['analyzed']:
                if r.get('preview'):
                    line = json.dumps({
                        'file': r['file'],
                        'preview': r['preview'],
                        'chars': r['chars'],
                        'headers': r.get('headers', 0),
                        'timestamp': datetime.now().isoformat(),
                        'source': 'igp-docmind-pipeline',
                    }, ensure_ascii=False)
                    f.write(line + '\n')
        print(f'\n💾 知识库已更新: pipeline_knowledge.jsonl ({len(results["analyzed"])}条)')
        
        return results


def main():
    pipe = PipelineIntegrator()
    pipe.run()


if __name__ == '__main__':
    main()
