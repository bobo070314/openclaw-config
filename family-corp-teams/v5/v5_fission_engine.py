#!/usr/bin/env python3
"""
IGP V5 染色体裂变引擎
六步循环：吸收→消化→研发→突变→裂变→升级
每条染色体独立运转，互不依赖
"""

import json, os, sys, subprocess, time, re, shutil
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V5_DIR = os.path.join(BASE, "v5")
ABSORB_DIR = os.path.join(BASE, "v5-absorb")
CHROMOSOMES_DIR = os.path.join(V5_DIR, "chromosomes")
os.makedirs(V5_DIR, exist_ok=True)
os.makedirs(CHROMOSOMES_DIR, exist_ok=True)

# ====================================================================
# 染色体定义
# ====================================================================

CHROMOSOMES = {
    "mcp": {
        "id": "chromosome1",
        "name": "MCP生态部",
        "desc": "MCP协议兼容，接入14,000+生态Server",
        "score": 1,
        "target": 9,
        "status": "absorbing",
        "models": ["igp_mcp_client.py", "igp_mcp_server.py"],
    },
    "a2a": {
        "id": "chromosome2",
        "name": "A2A联邦部",
        "desc": "Agent间标准通信，联邦化协作",
        "score": 0,
        "target": 7,
        "status": "absorbing",
        "models": ["igp_a2a_bridge.py"],
    },
    "skills": {
        "id": "chromosome3",
        "name": "Skills市场部",
        "desc": "Skills包市场，外部开发者可提交",
        "score": 3,
        "target": 9,
        "status": "absorbing",
        "models": ["igp_skills_loader.py"],
    },
    "provider": {
        "id": "chromosome4",
        "name": "Provider路由部",
        "desc": "多模型按需路由，Provider PK淘汰",
        "score": 4,
        "target": 9,
        "status": "absorbing",
        "models": ["igp_provider_router.py"],
    },
    "guardian": {
        "id": "chromosome5",
        "name": "安全Guardian部",
        "desc": "Plan/Act安全审批，自动回滚",
        "score": 2,
        "target": 8,
        "status": "absorbing",
        "models": ["igp_plan_act.py"],
    },
    "commerce": {
        "id": "chromosome6",
        "name": "商业协议部",
        "desc": "Agent商业协议，赚钱能力",
        "score": 0,
        "target": 6,
        "status": "absorbing",
        "models": ["igp_agent_commerce.py"],
    },
}

CHROMOSOME_CYCLE_FILE = os.path.join(V5_DIR, "chromosome_cycles.json")
ABSORPTION_LOG = os.path.join(V5_DIR, "absorption_log.json")


def load_cycles() -> Dict[str, Any]:
    if os.path.exists(CHROMOSOME_CYCLE_FILE):
        with open(CHROMOSOME_CYCLE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cycles(data: Dict[str, Any]):
    os.makedirs(os.path.dirname(CHROMOSOME_CYCLE_FILE), exist_ok=True)
    with open(CHROMOSOME_CYCLE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_chromosome_dir(chromo_id: str) -> str:
    """每条染色体有自己的独立工作目录"""
    d = os.path.join(CHROMOSOMES_DIR, chromo_id)
    os.makedirs(d, exist_ok=True)
    return d


# ====================================================================
# 六步循环执行器
# ====================================================================

class ChromosomeCycle:
    """
    每条染色体的独立生命周期
    吸收→消化→研发→突变→裂变→升级
    """

    def __init__(self, chromo_id: str):
        self.chromo_id = chromo_id
        self.info = CHROMOSOMES[chromo_id]
        self.dir = get_chromosome_dir(chromo_id)
        self.cycles = load_cycles()
        if chromo_id not in self.cycles:
            self.cycles[chromo_id] = {
                "cycle_count": 0,
                "steps": {},
                "score_history": [],
                "status": "idle",
                "created_at": now_iso(),
            }
        self.state = self.cycles[chromo_id]

    def step_absorb(self, absorb_report_path: str) -> bool:
        """Step 1: 吸收 - 读取吸收报告，提取关键点"""
        if not os.path.exists(absorb_report_path):
            print(f"  ⚠️  {self.info['name']}: 未找到吸收报告 {absorb_report_path}")
            return False
        with open(absorb_report_path, "r", encoding="utf-8") as f:
            report = f.read()
        self.state["steps"]["absorb"] = {
            "status": "done",
            "report_path": absorb_report_path,
            "report_length": len(report),
            "at": now_iso(),
        }
        self.state["status"] = "absorbed"
        save_cycles(self.cycles)
        print(f"  ✅ {self.info['name']}: 吸收完成 ({len(report)} chars)")
        return True

    def step_digest(self) -> bool:
        """Step 2: 消化 - 提取吸收物中的核心设计理念"""
        absorb = self.state["steps"].get("absorb", {})
        if absorb.get("status") != "done":
            print(f"  ⚠️  {self.info['name']}: 要先吸收才能消化")
            return False
        report_path = absorb.get("report_path", "")
        if not os.path.exists(report_path):
            return False
        with open(report_path, "r", encoding="utf-8") as f:
            report = f.read()
        digest = {
            "external_sources": extract_sources(report),
            "key_insights": extract_insights(report),
            "gap_analysis": extract_gaps(report),
            "digest_at": now_iso(),
        }
        digest_path = os.path.join(self.dir, "digest.json")
        with open(digest_path, "w", encoding="utf-8") as f:
            json.dump(digest, f, indent=2, ensure_ascii=False)
        self.state["steps"]["digest"] = {"status": "done", "path": digest_path, "at": now_iso()}
        self.state["status"] = "digested"
        save_cycles(self.cycles)
        print(f"  ✅ {self.info['name']}: 消化完成 ({len(digest['key_insights'])} insights)")
        return True

    def step_develop(self) -> bool:
        """Step 3: 研发 - 检查已有代码模型，标记缺失"""
        absorb = self.state["steps"].get("absorb", {})
        if not absorb:
            print(f"  ⚠️  {self.info['name']}: 需要先完成吸收")
            return False
        v4_dir = os.path.join(BASE, "upgrade-v4")
        models_found = []
        models_missing = []
        for model in self.info.get("models", []):
            model_path = os.path.join(v4_dir, model)
            if os.path.exists(model_path):
                models_found.append(model)
            else:
                models_missing.append(model)
        dev = {
            "models_found": models_found,
            "models_missing": models_missing,
            "need_new_development": bool(models_missing),
            "code_quality_score": len(models_found) / max(len(self.info.get("models", [])), 1) * 10,
        }
        dev_path = os.path.join(self.dir, "development.json")
        with open(dev_path, "w", encoding="utf-8") as f:
            json.dump(dev, f, indent=2, ensure_ascii=False)
        self.state["steps"]["develop"] = {"status": "done", "path": dev_path, "at": now_iso()}
        self.state["status"] = "developed"
        save_cycles(self.cycles)
        print(f"  ✅ {self.info['name']}: 研发评估完成 ({len(models_found)} existing, {len(models_missing)} missing)")
        return True

    def step_mutate(self) -> bool:
        """Step 4: 突变 - 生成突变设计方案"""
        import random
        mutations = [
            "PK排名机制",
            "Token效率评分",
            "自动升降级",
            "外部可插拔",
            "跨染色体调用",
            "成本熔断",
        ]
        selected = random.sample(mutations, min(3, len(mutations)))
        mutation = {
            "mutations_applied": selected,
            "mutation_design": f"{self.info['name']}突变设计:\n" + "\n".join(f"- {m}" for m in selected),
            "mutation_at": now_iso(),
        }
        mut_path = os.path.join(self.dir, "mutation.json")
        with open(mut_path, "w", encoding="utf-8") as f:
            json.dump(mutation, f, indent=2, ensure_ascii=False)
        self.state["steps"]["mutation"] = {"status": "done", "path": mut_path, "at": now_iso()}
        self.state["status"] = "mutated"
        save_cycles(self.cycles)
        print(f"  ✅ {self.info['name']}: 突变完成 ({', '.join(selected)})")
        return True

    def step_fission(self) -> bool:
        """Step 5: 裂变 - 生成独立运行模块"""
        chromo_dir = get_chromosome_dir(self.chromo_id)
        infra_dir = os.path.join(chromo_dir, "infra")
        skills_dir = os.path.join(chromo_dir, "skills")
        reports_dir = os.path.join(chromo_dir, "reports")
        os.makedirs(infra_dir, exist_ok=True)
        os.makedirs(skills_dir, exist_ok=True)
        os.makedirs(reports_dir, exist_ok=True)
        fission = {
            "dirs_created": [infra_dir, skills_dir, reports_dir],
            "independent_absorb_source": f"v5-absorb/chromosome_*_{self.chromo_id}.md",
            "independent_kpi": True,
            "can_survive_alone": True,
            "genes": self.state["steps"].get("mutation", {}).get("mutations_applied", []),
            "fission_at": now_iso(),
        }
        fission_path = os.path.join(chromo_dir, "fission.json")
        with open(fission_path, "w", encoding="utf-8") as f:
            json.dump(fission, f, indent=2, ensure_ascii=False)
        self.state["steps"]["fission"] = {"status": "done", "path": fission_path, "at": now_iso()}
        self.state["status"] = "fissioned"
        save_cycles(self.cycles)
        print(f"  ✅ {self.info['name']}: 裂变完成 (3个独立子目录)")
        return True

    def step_upgrade(self) -> bool:
        """Step 6: 升级 - 更新评分，归档本轮循环"""
        digest = self.state["steps"].get("digest", {})
        dev = self.state["steps"].get("develop", {})
        mutation = self.state["steps"].get("mutation", {})
        fission = self.state["steps"].get("fission", {})

        # 计算本轮得分
        base_score = self.info["score"]
        digest_bonus = 0.5 if digest.get("status") == "done" else 0
        dev_bonus = 1.0 if dev.get("status") == "done" else 0
        mutation_bonus = 1.5 if mutation.get("status") == "done" else 0
        fission_bonus = 2.0 if fission.get("status") == "done" else 0
        new_score = min(base_score + digest_bonus + dev_bonus + mutation_bonus + fission_bonus, self.info["target"])

        upgrade = {
            "new_score": round(new_score, 1),
            "previous_score": base_score,
            "target_score": self.info["target"],
            "delta": round(new_score - base_score, 1),
            "score_breakdown": {
                "base": base_score,
                "digest_bonus": digest_bonus,
                "dev_bonus": dev_bonus,
                "mutation_bonus": mutation_bonus,
                "fission_bonus": fission_bonus,
            },
            "cycle_complete_at": now_iso(),
        }
        upgrade_path = os.path.join(self.dir, "upgrade.json")
        with open(upgrade_path, "w", encoding="utf-8") as f:
            json.dump(upgrade, f, indent=2, ensure_ascii=False)

        self.state["steps"]["upgrade"] = {"status": "done", "path": upgrade_path, "at": now_iso()}
        self.state["cycle_count"] += 1
        self.state["score_history"].append({
            "cycle": self.state["cycle_count"],
            "score": new_score,
            "at": now_iso(),
        })
        self.state["status"] = "cycle_complete"
        self.info["score"] = new_score  # 更新染色体评分
        save_cycles(self.cycles)
        print(f"  ✅ {self.info['name']}: 升级完成 {base_score}→{new_score} (目标{self.info['target']})")
        return True

    def run_full_cycle(self, absorb_report_path: str) -> Dict[str, Any]:
        """执行一轮完整的六步循环"""
        print(f"\n{'='*60}")
        print(f"🧬 {self.info['name']} 第{self.state['cycle_count']+1}轮循环")
        print(f"{'='*60}")

        steps = [
            ("吸收", self.step_absorb, absorb_report_path),
            ("消化", self.step_digest, None),
            ("研发", self.step_develop, None),
            ("突变", self.step_mutate, None),
            ("裂变", self.step_fission, None),
            ("升级", self.step_upgrade, None),
        ]

        results = {}
        for name, func, arg in steps:
            try:
                if arg:
                    ok = func(arg)
                else:
                    ok = func()
                results[name] = "✅" if ok else "❌"
                if not ok:
                    print(f"  ⛔ {name}失败，终止本轮")
                    break
            except Exception as e:
                results[name] = f"❌ {e}"
                print(f"  💥 {name}异常: {e}")
                break

        self.state["steps"]["last_run"] = {
            "results": results,
            "completed_at": now_iso(),
        }
        save_cycles(self.cycles)

        return {
            "chromosome": self.chromo_id,
            "name": self.info["name"],
            "cycle": self.state["cycle_count"],
            "score": self.info["score"],
            "target": self.info["target"],
            "results": results,
        }

    def status(self) -> Dict[str, Any]:
        return {
            "id": self.chromo_id,
            "name": self.info["name"],
            "score": self.info["score"],
            "target": self.info["target"],
            "status": self.state["status"],
            "cycle_count": self.state["cycle_count"],
            "score_history": self.state["score_history"],
        }


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def extract_sources(report: str) -> List[str]:
    """从吸收报告中提取外部来源"""
    sources = []
    for line in report.split("\n"):
        line = line.strip()
        if line.startswith("- ") and ("http" in line or "github" in line.lower() or "pip" in line or "SDK" in line):
            sources.append(line)
    return sources[:10]


def extract_insights(report: str) -> List[str]:
    """提取关键发现"""
    insights = []
    lines = report.split("\n")
    capture = False
    for line in lines:
        if "关键发现" in line:
            capture = True
            continue
        if capture and line.strip().startswith("-"):
            insights.append(line.strip())
        if capture and ("吸收策略" in line or "差距" in line):
            break
    return insights[:10]


def extract_gaps(report: str) -> List[str]:
    """提取差距分析"""
    gaps = []
    lines = report.split("\n")
    capture = False
    for line in lines:
        if "差距" in line:
            capture = True
            continue
        if capture and line.strip().startswith("-"):
            gaps.append(line.strip())
        if capture and line.strip() == "":
            break
    return gaps[:5]


# ====================================================================
# V5 引擎主入口
# ====================================================================

class V5Engine:
    """管理所有染色体的裂变"""

    def __init__(self):
        self.cycles = {cid: ChromosomeCycle(cid) for cid in CHROMOSOMES}

    def run_all_cycles(self) -> Dict[str, Any]:
        """执行所有染色体的完整循环"""
        results = {}
        for cid, cycle in self.cycles.items():
            report_path = os.path.join(ABSORB_DIR, f"chromosome{list(CHROMOSOMES.keys()).index(cid)+1}_{cid}.md")
            # 尝试带名字的路径
            name_map = {
                "mcp": "chromosome1_MCP",
                "a2a": "chromosome2_A2A",
                "skills": "chromosome3_Skills",
                "provider": "chromosome4_Provider",
                "guardian": "chromosome5_Guardian",
                "commerce": "chromosome6_Commerce",
            }
            alt_path = os.path.join(ABSORB_DIR, f"{name_map[cid]}.md")
            final_path = alt_path if os.path.exists(alt_path) else report_path

            if not os.path.exists(final_path):
                print(f"\n⏳ {cycle.info['name']}: 等待吸收报告... (找: {final_path})")
                results[cid] = {"status": "waiting_absorb"}
                continue

            result = cycle.run_full_cycle(final_path)
            results[cid] = result

        return results

    def report(self) -> str:
        """生成裂变报告"""
        lines = []
        lines.append("=" * 60)
        lines.append("🧬 IGP V5 染色体裂变状况报告")
        lines.append(f"时间: {now_iso()}")
        lines.append("=" * 60)
        lines.append("")

        total_score = 0
        for cid, cycle in self.cycles.items():
            s = cycle.status()
            total_score += s["score"]
            bar = "🟢" * int(s["score"]) + "🔴" * (10 - int(s["score"]))
            lines.append(f"{s['name']:16s}  {s['score']:.1f}/10  {bar}  ({s['cycle_count']}轮循环)")
            lines.append(f"  {'状态':>8s}: {s['status']}")
            if s["score_history"]:
                hist = " → ".join([f"Cycle{h['cycle']}:{h['score']}" for h in s["score_history"]])
                lines.append(f"  {'进化':>8s}: {hist}")
            lines.append("")

        avg = total_score / max(len(self.cycles), 1)
        lines.append("-" * 60)
        lines.append(f"综合评分: {avg:.1f}/10")

        # 独立染色体判定
        independent_count = sum(1 for c in self.cycles.values() if c.state["cycle_count"] > 0)
        lines.append(f"已独立裂变: {independent_count}/{len(self.cycles)} 条染色体")
        lines.append(f"目标: 6/6 全独立")
        lines.append("=" * 60)

        return "\n".join(lines)


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"

    engine = V5Engine()

    if cmd == "run":
        results = engine.run_all_cycles()
        print("\n\n" + engine.report())

    elif cmd == "status":
        print(engine.report())

    elif cmd == "cycle":
        cid = sys.argv[2] if len(sys.argv) > 2 else ""
        if cid in engine.cycles:
            report_path = os.path.join(ABSORB_DIR, f"chromosome{list(CHROMOSOMES.keys()).index(cid)+1}_{cid}.md")
            result = engine.cycles[cid].run_full_cycle(report_path)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"未知染色体: {cid}. 可用: {list(CHROMOSOMES.keys())}")

    elif cmd == "report":
        print(engine.report())

    elif cmd == "reset":
        for cid in engine.cycles:
            cdir = get_chromosome_dir(cid)
            if os.path.exists(cdir):
                shutil.rmtree(cdir)
        if os.path.exists(CHROMOSOME_CYCLE_FILE):
            os.remove(CHROMOSOME_CYCLE_FILE)
        print("✅ 所有染色体状态已重置")
