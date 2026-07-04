#!/usr/bin/env python3
"""IGP V5 GitHub Trending Scanner — 扫描可吸收新项目"""
import os, sys, json, re, urllib.request, urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
ABSORB_DIR = os.path.join(os.path.dirname(BASE), 'v5-absorb')

RECOMMEND_RULES = [
    (r'(mcp|model.context|protocol|server|client)', 'MCP生态部', 'chromosome1'),
    (r'(payment|commerce|shop|stripe|patreon|marketplace)', '商业协议部', 'chromosome6'),
    (r'(llm|ai|gpt|model|train|generat|language)', 'Provider路由部', 'chromosome4'),
    (r'(security|auth|encrypt|audit|compliance)', '安全Guardian部', 'chromosome5'),
    (r'(agent|skill|tool|plugin|workflow)', 'Skills市场部', 'chromosome3'),
    (r'(a2a|agent-to-agent|federat)', 'A2A联邦部', 'chromosome2'),
]

# 已吸收项目（从吸收报告目录读取）
ABSORBED = set()
if os.path.isdir(ABSORB_DIR):
    absorbed_files = os.listdir(ABSORB_DIR)
    ABSORBED = set(
        re.sub(r'^chromosome\\\d+_|\.md$', '', f).lower().strip()
        for f in absorbed_files
    )

def recommend_chromosome(name, description):
    """自动推荐目标染色体"""
    text = f'{name} {description}'.lower()
    best = ('Skills市场部', 'chromosome3')  # default
    best_score = 0
    for pattern, chromo_name, chromo_id in RECOMMEND_RULES:
        score = len(re.findall(pattern, text))
        if score > best_score:
            best = (chromo_name, chromo_id)
            best_score = score
    return best

# Use mock data (GitHub Trending requires JS rendering)
USE_MOCK = True  # 设为False可尝试真实请求

def fetch_trending():
    """获取GitHub Trending项目"""
    try:
        req = urllib.request.Request('https://github.com/trending', 
                                     headers={'User-Agent': 'IGP-V5'})
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode('utf-8', errors='replace')
    except Exception:
        print('  📡 网络请求失败，使用本地mock数据')
        return mock_trending()
    
    # 解析HTML
    repos = []
    articles = re.findall(r'<article class="Box-row"(.*?)</article>', html, re.DOTALL)
    for art in articles[:15]:
        h2 = re.search(r'<h2[^>]*>.*?href="/([^"]+)"[^>]*>([^<]+)</a>', art, re.DOTALL)
        if not h2:
            continue
        repo_full = h2.group(1).strip()
        desc = re.search(r'<p class="col-9[^"]*"[^>]*>([^<]+)</p>', art, re.DOTALL)
        desc_text = desc.group(1).strip() if desc else ''
        stars = re.search(r'<span class="d-inline-block float-sm-right">(\\\d[\\\d,]*)\\s*stars', art)
        star_text = stars.group(1).replace(',', '') if stars else '0'
        lang = re.search(r'<span itemprop="programmingLanguage">([^<]+)</span>', art)
        lang_text = lang.group(1).strip() if lang else ''
        
        repos.append({
            'name': repo_full,
            'description': desc_text.strip(),
            'stars': int(star_text),
            'language': lang_text,
        })
    return repos[:10]

def mock_trending():
    """本地mock数据"""
    return [
        {'name': 'mcp/servers', 'description': 'Official MCP servers for various tools', 'stars': 42300, 'language': 'Python'},
        {'name': 'google/A2A', 'description': 'Agent-to-Agent protocol standard', 'stars': 8900, 'language': 'TypeScript'},
        {'name': 'stripe/stripe-python', 'description': 'Stripe SDK for Python', 'stars': 15100, 'language': 'Python'},
        {'name': 'langchain-ai/langchain', 'description': 'Building LLM applications', 'stars': 105000, 'language': 'Python'},
        {'name': 'anthropic/claude-code', 'description': 'Claude coding agent', 'stars': 29200, 'language': 'Python'},
        {'name': 'a2a/federation', 'description': 'A2A federation protocol', 'stars': 2400, 'language': 'Rust'},
        {'name': 'openclaw/openclaw', 'description': 'AI assistant gateway', 'stars': 5400, 'language': 'TypeScript'},
        {'name': 'deepseek/deepseek-v4', 'description': 'Next-gen LLM', 'stars': 18300, 'language': 'Python'},
        {'name': 'crewAI/crewAI', 'description': 'Multi-agent orchestration framework', 'stars': 32000, 'language': 'Python'},
        {'name': 'anthropic/safety', 'description': 'AI safety evaluation toolkit', 'stars': 1200, 'language': 'Python'},
    ]

def main():
    print('='*60)
    print('  🔭 IGP V5 GitHub Trending Scanner')
    print('  Scanning...')
    print('='*60)

    repos = fetch_trending()
    if not repos:
        print('  ⚠️ 使用本地mock数据')
        repos = mock_trending()

    print(f'\n  Top {len(repos)} 可吸收项目:\n')
    for i, repo in enumerate(repos, 1):
        name = repo['name']
        desc = repo['description'][:80] if repo['description'] else '(无描述)'
        stars = repo['stars']
        lang = repo['language']
        
        bare_name = name.split('/')[-1].lower() if '/' in name else name.lower()
        if bare_name in ABSORBED:
            status = '📌 已吸收'
        else:
            status = '🆕 可吸收'
        
        chromo_name, chromo_id = recommend_chromosome(name, desc)
        print(f'  {status} {i:2d}. {name:30s} ⭐{stars/1000:.1f}k')
        print(f'       {desc[:70]}')
        print(f'       → 推荐: {chromo_name} ({lang})')
        print()

    # 统计
    new_count = sum(1 for r in repos if r['name'].split('/')[-1].lower() not in ABSORBED)
    print(f'  📊 共{len(repos)}项目, 其中{new_count}个可吸收')
    print(f'='*60)

if __name__ == '__main__':
    main()
