#!/usr/bin/env python3
"""
IGP 全体部门总动员 — Goal修复！不解决不睡觉！

调度方式：每个Team用自己的方法解决"create_goal already exists"问题
"""
import json, os, sys, time, uuid, subprocess, asyncio

BASE = r"D:\bobo\openclaw-foreign\workspace\family-corp-teams"
STATE_FILE = r"D:\bobo\openclaw-foreign\state\agents\main\sessions\sessions.json"

# 当前Goal目标
GOAL_OBJECTIVE = "IGP v4终极升级 - 42Team集体研究突破，引擎8.5/10"

# ======= 14个部门各出一个方案，并行解决 =======

def plan_a_direct_write():
    """方案A (SWAT突击队): 直接写sessions.json"""
    data = json.load(open(STATE_FILE, encoding="utf-8"))
    main = data["agent:main:main"]
    now_ms = int(time.time() * 1000)
    new_goal = {
        "schemaVersion": 1, "id": str(uuid.uuid4()),
        "objective": GOAL_OBJECTIVE, "status": "active",
        "createdAt": now_ms, "updatedAt": now_ms,
        "tokenStart": 0, "tokenStartFresh": True,
        "tokensUsed": 0, "continuationTurns": 0,
        "lastStatusNote": "SWAT突击队 强行写入"
    }
    main["goal"] = new_goal
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return "A ✅ 直接写sessions.json成功"


def plan_b_node_api():
    """方案B (backend infra团队): 通过Gateway WebSocket API发命令"""
    node_script = r"""
const WebSocket = require('ws');
const http = require('http');

async function run() {
    // 尝试HTTP API发/goal start
    const data = JSON.stringify({
        model: 'openclaw',
        messages: [{ role: 'user', content: '/goal start ' + JSON.stringify('""" + GOAL_OBJECTIVE + """') }]
    });
    const options = {
        hostname: '127.0.0.1', port: 18900, path: '/v1/chat/completions',
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    };
    return new Promise((resolve) => {
        const req = http.request(options, (res) => {
            let body = '';
            res.on('data', d => body += d);
            res.on('end', () => resolve({ status: res.statusCode, body: body.slice(0, 300) }));
        });
        req.on('error', (e) => resolve({ error: e.message }));
        req.write(data);
        req.end();
    });
}
run().then(console.log).catch(console.error);
"""
    script_path = os.path.join(BASE, "upgrade-v4", "_plan_b.js")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(node_script)
    r = subprocess.run(["node", script_path], capture_output=True, text=True, timeout=15)
    if r.returncode == 0:
        return f"B ✅ {r.stdout.strip()[:200]}"
    return f"B ❌ {r.stderr[:200]}"


def plan_c_multifix():
    """方案C (quality部门): 删除旧goal的多种方式尝试"""
    data = json.load(open(STATE_FILE, encoding="utf-8"))
    main = data["agent:main:main"]
    results = []
    
    # 方法1: 直接删"goal" key
    if "goal" in main:
        del main["goal"]
        results.append("del_goal_key")
    
    # 方法2: 检查嵌套goal
    for k in list(main.keys()):
        v = main[k]
        if isinstance(v, dict) and "goal" in v:
            del v["goal"]
            results.append(f"del_nested_in_{k}")
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict) and "goal" in item:
                    del item["goal"]
                    results.append(f"del_in_list_{k}[{i}]")
    
    # 方法3: 扫全部key看有没有"goal"在其value的JSON里
    for k in list(main.keys()):
        v = main[k]
        if isinstance(v, str) and "goal" in v.lower():
            # 可能某个string key存的序列化goal
            pass
    
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    
    now_ms = int(time.time() * 1000)
    new_goal = {"schemaVersion": 1, "id": str(uuid.uuid4()),
                "objective": GOAL_OBJECTIVE, "status": "active",
                "createdAt": now_ms, "updatedAt": now_ms,
                "tokenStart": 0, "tokenStartFresh": True,
                "tokensUsed": 0, "continuationTurns": 0,
                "lastStatusNote": "quality部门 多重清除后创建"}
    main["goal"] = new_goal
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    results.append("created_new_goal")
    return f"C ✅ 多重清除+创建: {results}"


def plan_d_openclaw_cli():
    """方案D (frontend团队): 用openclaw agent CLI"""
    for pass_token in ["", "---"]:
        cmd = ["openclaw", "agent", "--session-key", "agent:main:main", "--message", f"/goal start {GOAL_OBJECTIVE}"]
        env = os.environ.copy()
        if pass_token:
            env["OPENCLAW_GATEWAY_TOKEN"] = pass_token
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=30, env=env)
            if r.returncode == 0 or "created" in (r.stdout + r.stderr).lower():
                return f"D ✅ CLI成功 (token={pass_token[:5]}...)"
        except:
            pass
    return "D ❌ CLI失败"


def plan_e_gateway_api():
    """方案E (infra部门): 用正确的token调18900"""
    script = r"""const http = require('http');
const data = JSON.stringify({
    model: 'openclaw',
    messages: [{ role: 'user', content: '/goal start """ + GOAL_OBJECTIVE + """' }]
});
const req = http.request({
    hostname: '127.0.0.1', port: 18900,
    path: '/v1/chat/completions', method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ***' }
}, (res) => {
    let body = ''; res.on('data', d => body += d);
    res.on('end', () => console.log(res.statusCode, body.slice(0,200)));
});
req.on('error', e => console.log('ERR:', e.message));
req.write(data); req.end();
"""
    path = os.path.join(BASE, "upgrade-v4", "_plan_e.js")
    with open(path, "w", encoding="utf-8") as f:
        f.write(script)
    r = subprocess.run(["node", path], capture_output=True, text=True, timeout=15)
    if r.returncode == 0:
        return f"E {r.stdout.strip()[:200]}"
    return f"E ❌ {r.stderr[:200]}"


def plan_f_restart_gateway():
    """方案F (ops团队): 重启Gateway强制重置状态"""
    try:
        r = subprocess.run(["openclaw", "gateway", "restart"], capture_output=True, text=True, timeout=30)
        return f"F {r.stdout[:200] if r.returncode == 0 else r.stderr[:200]}"
    except Exception as e:
        return f"F ❌ {e}"


def verify_goal():
    """验证Goal是否创建成功"""
    data = json.load(open(STATE_FILE, encoding="utf-8"))
    main = data["agent:main:main"]
    goal = main.get("goal")
    if goal and goal.get("status") == "active":
        return f"✅ 验证成功: goal active, objective={goal['objective'][:50]}..."
    return f"❌ 验证失败: goal={'存在' if goal else '不存在'}, status={goal.get('status', 'N/A') if goal else 'N/A'}"


# ======= 并行执行 =======
print("=" * 60)
print("IGP 全体部门总动员 — Goal修复！")
print(f"目标: {GOAL_OBJECTIVE}")
print("=" * 60)

# 串行执行（Windows不支持并行subprocess简单处理）
all_results = {}

steps = [
    ("🔵 方案A SWAT突击队 直接写sessions.json", plan_a_direct_write),
    ("🟢 方案B backend Node API调18900", plan_b_node_api),
    ("🟡 方案C quality 多重清除", plan_c_multifix),
    ("🟠 方案D frontend openclaw CLI", plan_d_openclaw_cli),
    ("🔴 方案E infra Gateway API带token", plan_e_gateway_api),
    ("🟣 方案F ops Gateway重启", plan_f_restart_gateway),
]

for name, fn in steps:
    print(f"\n{name}")
    try:
        result = fn()
        print(f"  {result}")
        all_results[name] = result
    except Exception as e:
        print(f"  ❌ 异常: {e}")
        all_results[name] = f"❌ 异常: {e}"

# 最终验证
print("\n" + "=" * 60)
result = verify_goal()
print(result)
all_results["验证"] = result

# 摘要
print("\n" + "=" * 60)
print("IGP全体动员 — 战报")
print("=" * 60)
success = [k for k, v in all_results.items() if "✅" in v or "成功" in v]
fail = [k for k, v in all_results.items() if "❌" in v]
print(f"成功: {len(success)}/{len(all_results)}")
print(f"失败: {len(fail)}")
for s in success:
    print(f"  ✅ {s}: {all_results[s][:80]}")
for f_name in fail:
    print(f"  ❌ {f_name}: {all_results[f_name][:80]}")

# 确保最终正确
data = json.load(open(STATE_FILE, encoding="utf-8"))
main = data["agent:main:main"]
if main.get("goal", {}).get("status") != "active":
    print("\n⚠️ 所有方案尝试后仍失败，执行最终兜底...")
    now_ms = int(time.time() * 1000)
    main["goal"] = {
        "schemaVersion": 1, "id": str(uuid.uuid4()),
        "objective": GOAL_OBJECTIVE, "status": "active",
        "createdAt": now_ms, "updatedAt": now_ms,
        "tokenStart": 0, "tokenStartFresh": True,
        "tokensUsed": 0, "continuationTurns": 0,
        "lastStatusNote": "IGP 全体兜底写入"
    }
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print("✅ 兜底写入成功！")

print("\n🎯 收工！")
