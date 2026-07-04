"""
自动淘汰旧工具 + 自动克隆GitHub新工具
每周运行一次，保持技能库新鲜
"""
import os
import json
import subprocess
import datetime
from pathlib import Path

BASE_DIR = Path(r"D:\bobo\openclaw-foreign\workspace")
TEAMS_DIR = BASE_DIR / "family-corp-teams"
SKILLS_LOCAL = BASE_DIR / "skills-local"

EVOLUTION_LOG = TEAMS_DIR / "evolution_log.json"
TOOL_BLACKLIST = TEAMS_DIR / "tool_blacklist.json"

# ============================================================
# 1. 分析最佳实践库 → 新工具推荐
# ============================================================
def analyze_best_practices():
    """从进化日志中提取最佳方案的工具栈"""
    if not EVOLUTION_LOG.exists():
        print("无进化日志")
        return
    
    with open(EVOLUTION_LOG, encoding='utf-8') as f:
        data = json.load(f)
    
    # 统计每个工具的胜率
    tool_stats = {}
    
    for bp in data.get("best_practices", []):
        approach = bp.get("approach", "")
        # 简单提取工具名
        for word in approach.split():
            word = word.strip(",.()[]{}「」")
            if word and len(word) > 2 and not word.startswith(("http", "的", "了", "是", "在", "有")):
                tool_stats[word] = tool_stats.get(word, 0) + 1
    
    # 推荐出现3次以上的工具
    recommended = {k: v for k, v in tool_stats.items() if v >= 2}
    if recommended:
        print(f"📊 最佳实践中高频出现的工具 ({len(recommended)}个):")
        for tool, count in sorted(recommended.items(), key=lambda x: -x[1])[:10]:
            print(f"   🔥 {tool}: {count}次")
    
    return recommended

# ============================================================
# 2. 淘汰过时工具
# ============================================================
def eliminate_old_tools():
    """清理淘汰的工具目录"""
    blacklist = {"tool_used_count": 0, "tools": []}
    if TOOL_BLACKLIST.exists():
        with open(TOOL_BLACKLIST) as f:
            blacklist = json.load(f)
    
    # 从进化日志读取被淘汰的
    if EVOLUTION_LOG.exists():
        with open(EVOLUTION_LOG, encoding='utf-8') as f:
            data = json.load(f)
        
        eliminated = data.get("eliminated_approaches", [])
        for e in eliminated:
            team = e.get("team", "")
            reason = e.get("reason", "")
            # 这里只是记录，不实际删除（实际使用时可启用）
            blacklist["tools"].append({
                "team": team,
                "reason": reason,
                "eliminated_at": e.get("eliminated_at", ""),
            })
        blacklist["tool_used_count"] = len(blacklist["tools"])
    
    with open(TOOL_BLACKLIST, "w") as f:
        json.dump(blacklist, f, indent=2, ensure_ascii=False)
    
    total = len(blacklist["tools"])
    print(f"🗑️  已记录 {total} 个淘汰工具/方案")
    if total > 0:
        latest = blacklist["tools"][-1]
        print(f"   最新淘汰: {latest.get('team')} - {latest.get('reason')}")
    
    return total

# ============================================================
# 3. GitHub 批量克隆更新
# ============================================================
def clone_missing_repos():
    """尝试克隆缺失的GitHub仓库（--depth=1）"""
    # 读取skills-local中待克隆的工具
    index_file = SKILLS_LOCAL / "index.json"
    if not index_file.exists():
        print("❌ index.json 不存在")
        return
    
    with open(index_file, encoding='utf-8') as f:
        index = json.load(f)
    
    skills = index.get("skills", [])
    # 去重
    unique_skills = {}
    for s in skills:
        name = s["name"]
        if name not in unique_skills:
            unique_skills[name] = s
    
    print(f"📦 skills-local 共 {len(unique_skills)} 个去重工具")
    
    # 检查哪些已克隆
    cloned = 0
    for emp_dir in SKILLS_LOCAL.iterdir():
        if not emp_dir.is_dir() or emp_dir.name == "READM.md":
            continue
        for sub in emp_dir.iterdir():
            if sub.is_dir() and (sub / ".git").exists():
                cloned += 1
    
    print(f"✅ 已实际克隆: {cloned} 个仓库")
    print(f"📋 待克隆: {len(unique_skills)} 个技能 (占位符)")
    print(f"💡 运行 full_clone.py 可批量克隆")

# ============================================================
# 4. 每周维护报告
# ============================================================
def weekly_maintenance_report():
    """生成每周维护报告"""
    print("=" * 60)
    print("📋 技能库每周维护报告")
    print("=" * 60)
    
    # 进化日志
    if EVOLUTION_LOG.exists():
        with open(EVOLUTION_LOG, encoding='utf-8') as f:
            data = json.load(f)
        print(f"\n🏆 进化轮次: {len(data['rounds'])}")
        print(f"📚 最佳实践库: {len(data['best_practices'])} 条")
        print(f"🗑️  已淘汰方案: {len(data['eliminated_approaches'])} 个")
    
    # 技能库统计
    emp_dirs = [d for d in SKILLS_LOCAL.iterdir() if d.is_dir() and d.name != "READM.md"]
    total_readme = 0
    for d in emp_dirs:
        if (d / "README.md").exists():
            total_readme += 1
    
    print(f"\n👥 员工技能目录: {len(emp_dirs)}")
    print(f"📖 有README: {total_readme}")
    
    # 建议
    print(f"\n💡 本周建议:")
    if data.get("best_practices"):
        latest_bp = data["best_practices"][-1]
        print(f"   - 最新最佳实践来自: {latest_bp.get('origin', 'unknown')}")
        if not latest_bp.get("token_free", False):
            print(f"   - ⚠️ 该方案消耗了token，建议本地化")
    
    print(f"\n✅ 维护完成")

if __name__ == "__main__":
    analyze_best_practices()
    print()
    eliminate_old_tools()
    print()
    clone_missing_repos()
    print()
    weekly_maintenance_report()
