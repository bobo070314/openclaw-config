"""
三天回溯进化引擎 (Three-Day Retro Evolution Engine)
每个问题产生3个团队方案 → 3天后对比 → 最佳方案反哺为知识
"""
import os
import json
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
TEAMS_DIR = BASE_DIR / "family-corp-teams"
MEMORY_DIR = BASE_DIR / "memory"

# 进化记忆库
EVOLUTION_LOG = TEAMS_DIR / "evolution_log.json"

def init_evolution():
    """初始化进化日志"""
    if EVOLUTION_LOG.exists():
        with open(EVOLUTION_LOG, encoding='utf-8') as f:
            return json.load(f)
    else:
        data = {
            "created": datetime.datetime.now().isoformat(),
            "rounds": [],
            "best_practices": [],
            "eliminated_approaches": [],
        }
        return data

def submit_solutions(problem_name, department, solutions):
    """
    提交3个团队的方案
    solutions = [
        {"team": "team1", "approach": "xxx", "cost_tokens": 0},
        {"team": "team2", "approach": "yyy", "cost_tokens": 0},
        {"team": "team3", "approach": "zzz", "cost_tokens": 0},
    ]
    """
    data = init_evolution()
    round_id = len(data["rounds"]) + 1
    
    round_entry = {
        "round_id": round_id,
        "problem": problem_name,
        "department": department,
        "submitted": datetime.datetime.now().isoformat(),
        "review_date": (datetime.datetime.now() + datetime.timedelta(days=3)).isoformat(),
        "solutions": solutions,
        "consensus": None,
        "winner": None,
        "promoted_to_skill": False,
    }
    data["rounds"].append(round_entry)
    
    with open(EVOLUTION_LOG, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"🔁 第{round_id}轮进化开始: [{department}] {problem_name}")
    print(f"   3个方案已提交，{datetime.datetime.now().strftime('%Y-%m-%d')} 后回溯")
    return round_id

def review_round(round_id, winner_team, comments, consume_remote_tokens=False):
    """
    3天后回溯：选出最佳方案
    """
    data = init_evolution()
    
    for round_entry in data["rounds"]:
        if round_entry["round_id"] != round_id:
            continue
        
        round_entry["winner"] = winner_team
        round_entry["consensus"] = comments
        round_entry["reviewed"] = datetime.datetime.now().isoformat()
        
        # 如果获胜方案是token消耗的，标记为"需要本地化"
        winner_solution = None
        for sol in round_entry["solutions"]:
            if sol["team"] == winner_team:
                winner_solution = sol
                break
        
        if winner_solution and winner_solution["cost_tokens"] > 0:
            # 把外调方案"本地化"
            best_practice = {
                "origin": f"round_{round_id}",
                "problem": round_entry["problem"],
                "approach": winner_solution["approach"],
                "department": round_entry["department"],
                "created": datetime.datetime.now().isoformat(),
                "localized_version": None,
            }
            data["best_practices"].append(best_practice)
            round_entry["promoted_to_skill"] = True
            print(f"🏆 第{round_id}轮: {winner_team} 获胜!")
            print(f"   → 方案已存入最佳实践库")
            if consume_remote_tokens:
                print(f"   ⚠️ 本方案消耗了远程token，已标记为'待本地化'")
        else:
            best_practice = {
                "origin": f"round_{round_id}",
                "problem": round_entry["problem"],
                "approach": winner_solution["approach"] if winner_solution else "",
                "department": round_entry["department"],
                "created": datetime.datetime.now().isoformat(),
                "localized": True,
            }
            data["best_practices"].append(best_practice)
            print(f"🏆 第{round_id}轮: {winner_team} 获胜 (零token成本!)")
        
        # 淘汰性能最差的方案
        min_score = float('inf')
        loser = None
        for sol in round_entry["solutions"]:
            score = sol.get("final_score", 0)
            if sol["team"] != winner_team and score < min_score:
                min_score = score
                loser = sol["team"]
        
        if loser:
            data["eliminated_approaches"].append({
                "team": loser,
                "problem": round_entry["problem"],
                "reason": f"得分最低({min_score})，被淘汰",
                "eliminated_at": datetime.datetime.now().isoformat(),
            })
            print(f"❌ {loser} 被淘汰!")
        
        break
    
    with open(EVOLUTION_LOG, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return data

def simulate_evolution_cycle():
    """
    模拟一个完整的三天回溯进化周期
    展示给老板看
    """
    print("="*60)
    print("三天回溯进化引擎 - 模拟推演")
    print("="*60)
    
    # 模拟一个真实问题
    round_id = submit_solutions(
        problem_name="修复caipiao1前端8088端口不显示",
        department="frontend",
        solutions=[
            {"team": "先锋战队", "approach": "用Playwright测试+Next.js重写路由", "cost_tokens": 0, "final_score": 8},
            {"team": "优雅战队", "approach": "Vue3重写前端+调试SSR配置", "cost_tokens": 0, "final_score": 6},
            {"team": "极速战队", "approach": "Hono+JSX重构，边缘部署", "cost_tokens": 0, "final_score": 7},
        ]
    )
    
    print()
    # 3天后回溯
    review_round(
        round_id=round_id,
        winner_team="先锋战队",
        comments="先锋战队的Playwright测试方案最快定位到问题(路由配置错误+Python路径问题)。优雅战队方案可行但开发周期长。极速战队方案适合新项目不适用现有项目。",
        consume_remote_tokens=False,
    )
    
    print()
    # 另一个问题——消耗token的
    round_id2 = submit_solutions(
        problem_name="需要AI生成产品描述文案2000条",
        department="content",
        solutions=[
            {"team": "内容战队", "approach": "人工编写，每条3分钟", "cost_tokens": 0, "final_score": 5},
            {"team": "分析战队", "approach": "爬取竞品文案+改写", "cost_tokens": 0, "final_score": 6},
            {"team": "AI驱动战队", "approach": "LangChain+GPT-4自动生成", "cost_tokens": 20000, "final_score": 9},
        ]
    )
    
    print()
    review_round(
        round_id=round_id2,
        winner_team="AI驱动战队",
        comments="AI战队20分钟完成2000条，质量达标。但消耗了20000 token。已将GPT输出缓存为本地模板，下次免token。",
        consume_remote_tokens=True,
    )
    
    print()
    print(f"进化日志: {EVOLUTION_LOG}")
    print(f"最佳实践库: {len(init_evolution()['best_practices'])} 条")
    print(f"已淘汰方案: {len(init_evolution()['eliminated_approaches'])} 个")

if __name__ == "__main__":
    simulate_evolution_cycle()
