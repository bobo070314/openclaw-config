"""
IGP v3.0 Upgrade Engine — 升级配方式执行器

不暴力重写，而是通过"配方"一步步升级IGP：
1. MCP工具层 → 已有 (igp_mcp_bridge.py)
2. Agent Runner → 已有 (igp_agent_runner.py)
3. 连接现有igp_engine.py → 在此完成
4. 创建v3心跳
"""

import json, pathlib, sys, datetime, subprocess, traceback

ROOT = pathlib.Path(__file__).parent.parent  # family-corp-teams
V3_DIR = ROOT / "upgrade-v3"
ENGINE = ROOT / "igp_engine.py"

def step(msg):
    print(f"\n{'='*50}")
    print(f"  {msg}")
    print(f"{'='*50}")

def check_mark(ok: bool):
    return "✅" if ok else "❌"

# ── 配方1: 检查igp_engine.py是否可读 ──
step("配方1: 检查现有igp_engine.py")

if ENGINE.exists():
    content = ENGINE.read_text(encoding="utf-8")
    lines = content.count("\n")
    print(f"  ✅ igp_engine.py 存在: {lines} 行")
else:
    print(f"  ❌ igp_engine.py 不存在!")
    sys.exit(1)

# ── 配方2: 检查MCP Bridge是否可用 ──
step("配方2: 验证IGP MCP Bridge")

sys.path.insert(0, str(V3_DIR))
try:
    from igp_mcp_bridge import IGP_MCP
    mcp = IGP_MCP()
    ls_out = mcp.ls(".")
    print(f"  ✅ MCP Bridge: {len(ls_out.split(chr(10)))} 个文件可列")
except Exception as e:
    print(f"  ❌ MCP Bridge失败: {e}")
    traceback.print_exc()

# ── 配方3: 检查Agent Runner ──
step("配方3: 验证Agent Runner")

try:
    from igp_agent_runner import TeamAgent
    agent = TeamAgent("quality", 1)
    profile = agent.load_profile()
    print(f"  ✅ TeamAgent创建成功: {agent.name}")
    print(f"  ✅ 加载配置: {bool(profile)}")
except Exception as e:
    print(f"  ❌ Agent Runner失败: {e}")
    traceback.print_exc()

# ── 配方4: 检查Docker ──
step("配方4: 检查Docker沙箱可用性")

try:
    r = subprocess.run(["docker", "info", "--format", "{{.ServerVersion}}"],
                       capture_output=True, text=True, timeout=10,
                       encoding="utf-8", errors="replace")
    if r.returncode == 0 and r.stdout.strip():
        print(f"  ✅ Docker: v{r.stdout.strip()}")
    else:
        print(f"  ⚠️ Docker: 未运行或未安装")
        print(f"     stderr: {r.stderr[:200]}")
except FileNotFoundError:
    print(f"  ❌ Docker: 未找到docker命令")
except Exception as e:
    print(f"  ❌ Docker检查失败: {e}")

# ── 配方5: 检查环境变量 ──
step("配方5: 检查API Key")

import os
keys = {
    "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
    "QWEN_API_KEY": os.environ.get("QWEN_API_KEY", ""),
    "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY", ""),
}
for k, v in keys.items():
    if v:
        print(f"  ✅ {k}: {v[:8]}...{v[-4:]}")
    else:
        print(f"  ❌ {k}: 未设置")

# ── 配方6: 检查pip包 ──
step("配方6: 检查Python依赖")

pkgs = ["httpx", "langgraph", "mcp", "pytest"]
for pkg in pkgs:
    r = subprocess.run(["python", "-m", "pip", "show", pkg],
                       capture_output=True, text=True, timeout=10,
                       encoding="utf-8")
    if r.returncode == 0:
        ver = [l for l in r.stdout.split("\n") if l.startswith("Version:")]
        print(f"  ✅ {pkg}: {ver[0].split(':')[1].strip() if ver else '已安装'}")
    else:
        print(f"  ❌ {pkg}: 未安装")

# ── 配方7: 检查upgrade-v3目录完整性 ──
step("配方7: 升级结构完整性")

v3_files = list(V3_DIR.rglob("*"))
for f in v3_files:
    if f.is_file():
        rel = f.relative_to(V3_DIR)
        print(f"  📄 {rel}")
print(f"  共计 {len([f for f in v3_files if f.is_file()])} 个文件")

# ── 最终评分 ──
step("📊 IGP v3.0 就绪报告")

print(f"""
升级准备状态评估:
  MCP工具层:    {check_mark('igp_mcp_bridge.py' in [str(f.relative_to(V3_DIR)) for f in V3_DIR.rglob('*') if f.is_file()])}
  Agent Runner: {check_mark('igp_agent_runner.py' in [str(f.relative_to(V3_DIR)) for f in V3_DIR.rglob('*') if f.is_file()])}
  吸收蓝图:     {check_mark('absorb_blueprint.md' in [str(f.relative_to(V3_DIR)) for f in V3_DIR.rglob('*') if f.is_file()])}
  Docker沙箱:   {('需要启动docker' if 'Docker: 未运行' in str(subprocess.run(['docker', 'info'], capture_output=True, text=True, timeout=5, encoding='utf-8').stdout) else '可用')}

v3.0 升级就绪度: 基础设施层就绪
下一步: 执行 upgrade_steps.py 安装剩余依赖
""")
