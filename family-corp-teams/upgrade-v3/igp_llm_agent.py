"""
IGP LLM Agent — 通过OpenRouter/DeepSeek驱动真正的代码生成Agent

设计哲学：
- 不绑定任何特定供应商，通过OpenRouter统一路由
- 每个Agent有自己的system prompt（基于部门/团队配置）
- 支持流式和阻塞两种调用模式
- 调用历史记录，方便PK回溯
"""

import os, json, httpx, datetime, textwrap

# 可用API源
APIS = {
    "dashscope": {
        "base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "key_env": "OPENCLAW_DASHSCOPE_KEY",
        "default_model": "qwen-plus",
    },
    "openrouter": {
        "base": "https://openrouter.ai/api/v1",
        "key_env": "CHECKER_OPENROUTER_KEY",
        "default_model": "deepseek/deepseek-chat",
    },
}
DEFAULT_PROVIDER = "dashscope"  # Qwen 免费且已验证可用

class IGPAgent:
    """真正的AI Agent，可调用LLM完成任务"""

    def __init__(self, dept: str, team_num: int, api_key: str = None, model: str = None):
        self.dept = dept
        self.team_num = team_num
        self.name = f"{dept}-team{team_num}"
        # 优先用CHECKER_OPENROUTER_KEY（已验证有效），其次OPENAI_API_KEY
        self.api_key = api_key or ""
        self.provider = DEFAULT_PROVIDER
        self.model = model or APIS[self.provider]["default_model"]
        self.api_base = APIS[self.provider]["base"]
        self.history = []  # 调用记录
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """构建团队专属的system prompt"""
        return f"""你是IGP国际集团{self.dept}部门的{self.name}队。
你的定位：顶级{self.dept}工程师。

做事原则：
1. 先理解再动手——分析问题，明确目标
2. 生成精确的代码/方案——不啰嗦、不废话
3. 遵循行业最佳实践
4. 注意代码安全性和健壮性
5. 输出格式：先1行说明，然后是代码（markdown代码块）

你正在沙箱环境中工作，可以安全执行任何代码。"""

    def think(self, task: str, context: dict = None) -> str:
        """调用LLM进行思考/规划"""
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        if context:
            ctx_str = json.dumps(context, ensure_ascii=False, indent=2)
            messages.append({"role": "user", "content": f"当前上下文:\n{ctx_str}\n\n任务: {task}"})
        else:
            messages.append({"role": "user", "content": task})

        # 自动获取API key（如果未提供）
        if not self.api_key:
            env_key = APIS[self.provider]["key_env"]
            self.api_key = os.environ.get(env_key, "")

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 4096,
        }

        try:
            with httpx.Client(timeout=90) as client:
                resp = client.post(
                    f"{self.api_base}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )
            if resp.status_code == 200:
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                used_tokens = data.get("usage", {}).get("total_tokens", 0)
                self.history.append({
                    "time": datetime.datetime.now().isoformat(),
                    "task": task[:100],
                    "tokens": used_tokens,
                    "status": "ok",
                })
                return content
            else:
                self.history.append({
                    "time": datetime.datetime.now().isoformat(),
                    "task": task[:100],
                    "tokens": 0,
                    "status": f"err:{resp.status_code}",
                })
                return f"[API Error {resp.status_code}]: {resp.text[:200]}"
        except Exception as e:
            return f"[Error]: {e}"

    def execute_task(self, task: str) -> dict:
        """完整执行：思考+输出"""
        start = datetime.datetime.now()
        result = self.think(task)
        elapsed = (datetime.datetime.now() - start).total_seconds()
        return {
            "agent": self.name,
            "model": self.model,
            "result": result,
            "tokens": self.history[-1]["tokens"] if self.history else 0,
            "time_seconds": round(elapsed, 2),
        }

    def summary(self):
        calls = len(self.history)
        tokens = sum(h["tokens"] for h in self.history)
        return f"{self.name}: {calls}次调用, {tokens} tokens, 模型={self.model}"


class PKManager:
    """部门内PK 调度器"""

    def __init__(self):
        self.agents = {}
        self._init_all()

    def _init_all(self):
        depts = [
            "frontend", "backend", "infrastructure", "ai",
            "mobile", "design", "quality", "pmo",
            "growth", "compliance", "advertising-anime", "ecommerce-marketing",
        ]
        for d in depts:
            for tn in [1, 2, 3]:
                a = IGPAgent(d, tn)
                self.agents[a.name] = a
        print(f"  ✅ 已加载 {len(self.agents)} 个LLM Agent")

    def run_pk(self, dept: str, task: str, verbose: bool = True) -> dict:
        """部门内3队同时执行同一任务，比较结果"""
        team_names = [f"{dept}-team{tn}" for tn in [1, 2, 3]]
        agents = [self.agents.get(n) for n in team_names if n in self.agents]

        if len(agents) < 3:
            return {"error": f"部门 {dept} 可用Agent不足"}

        print(f"\n{'#'*60}")
        print(f"⚔️  {dept} PK: 3队同时执行")
        print(f"  任务: {task}")
        print(f"{'#'*60}")

        results = []
        for a in agents:
            r = a.execute_task(task)
            print(f"\n  [{a.name}] {len(r['result'])} chars | {r['tokens']} tokens | {r['time_seconds']}s")
            if verbose:
                preview = r["result"][:200].replace("\n", " ")[:150]
                print(f"    预览: {preview}...")
            results.append(r)

        # 按token效率评分（少token+好内容=高分）
        for r in results:
            content_len = len(r["result"])
            token_cost_penalty = r["tokens"] / 100  # 每100 token -1分
            content_bonus = min(content_len / 200, 5)  # 最多+5分
            r["score"] = round(10 - token_cost_penalty + content_bonus, 1)
            r["score"] = max(1, min(10, r["score"]))

        results.sort(key=lambda x: x["score"], reverse=True)
        return {
            "dept": dept,
            "task": task,
            "winner": results[0]["agent"],
            "loser": results[-1]["agent"],
            "scores": [(r["agent"], r["score"]) for r in results],
        }

    def summary(self):
        for name, agent in self.agents.items():
            print(f"  {agent.summary()}")


if __name__ == "__main__":
    print("🚀 IGP LLM Agent — 加载中...")
    mgr = PKManager()
    print("\n  ✅ 就绪")
    print("  run_pk(dept, task)  — 3队PK")
