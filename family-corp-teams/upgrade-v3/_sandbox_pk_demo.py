"""
IGP v3 Sandbox PK Demo — quality部门在Docker沙箱中真实PK
"""
import sys, pathlib, json

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from igp_agent_runner import TeamAgent, IGPAgentManager
from igp_mcp_bridge import IGP_MCP

print("=" * 60)
print("⚔️  IGP v3.0 Sandbox PK Demo")
print("=" * 60)

# 启动Docker沙箱
mcp = IGP_MCP()
print("\n[1/4] 启动Docker沙箱...")
result = mcp.sandbox_start("python:3.12-slim")
print(f"  {result}")

# 加载Quality部门3队
print("\n[2/4] 加载Quality部门3队...")
agents = []
for tn in [1, 2, 3]:
    a = TeamAgent("quality", tn)
    a.load_profile()
    agents.append(a)
    print(f"  ✅ {a.name}: {', '.join(a.tools) if a.tools else '通用'}")

# 派发任务
task = "优化GitHub仓库的README.md文件结构，增加API文档章节"
print(f"\n[3/4] 派发任务: {task}")

results = []
for a in agents:
    a.mcp = IGP_MCP()  # 每个agent自己的MCP
    r = a.execute(task)
    results.append(r)

# 评分PK
results.sort(key=lambda x: x["score"], reverse=True)
print(f"\n⚡ PK结果:")
for i, r in enumerate(results):
    medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"  {i+1}."
    print(f"  {medal} {r['team']}: {r['score']}/10")

# 清理沙箱
print("\n[4/4] 清理沙箱...")
mcp.sandbox_stop()

print(f"\n{'='*60}")
print(f"🏆 胜者: {results[0]['team']}")
print(f"💀 败者: {results[-1]['team']}")
print(f"{'='*60}")
