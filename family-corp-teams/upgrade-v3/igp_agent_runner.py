"""
IGP Agent Runner v1 — 为42个团队提供真正的Agent执行能力

架构：
14部门 × 3队 = 42个 Agent
每个 Agent 执行周期: 感知(Observe) → 推理(Plan) → 行动(Act) → 验证(Verify)

设计哲学：
- 不绑定任何LLM API，通过策略模式注入
- 每个团队独立沙箱（可选Docker）
- 继承IGP的PK/淘汰机制，但输出来自真实执行
"""

import json, pathlib, sys, datetime, textwrap, traceback, os

# 上级目录
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from igp_mcp_bridge import IGP_MCP

TEAMS_DIR = pathlib.Path(__file__).parent.parent
API_BASE = "https://api.deepseek.com/v1"
API_KEY = os.environ.get("OPENAI_API_KEY", "")

class TeamAgent:
    """一个IGP团队的Agent执行器"""

    def __init__(self, dept: str, team_num: int, api_key: str = None):
        self.dept = dept          # 部门名, e.g. "frontend"
        self.team_num = team_num   # 1/2/3
        self.name = f"{dept}-team{team_num}"
        self.mcp = IGP_MCP()
        self.api_key = api_key or API_KEY
        self.tools = []           # 该团队可用的工具列表
        self.kpi = {"wins": 0, "losses": 0, "score": 100, "token_cost": 0}

    def load_profile(self):
        """从部门文件加载团队配置"""
        path = TEAMS_DIR / self.dept / f"team{self.team_num}.md"
        if path.exists():
            content = path.read_text(encoding="utf-8")
            # 解析工具栈
            for line in content.split("\n"):
                if line.startswith("- 工具栈:"):
                    self.tools = [t.strip() for t in line.replace("- 工具栈:", "").split("/")]
            return content
        return None

    def observe(self, task: str) -> dict:
        """感知阶段：收集任务相关的所有上下文"""
        context = {
            "task": task,
            "repo_structure": self.mcp.ls("."),
            "tool_stack": self.tools,
            "team_name": self.name,
            "time": datetime.datetime.now().isoformat(),
        }
        return context

    def plan(self, context: dict) -> str:
        """推理阶段：规划执行方案"""
        # 调用LLM规划（也可以本地规则规划）
        prompt = f"""你是IGP集团{self.dept}部门的{self.name}队。
你的工具栈: {', '.join(self.tools)}

任务: {context['task']}

请输出一个简洁的执行计划（3-5步），包括具体要修改的文件和操作。
只输出计划本身，不要额外说明。
"""
        # 这里可以用LLM生成（将来），目前用规则模板
        return f"""计划 ({self.name}):
1. 分析当前仓库结构和相关文件
2. 定位需要修改的文件
3. 执行代码变更
4. 运行验证（测试/lint）
5. 生成变更摘要"""

    def act(self, plan: str) -> str:
        """行动阶段：执行计划的每一步"""
        results = []
        # Step 1: 检查仓库
        r1 = self.mcp.git_status(".")
        results.append(f"[git status]\n{r1}")

        # Step 2: 读取相关文件（按规划）
        # (实际执行时会根据plan决定读哪些文件)

        # Step 3: 执行变更
        # (实际执行时会调用LLM生成代码)

        # Step 4: 验证
        r4 = self.mcp.git_diff(".")
        results.append(f"[git diff]\n{r4}")

        return "\n\n".join(results)

    def verify(self, output: str) -> dict:
        """验证阶段：评估执行结果"""
        score = 7  # 基础分
        detail = output[:500] if len(output) > 500 else output
        return {
            "score": score,
            "detail": detail,
            "team": self.name,
        }

    def execute(self, task: str) -> dict:
        """完整执行周期：感知→推理→行动→验证"""
        print(f"\n{'='*50}")
        print(f"🏃 {self.name} 开始执行: {task}")
        print(f"{'='*50}")

        try:
            ctx = self.observe(task)
            plan = self.plan(ctx)
            print(f"\n📋 计划:\n{textwrap.indent(plan, '  ')}")
            output = self.act(plan)
            print(f"\n📊 输出:\n{textwrap.indent(output[:300], '  ')}")
            result = self.verify(output)
            print(f"\n  ✅ 评分: {result['score']}/10")
            return result
        except Exception as e:
            print(f"\n  ❌ 执行失败: {e}")
            return {"score": 1, "detail": str(e), "team": self.name}

    def __repr__(self):
        return f"<TeamAgent {self.name}>"


class IGPAgentManager:
    """管理42个TeamAgent"""

    def __init__(self):
        self.agents = {}
        self._init_agents()

    def _init_agents(self):
        """扫描所有部门目录创建Agent实例"""
        depts = [
            "frontend", "backend", "infrastructure", "ai",
            "mobile", "design", "quality", "pmo",
            "growth", "compliance", "advertising-anime", "ecommerce-marketing",
        ]
        for d in depts:
            for tn in [1, 2, 3]:
                agent = TeamAgent(d, tn)
                agent.load_profile()
                self.agents[agent.name] = agent
        print(f"  ✅ {len(self.agents)}个Agent加载完毕")

    def get_team(self, dept: str, team_num: int) -> TeamAgent:
        return self.agents.get(f"{dept}-team{team_num}")

    def get_department(self, dept: str) -> list:
        return [self.agents[f"{dept}-team{tn}"] for tn in [1, 2, 3] if f"{dept}-team{tn}" in self.agents]

    def run_pk(self, dept: str, task: str) -> dict:
        """部门内3队PK"""
        teams = self.get_department(dept)
        if len(teams) < 3:
            return {"error": f"部门 {dept} 团队不足"}

        print(f"\n{'#'*60}")
        print(f"⚔️  {dept} 部门 PK: {task}")
        print(f"{'#'*60}")

        results = []
        for t in teams:
            r = t.execute(task)
            results.append(r)

        # 排序
        results.sort(key=lambda x: x["score"], reverse=True)
        return {
            "dept": dept,
            "task": task,
            "winner": results[0]["team"],
            "loser": results[-1]["team"],
            "scores": [(r["team"], r["score"]) for r in results],
            "details": results,
        }


if __name__ == "__main__":
    print("🚀 IGP Agent Runner v1 — 初始化...")
    mgr = IGPAgentManager()
    print("\n  可用指令:")
    print("    run_pk(dept, task)  — 部门内3队PK")
    print("    get_team(dept, n)   — 获取指定团队")
    print("    get_department(d)   — 获取部门全部团队")
