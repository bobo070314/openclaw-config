#!/usr/bin/env python3
"""IGP V5 Skills Registry — 38模块注册表 + Skills目录"""
import os, sys, json, re

BASE = os.path.dirname(os.path.abspath(__file__))
CHROMO_DIR = os.path.join(BASE, 'chromosomes')
REGISTRY_FILE = os.path.join(BASE, 'v5_skills_registry.json')
CATALOG_FILE = os.path.join(BASE, 'skills_catalog.md')

CHROMOSOMES = {
    '1': 'MCP生态部',
    '2': 'A2A联邦部',
    '3': 'Skills市场部',
    '4': 'Provider路由部',
    '5': '安全Guardian部',
    '6': '商业协议部',
    '7': 'Agent OS层',
    '8': 'AP2支付协议',
}

def extract_docstring(fp):
    """从文件提取docstring前3行"""
    try:
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            first = f.read(500)
        m = re.search(r'"""(.+?)"""', first, re.DOTALL)
        if m:
            lines = m.group(1).strip().split('\n')
            return lines[0][:100]
        m = re.search(r"'''(.+?)'''", first, re.DOTALL)
        if m:
            lines = m.group(1).strip().split('\n')
            return lines[0][:100]
    except:
        pass
    return '(无文档)'

def main():
    print('='*55)
    print('  📦 IGP V5 Skills Registry')
    print('='*55)
    
    registry = []
    total_modules = 0
    
    for cid, cname in sorted(CHROMOSOMES.items()):
        infra = os.path.join(CHROMO_DIR, f'chromosome{cid}', 'infra')
        if not os.path.isdir(infra):
            continue
        
        py_files = sorted([f for f in os.listdir(infra) if f.endswith('.py') and f != '__init__.py'])
        if not py_files:
            continue
        
        entry_point = 'run_v2.py' if cid == '6' else 'run.py'
        entry_path = os.path.join(infra, entry_point)
        if not os.path.exists(entry_path):
            entry_point = py_files[0]
        
        modules = []
        for pf in py_files:
            fp = os.path.join(infra, pf)
            doc = extract_docstring(fp)
            size = os.path.getsize(fp)
            modules.append({
                'filename': pf,
                'docstring': doc,
                'size_bytes': size,
            })
        
        chromo_entry = {
            'name': cname,
            'type': 'chromosome',
            'chromosome_id': int(cid),
            'modules': [m['filename'] for m in modules],
            'module_details': modules,
            'entry_point': entry_point,
            'entry_command': f'python chromosomes/chromosome{cid}/infra/{entry_point}',
            'total_modules': len(modules),
        }
        
        registry.append(chromo_entry)
        total_modules += len(modules)
        
        print(f'  ✅ #{cid} {cname:16s} {len(modules):2d}模块 → {entry_point}')
    
    # 写JSON
    with open(REGISTRY_FILE, 'w', encoding='utf-8') as f:
        json.dump({'registry': registry, 'total_chromosomes': len(registry), 'total_modules': total_modules}, 
                  f, ensure_ascii=False, indent=2)
    
    # 写Markdown目录
    with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
        f.write('# 🧬 IGP V5 Skills Catalog\n\n')
        f.write(f'_8条染色体, {total_modules}个独立模块 | 纯标准库 | 0外部依赖_\n\n')
        for entry in registry:
            f.write(f'## #{entry["chromosome_id"]} {entry["name"]}\n\n')
            f.write(f'- **入口**: `{entry["entry_command"]}`\n')
            f.write(f'- **模块数量**: {entry["total_modules"]}\n\n')
            f.write('| 模块 | 功能 | 大小 |\n')
            f.write('|------|------|------|\n')
            for m in entry['module_details']:
                f.write(f'| {m["filename"]} | {m["docstring"]} | {m["size_bytes"]}B |\n')
            f.write('\n')
    
    print(f'\n  📊 总计: {len(registry)}条染色体, {total_modules}个模块')
    print(f'  📝 注册表: {REGISTRY_FILE}')
    print(f'  📝 目录:   {CATALOG_FILE}')
    print('='*55)

if __name__ == '__main__':
    main()
