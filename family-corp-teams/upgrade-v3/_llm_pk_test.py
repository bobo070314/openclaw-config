"""
IGP v3 真实LLM PK测试 — Quality部门3队用DeepSeek进行代码审查PK
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from igp_llm_agent import IGPAgent, PKManager

print("=" * 60)
print("🔮 IGP v3.0 LLM PK Test")
print("=" * 60)

# 检查API key
import os
ak = os.environ.get("OPENAI_API_KEY", "")
print(f"\n[检查] API Key: {ak[:8]}...{ak[-4:] if len(ak)>12 else ''}")

# 创建3个Quality agent
agents = []
for tn in [1, 2, 3]:
    a = IGPAgent("quality", tn)
    agents.append(a)
    print(f"\n✅ 创建 {a.name} (模型: {a.model}, key: {ak[:8]}...)")

# 执行任务 — 代码审查
task = """审查以下Python代码，找出潜在问题和改进建议：

```python
def process_data(data):
    results = []
    for i in range(len(data)):
        item = data[i]
        if item['type'] == 'user':
            name = item['name']
            if len(name) > 0:
                results.append({'user': name, 'active': item.get('active', False)})
            else:
                print('Empty name')
        elif item['type'] == 'admin':
            if 'admin_level' in item:
                if item['admin_level'] > 5:
                    results.append({'admin': item['name'], 'level': 'senior'})
                else:
                    results.append({'admin': item['name'], 'level': 'junior'})
    return results
```

请列出：
1. 代码风格问题
2. 潜在bug
3. 性能问题
4. 改进建议（含代码）"""

print(f"\n{'#'*60}")
print(f"⚔️ Quality 部门 3队 代码审查PK")
print(f"  任务: 审查Python代码")
print(f"{'#'*60}")

for a in agents:
    print(f"\n[{a.name}] 调用LLM...")
    r = a.execute_task(task)
    print(f"  响应: {len(r['result'])} chars | {r['tokens']} tokens | {r['time_seconds']}s")
    print(f"  内容预览:")
    for line in r['result'][:400].split("\n")[:8]:
        print(f"    | {line}")

print(f"\n{'#'*60}")
print(f"🏆 PK总结:")
for a in agents:
    t = sum(h['tokens'] for h in a.history)
    print(f"  {a.name}: {len(a.history)}次调用, {t} tokens")
print(f"{'#'*60}")
