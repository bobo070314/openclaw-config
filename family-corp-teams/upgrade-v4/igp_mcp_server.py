
#!/usr/bin/env python3
"""MCP Server for IGP — tools, resources, prompts"""
from mcp.server import MCPServer
import json, os, subprocess

mcp = MCPServer("igp-server")

@mcp.tool()
def igp_pk(dept_a: str, dept_b: str, task: str) -> str:
    """Run IGP PK round between two departments"""
    return json.dumps({
        "dept_a": dept_a,
        "dept_b": dept_b, 
        "task": task,
        "result": "PK recorded",
        "winner": "pending_llm_call"
    })

@mcp.tool()
def igp_skills_list() -> str:
    """List all installed IGP skills"""
    skills_dir = r"D:\\\bobo\\\openclaw-foreign\\\workspace\\\family-corp-teams\\\upgrade-v4\\\skills"
    results = []
    for item in os.listdir(skills_dir):
        skill_md = os.path.join(skills_dir, item, "SKILL.md")
        if os.path.exists(skill_md):
            with open(skill_md, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
            results.append({"name": item, "file": first_line})
    return json.dumps({"skills": results, "count": len(results)})

@mcp.tool()
def igp_leaderboard() -> str:
    """Get IGP provider leaderboard"""
    return json.dumps({
        "leaderboard": [
            {"provider": "qwen-turbo", "win_rate": 83.9, "wins": 26},
            {"provider": "qwen-plus", "win_rate": 27.3, "wins": 3}
        ]
    })

@mcp.resource("igp://departments")
def departments() -> str:
    """List all IGP departments"""
    depts = ["frontend", "backend", "infrastructure", "ai", "quality",
             "mobile", "design", "content", "data", "growth", 
             "compliance", "pmo", "tech-support", "advertising-anime",
             "ecommerce-marketing"]
    return json.dumps({"departments": depts, "count": len(depts)})

if __name__ == "__main__":
    from mcp.server.stdio import stdio_server
    import asyncio
    asyncio.run(stdio_server(mcp))
