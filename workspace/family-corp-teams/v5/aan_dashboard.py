# -*- coding: utf-8 -*-
"""
AAN Web Dashboard — 实时展示自治智能体网络
"""
import json, os, sys, threading, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

sys.path.insert(0, r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5")

try:
    from aan_v1 import AAN
except:
    pass

# ========= AAN 引擎 =========
aan = AAN()
aan.setup()

dashboard_data = {
    "cycles": [],
    "total_cycles": 0,
    "health": {},
    "threats": {},
    "evolution": {},
    "last_update": ""
}

def run_aan_cycles():
    """后台跑 AAN 循环"""
    import random
    while True:
        ctx = {
            "cpu": random.randint(20, 95),
            "memory": random.randint(30, 92),
            "latency_ms": random.randint(50, 1200),
            "anomaly_score": round(random.uniform(0.01, 0.95), 2),
            "error_rate": round(random.uniform(0.001, 0.15), 3),
            "quality": random.randint(2, 9),
            "efficiency": random.randint(2, 9),
            "stability": random.randint(2, 9)
        }
        r = aan.cycle(ctx)
        dashboard_data["cycles"].append(r)
        if len(dashboard_data["cycles"]) > 50:
            dashboard_data["cycles"] = dashboard_data["cycles"][-50:]
        dashboard_data["total_cycles"] = aan._cycles
        dashboard_data["health"] = aan.health.summary()
        dashboard_data["threats"] = aan.threat.report()
        dashboard_data["evolution"] = aan.evolution.summary()
        dashboard_data["last_update"] = datetime.now().isoformat()
        time.sleep(3)

t = threading.Thread(target=run_aan_cycles, daemon=True)
t.start()

# ========= Web Dashboard =========
HTML = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IGP AAN Dashboard</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family: 'Segoe UI', system-ui, sans-serif; background:#0a0a1a; color:#e0e0e0; padding:20px; }
  h1 { font-size:1.5rem; margin-bottom:8px; background:linear-gradient(135deg,#00d4ff,#ff6b6b); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
  .sub { color:#888; font-size:0.85rem; margin-bottom:20px; }
  .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:16px; margin-bottom:20px; }
  .card { background:#14142e; border:1px solid #2a2a5a; border-radius:12px; padding:16px; }
  .card h3 { font-size:0.85rem; color:#888; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px; }
  .card .big { font-size:2rem; font-weight:700; margin-bottom:4px; }
  .card .big.green { color:#4ade80; }
  .card .big.yellow { color:#facc15; }
  .card .big.red { color:#ef4444; }
  .card .big.blue { color:#60a5fa; }
  .card .detail { font-size:0.8rem; color:#888; line-height:1.6; }
  .cycle-row { display:flex; gap:8px; padding:6px 10px; border-bottom:1px solid #1a1a3a; font-size:0.8rem; }
  .cycle-row:last-child { border-bottom:none; }
  .cycle-num { color:#888; width:60px; flex-shrink:0; }
  .cycle-decision { font-weight:600; width:140px; flex-shrink:0; }
  .cycle-fitness { width:80px; flex-shrink:0; }
  .cycle-time { color:#888; }
  .badge { display:inline-block; padding:2px 8px; border-radius:4px; font-size:0.75rem; margin:1px; }
  .badge.green { background:#166534; color:#bbf7d0; }
  .badge.yellow { background:#713f12; color:#fef08a; }
  .badge.red { background:#7f1d1d; color:#fecaca; }
  table { width:100%; border-collapse:collapse; font-size:0.8rem; }
  td, th { padding:6px 8px; text-align:left; border-bottom:1px solid #1a1a3a; }
  th { color:#888; font-weight:400; text-transform:uppercase; font-size:0.7rem; }
  .status-bar { margin-top:20px; padding:10px; border-radius:8px; background:#0d0d2b; text-align:center; font-size:0.75rem; color:#555; }
</style>
</head>
<body>
<h1>IGP Autonomous Agent Network</h1>
<div class="sub" id="status">⏳ 连接中...</div>

<div class="grid" id="stats-grid">
  <div class="card"><h3>总循环</h3><div class="big blue" id="total">0</div><div class="detail">cycles completed</div></div>
  <div class="card"><h3>系统健康</h3><div class="big green" id="health">ok</div><div class="detail" id="health-detail">0 components</div></div>
  <div class="card"><h3>异常检测</h3><div class="big" id="anomalies">0</div><div class="detail" id="anomalies-detail">threats detected</div></div>
  <div class="card"><h3>进化代数</h3><div class="big" id="generations">0</div><div class="detail" id="evolution-detail">best: 0</div></div>
</div>

<div class="grid" style="grid-template-columns:1fr 1fr;">
  <div class="card">
    <h3>🔄 最近循环</h3>
    <div id="cycles"></div>
  </div>
  <div class="card">
    <h3>📋 对比表 — AAN vs 传统Agent</h3>
    <table>
      <tr><th>能力</th><th>传统</th><th>AAN</th></tr>
      <tr><td>路由</td><td>静态</td><td class="green">Dijkstra</td></tr>
      <tr><td>诊断</td><td>无</td><td class="green">预测分析</td></tr>
      <tr><td>决策</td><td>硬编码</td><td class="green">矩阵规则</td></tr>
      <tr><td>进化</td><td>无</td><td class="green">染色体</td></tr>
      <tr><td>安全</td><td>无</td><td class="green">Z-score</td></tr>
      <tr><td>记忆</td><td>单层</td><td class="green">两级+配额</td></tr>
      <tr><td>合规</td><td>无</td><td class="green">自动审计</td></tr>
      <tr><td>通信</td><td>无</td><td class="green">加密A2A</td></tr>
      <tr style="font-weight:700"><td>引擎数</td><td>1-2</td><td class="big">8</td></tr>
    </table>
  </div>
</div>

<div class="status-bar">IGP AAN v1.0 — 8个引擎全链路自治 | 延迟 &lt;1ms/cycle</div>

<script>
async function refresh() {
  try {
    const r = await fetch('/data');
    const d = await r.json();
    document.getElementById('total').textContent = d.total_cycles;
    document.getElementById('health').textContent = d.health.overall || 'ok';
    document.getElementById('health').className = 'big ' + (d.health.overall === 'ok' ? 'green' : d.health.overall === 'warning' ? 'yellow' : 'red');
    document.getElementById('health-detail').textContent = (d.health.total || 0) + ' components';
    document.getElementById('anomalies').textContent = d.threats.anomalies || 0;
    document.getElementById('anomalies').className = 'big ' + ((d.threats.anomalies || 0) > 0 ? 'red' : '');
    document.getElementById('generations').textContent = d.evolution.generations || 0;
    document.getElementById('evolution-detail').textContent = 'best: ' + (d.evolution.best || 0);
    document.getElementById('status').textContent = '🟢 运行中 — 最后更新: ' + new Date(d.last_update).toLocaleTimeString();

    const cyclesDiv = document.getElementById('cycles');
    cyclesDiv.innerHTML = (d.cycles || []).slice().reverse().slice(0,15).map(c => 
      '<div class="cycle-row"><span class="cycle-num">#' + c.cycle + '</span>' +
      '<span class="cycle-decision">' + (c.decision || 'noop') + '</span>' +
      '<span class="cycle-fitness">fit: ' + (c.fitness_score || 0) + '</span>' +
      '<span class="cycle-time">' + (c.latency_ms || 0) + 'ms</span></div>'
    ).join('');
  } catch(e) {
    document.getElementById('status').textContent = '🔴 连接失败: ' + e.message;
  }
}
refresh();
setInterval(refresh, 3000);
</script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            data = {
                "total_cycles": dashboard_data["total_cycles"],
                "health": dashboard_data["health"],
                "threats": dashboard_data["threats"],
                "evolution": dashboard_data["evolution"],
                "last_update": dashboard_data["last_update"],
                "cycles": dashboard_data["cycles"][-20:]
            }
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML.encode('utf-8'))
    def log_message(self, format, *args): pass

port = 18080
server = HTTPServer(('0.0.0.0', port), Handler)
print(f"\n{'='*60}")
print(f"🚀 IGP AAN Dashboard")
print(f"   地址: http://localhost:{port}")
print(f"   刷新: 每3秒自动更新")
print(f"   引擎: 8个全链路集成")
print(f"{'='*60}\n")
server.serve_forever()
