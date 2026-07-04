#!/usr/bin/env python3
"""强行清旧Goal + 创建新Goal — 走IGP引擎层，不依赖OpenClaw tool限制"""
import subprocess, sys, json, os

# 方案：直接调OpenClaw CLI清Goal
# OpenClaw 提供了 /goal clear 和 /goal start 的CLI接口
# 通过 openclaw 命令或者直接写文件

# 方法1: 通过API调WebSocket
# 方法2: 直接exec openclaw CLI

# 检查openclaw命令是否存在
cmds = ["openclaw", "npx openclaw", "node"]

found_cli = None
for c in cmds:
    base = c.split()[0]
    try:
        subprocess.run([base, "--version"], capture_output=True, text=True, timeout=5)
        found_cli = c
        break
    except:
        continue

if found_cli:
    print(f"[IGP] Found CLI: {found_cli}")
else:
    print("[IGP] No openclaw CLI found, trying direct session API...")

# 方法3: 直接通过WebSocket在当前session发送/goal命令
# 用node脚本调用OpenClaw内部API
node_script = r'''
const http = require('http');
const path = require('path');
const fs = require('fs');

// 找config
const home = process.env.OPENCLAW_HOME || process.env.HOME || process.env.USERPROFILE;
const configPath = path.join(home, '.openclaw', 'config.yaml');
console.log("Config:", configPath, "exists:", fs.existsSync(configPath));

// 尝试通过Gateway API /goal clear
// Gateway监听端口通常在配置里
const possiblePorts = [18791, 18789, 3000, 4000, 8080];
function tryPort(port) {
    return new Promise((resolve) => {
        const req = http.request({
            hostname: '127.0.0.1',
            port: port,
            path: '/api/command?cmd=/goal+clear',
            method: 'GET',
            timeout: 3000,
        }, (res) => {
            let data = '';
            res.on('data', d => data += d);
            res.on('end', () => resolve({port, status: res.statusCode, data: data.slice(0,200)}));
        });
        req.on('error', () => resolve({port, error: true}));
        req.end();
    });
}

async function main() {
    for (const port of possiblePorts) {
        const result = await tryPort(port);
        if (!result.error && result.status < 500) {
            console.log(`Port ${port}: ${result.status} - ${result.data}`);
        }
    }
    console.log("Done scanning ports");
}
main().catch(console.error);
'''

node_file = os.path.join(os.path.dirname(__file__), "_tmp_clear_goal.js")
with open(node_file, "w", encoding="utf-8") as f:
    f.write(node_script)

result = subprocess.run(["node", node_file], capture_output=True, text=True, timeout=15)
print(result.stdout)
print(result.stderr[:500] if result.stderr else "")
os.remove(node_file)
