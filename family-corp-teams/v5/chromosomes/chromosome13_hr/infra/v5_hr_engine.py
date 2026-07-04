"""
IGP岗位说明书引擎 — 为每个类生成岗位说明书
吸收自: facebookresearch/DocAgent (ACL 2025)
适用: IGP V5 12染色体 × 所有类
"""
import os, sys, ast, json
from collections import defaultdict
from datetime import datetime, timezone

class JobDescription:
    """岗位说明书 — 单个类的职责/接口/依赖/调用链"""
    
    def __init__(self, class_name, file_path, chromosome):
        self.class_name = class_name
        self.file_path = file_path
        self.chromosome = chromosome
        self.docstring = ''
        self.bases = []
        self.methods = []
        self.properties = []
        self.dependencies = []
        self.call_chain = []
        self.metrics = {}
    
    def to_dict(self):
        return {
            'class_name': self.class_name,
            'file': os.path.basename(self.file_path),
            'chromosome': self.chromosome,
            'docstring': self.docstring[:200] if self.docstring else '(无描述)',
            'bases': self.bases,
            'method_count': len(self.methods),
            'methods': self.methods,
            'properties': self.properties,
            'dependencies': self.dependencies,
            'call_chain': self.call_chain,
            'metrics': self.metrics,
        }


class Reader:
    """DocAgent Reader — 解析代码AST，提取结构"""
    
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.jobs = []
    
    def scan(self):
        if not os.path.exists(self.base_dir):
            return []
        
        for chrom in sorted(os.listdir(self.base_dir)):
            chrom_dir = os.path.join(self.base_dir, chrom)
            if not os.path.isdir(chrom_dir) or not chrom.startswith('chromosome'):
                continue
            for scan_dir in [chrom_dir, os.path.join(chrom_dir, 'infra')]:
                if not os.path.isdir(scan_dir):
                    continue
                for f in sorted(os.listdir(scan_dir)):
                    if not f.endswith('.py') or f.startswith('__'):
                        continue
                    fp = os.path.join(scan_dir, f)
                    self._parse_file(fp, chrom)
        
        tu = os.path.join(os.path.dirname(self.base_dir), 'thin_upgrade.py')
        if os.path.exists(tu):
            self._parse_file(tu, 'thin_upgrade')
        
        return self.jobs
    
    def _parse_file(self, fp, chromosome):
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                src = f.read()
            tree = ast.parse(src)
        except SyntaxError:
            return
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}" if module else alias.name)
        
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            
            jd = JobDescription(node.name, fp, chromosome)
            jd.docstring = ast.get_docstring(node) or ''
            jd.bases = [self._base_name(b) for b in node.bases]
            jd.dependencies = imports
            
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == 'self':
                            jd.properties.append(target.attr)
                
                elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    method_doc = ast.get_docstring(item) or ''
                    args = [a.arg for a in item.args.args if a.arg != 'self']
                    jd.methods.append({
                        'name': item.name,
                        'args': ', '.join(args) if args else '',
                        'is_async': isinstance(item, ast.AsyncFunctionDef),
                        'doc': method_doc.split('\n')[0][:80] if method_doc else '',
                    })
            
            jd.metrics = {
                'levels': 'trophy' if len(jd.methods) >= 5 else 'check' if len(jd.methods) >= 3 else 'warn',
                'has_doc': bool(jd.docstring),
                'import_deps': len(jd.dependencies),
                'property_count': len(jd.properties),
                'method_count': len(jd.methods),
                'bases_count': len(jd.bases),
            }
            self.jobs.append(jd)
    
    def _base_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._base_name(node.value)}.{node.attr}"
        return ast.dump(node)


class ReportWriter:
    """DocAgent Writer — 输出岗位说明书"""
    
    EMOJI_MAP = {'trophy': 'trophy', 'check': 'check', 'warn': 'warning'}
    
    def __init__(self, jobs):
        self.jobs = jobs
    
    def write_md(self, out_path):
        lines = []
        chroms = defaultdict(list)
        for j in self.jobs:
            chroms[j.chromosome].append(j)
        
        emoji = lambda m: 'trophy' if m == 'trophy' else 'check' if m == 'check' else 'warning'
        
        lines.append(f"# IGP Job Descriptions")
        lines.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
        lines.append(f"Total positions: {len(self.jobs)} classes\n")
        
        total_stars = 0
        for chrom in sorted(chroms.keys()):
            jobs = chroms[chrom]
            counts = {'trophy': 0, 'check': 0, 'warn': 0}
            for j in jobs:
                m = j.metrics.get('levels', 'warn')
                counts[m] = counts.get(m, 0) + 1
            total_stars += counts['trophy']
            
            lines.append(f"## {chrom} ({len(jobs)} positions)")
            labels = f"trophy{counts['trophy']} | check{counts['check']} | warning{counts['warn']}"
            lines.append(f"  {labels}")
            
            for j in sorted(jobs, key=lambda x: x.class_name):
                m = j.metrics.get('levels', 'warn')
                e = emoji(m)
                lines.append(f"### {e} {j.class_name}")
                fn = os.path.basename(j.file_path)
                lines.append(f"- **File**: `{fn}`")
                d = j.docstring.split('\n')[0][:120] if j.docstring else 'No description'
                lines.append(f"- **Role**: {d}")
                lines.append(f"- **Capabilities**: {j.metrics['method_count']} methods | {len(j.properties)} props | {j.metrics['bases_count']} bases")
                if j.bases:
                    lines.append(f"- **Inherits**: {', '.join(j.bases)}")
                lines.append("- **Methods**:")
                for mth in j.methods[:8]:
                    extra = f" - {mth['doc']}" if mth['doc'] else ''
                    lines.append(f"  - `{mth['name']}({mth['args']})`{extra}")
                if len(j.methods) > 8:
                    lines.append(f"  - ... +{len(j.methods)-8} more")
        
        lines.append(f"\n---")
        lines.append(f"\nSummary: {len(self.jobs)} classes | trophy{total_stars} advanced")
        
        content = '\n'.join(lines)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return content


class Verifier:
    """DocAgent Verifier — 验证岗位说明书完整性"""
    
    def __init__(self, jobs):
        self.jobs = jobs
    
    def verify(self):
        results = {
            'total': len(self.jobs),
            'missing_doc': [],
            'thin_classes': [],
        }
        
        for j in self.jobs:
            if not j.docstring:
                results['missing_doc'].append(j.class_name)
            if len(j.methods) < 3:
                results['thin_classes'].append(j.class_name)
        
        results['health'] = {
            'missing_doc_pct': round(len(results['missing_doc']) / max(len(self.jobs),1) * 100, 1),
            'thin_pct': round(len(results['thin_classes']) / max(len(self.jobs),1) * 100, 1),
        }
        return results


def main():
    base = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'
    chroms_dir = os.path.join(base, 'chromosomes')
    out_dir = os.path.join(base, 'job_descriptions')
    os.makedirs(out_dir, exist_ok=True)
    
    reader = Reader(chroms_dir)
    jobs = reader.scan()
    
    writer = ReportWriter(jobs)
    writer.write_md(os.path.join(out_dir, 'all_job_descriptions.md'))
    
    verifier = Verifier(jobs)
    v = verifier.verify()
    
    print(f"=== Job Descriptions Generated ===")
    print(f"Scanned: {v['total']} classes")
    print(f"Missing description: {len(v['missing_doc'])}")
    print(f"Thin classes (<3 methods): {len(v['thin_classes'])}")
    print(f"Description coverage: {100-v['health']['missing_doc_pct']}%")
    print(f"Sufficiency rate: {100-v['health']['thin_pct']}%")
    print(f"Output: {out_dir}/")

if __name__ == '__main__':
    main()
