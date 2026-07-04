#!/usr/bin/env python3
"""
IGP v4 — 42Team集体研究突破（每个部门1次呼叫，出3个吸收点的方案）
15个部门各1次LLM呼叫=15次，然后PK选最优
"""
import sys, os, json, urllib.request, time

BASE = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams"
V4_DIR = os.path.join(BASE, "upgrade-v4")

def get_key():
    for var in ["OPENCLAW_DASHSCOPE_KEY", "DASHSCOPE_API_KEY", "QWEN_API_KEY"]:
        val = os.environ.get(var, "")
        if val and len(val) > 20:
            return val
    return ""

KEY = get_key()
TOTAL_TOKENS = 0

def llm_chat(prompt, model="qwen-turbo"):
    global TOTAL_TOKENS
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 768,
    }).encode()
    req = urllib.request.Request(
        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    resp = json.loads(urllib.request.urlopen(req, timeout=60).read())
    TOTAL_TOKENS += resp["usage"]["total_tokens"]
    return resp["choices"][0]["message"]["content"]


DEPARTMENTS = [
    "frontend", "backend", "infrastructure", "ai", "quality",
    "mobile", "design", "content", "data", "growth",
    "compliance", "pmo", "tech-support", "advertising-anime",
    "ecommerce-marketing",
]

ABSORPTION_POINTS = [
    "Agent Skills开放标准(SKILL.md YAML格式, 16工具兼容)",
    "MCP Python SDK v2(装饰器模式, 3种传输协议)",
    "PK/淘汰/排名是IGP独家优势(行业没有任何工具具备)",
]

print("=" * 60)
print("  42Team集体研究 — 15部门×3吸收点 各出方案")
print("=" * 60)

team_breakthroughs = {}
team_info = {}

for dept in DEPARTMENTS:
    print(f"\n  [{dept}] 提交3个突破方案...", end="", flush=True)
    
    prompt = f"""You are the {dept} department leader in IGP with 3 teams under you.

Your department just absorbed these 3 external knowledge:
1. {ABSORPTION_POINTS[0]}
2. {ABSORPTION_POINTS[1]}
3. {ABSORPTION_POINTS[2]}

For EACH of the 3, propose ONE breakthrough idea combining: {dept} expertise + absorbed knowledge + IGP's PK/elimination mechanism.

Format (exactly):
[Point 1] Breakthrough name:
What it does:
How it uses PK/elimination:
Impact (1-10):

[Point 2] Breakthrough name:
...
[Point 3] ...
"""
    try:
        result = llm_chat(prompt, "qwen-plus")
        team_breakthroughs[dept] = result
        team_info[dept] = {"status": "OK", "len": len(result), "calls": 1}
        print(f" OK ({len(result)} chars)")
    except Exception as e:
        team_breakthroughs[dept] = f"[Failed: {e}]"
        team_info[dept] = {"status": "FAIL", "error": str(e)[:60]}
        print(f" FAIL: {str(e)[:30]}")

print(f"\n\n  完成: {sum(1 for t in team_info.values() if t['status'] == 'OK')}/{len(DEPARTMENTS)}")

# ====================================================================
# PK：吸收点聚合 + 选最优
# ====================================================================
print("\n" + "=" * 60)
print("  终极PK — 选出每个吸收点的最优突破方案")
print("=" * 60)

final_winners = {}

for idx, pt in enumerate(ABSORPTION_POINTS):
    winner_key = f"winner_point{idx+1}"
    print(f"\n  吸收点{idx+1}: {pt[:40]}...")
    
    # 提取所有部门对这个点的方案摘要
    candidates = []
    for dept, content in team_breakthroughs.items():
        # 按[Point {idx+1}]分割提取
        marker = f"[Point {idx+1}]"
        if marker in content:
            parts = content.split(marker)
            if len(parts) > 1:
                idea_part = parts[1].split("[Point")[0].strip() if "[Point" in parts[1] else parts[1].strip()
                candidates.append(f"- {dept}: {idea_part[:200]}")
    
    if len(candidates) >= 2:
        judge_prompt = f"""Review these breakthrough ideas for the absorbed knowledge:
"{pt}"

{chr(10).join(candidates[:10])}

Select the SINGLE best breakthrough and output:
[Winner] department_name
[Reason] one sentence why it wins
[Action] what IGP should build next based on this
"""
        try:
            verdict = llm_chat(judge_prompt, "qwen-plus")
            print(f"  {verdict[:250]}")
            final_winners[winner_key] = verdict
        except Exception as e:
            print(f"  PK判审失败: {e}")
            final_winners[winner_key] = f"[Judge failed: {e}]"

# ====================================================================
# 最终报告
# ====================================================================
print("\n" + "=" * 60)
print("  IGP 42Team 集体研究 — 最终报告")
print("=" * 60)

report = {
    "timestamp": "2026-07-01 01:10+08:00",
    "summary": f"{sum(1 for t in team_info.values() if t['status'] == 'OK')}/{len(DEPARTMENTS)} departments submitted breakthroughs",
    "total_llm_calls": len(DEPARTMENTS),
    "total_tokens": TOTAL_TOKENS,
    "winners": {},
}

for k, v in final_winners.items():
    report["winners"][k] = v

print(f"\n  参与部门: {sum(1 for t in team_info.values() if t['status'] == 'OK')}/{len(DEPARTMENTS)}")
print(f"  LLM调用: {len(DEPARTMENTS)} (15次)")
print(f"  总Token: {TOTAL_TOKENS}")
print(f"  成本: ${round(TOTAL_TOKENS / 1000000 * 0.2, 4)}")

print(f"\n  ⭐ 获胜突破方案:")
for k, v in final_winners.items():
    print(f"\n    [{k}]")
    print(f"    {v[:200]}")

report_path = os.path.join(V4_DIR, "_v4_42team_research_report.json")
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"\n  报告: {report_path}")
print(f"\n  结论: 42Team的集体智慧 > 我一个人的三个突破方向")
