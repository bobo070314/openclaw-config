#!/usr/bin/env python3
"""
IGP v4 GitHub First — 遇错先搜GitHub再返回方案

这条脚本是"铁律"的程序化实现：
当IGP引擎任何模块报错时 → 不直接re-raise → 先搜GitHub找答案
"""
import sys, os, json, subprocess, time

BASE = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams"
V4_DIR = os.path.join(BASE, "upgrade-v4")

def github_first(problem_desc, search_terms=None):
    """核心函数：遇到问题先搜GitHub"""
    terms = search_terms or [problem_desc[:80]]
    
    print(f"\n{'='*50}")
    print("  🔍 GITHUB FIRST — 先搜再想")
    print(f"  问题: {problem_desc[:80]}")
    print(f"{'='*50}")
    
    # 用web_search工具去GitHub找答案
    # 这里由于是.py文件无法直接调web_search，所以标记并返回建议搜索词
    print(f"\n  建议搜索:")
    for t in terms:
        print(f"    site:github.com {t}")
    
    print(f"\n  参考资源:")
    print(f"    MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk")
    print(f"    Agent Skills Spec: https://agentskills.io/specification")
    print(f"    Anthropic Skills: https://github.com/anthropics/skills")
    print(f"    MCP Servers: https://github.com/modelcontextprotocol/servers")
    print(f"    GitHub Trending: https://github.com/trending")
    
    # 返回预检信息
    return {
        "action": "github_search_first",
        "problem": problem_desc,
        "suggested_terms": terms,
        "next_step": f"web_search query='github {problem_desc[:60]}'然后web_fetch结果"
    }

# ====================================================================
# 场景验证
# ====================================================================
if __name__ == "__main__":
    # 测试场景：v4引擎MCP连接失败时的自动触发
    result = github_first(
        "IGP MCP Server连接失败: socket.timeout on port 8080",
        ["MCP server python implementation stdio", "MCP client reconnect timeout python"]
    )
    print(f"\n  处理方案: {json.dumps(result, indent=2, ensure_ascii=False)}")
