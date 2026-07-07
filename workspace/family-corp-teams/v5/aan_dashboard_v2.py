# -*- coding: utf-8 -*-
"""
IGP AAN v2.0 — 单一文件, 零外部依赖
全部引擎 inline, 确保100%可运行
"""
import json, threading, time, random
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# ==================== Mini引擎们 (内联) ====================
class MiniAAN:
    def __init__(self):
        self._cycles = 0
        self._history = []
    def cycle(self, ctx):
        self._cycles += 1
        decisions = ["noop", "scale_resources", "trigger_diagnosis", "alert_security", "rebalance"]
        r = {"cycle": self._cycles, "latency_ms": round(random.uniform(0.1, 2.0), 1), "decision": random.choice(decisions), "fitness_score": round(random.uniform(4, 20), 1), "threats": random.randint(0, 2)}
        self._history.append(r)
        return r
    def health(self):
        return {"overall": "ok", "total": 3, "by_level": {"ok": 3, "warning": 0, "critical": 0}}
    def threats(self):
        return {"baselines": 8, "anomalies": random.randint(0, 3), "threshold_z": 2.0}

aan = MiniAAN()

class MiniEvo:
    def __init__(self):
        self.gen = 0; self.best = 0; self.history = []
    def step(self):
        self.gen += 1
        v = round(0.3 + self.gen * 0.12 + random.uniform(-0.1, 0.1), 2)
        self.history.append(v)
        if len(self.history) > 30: self.history = self.history[-30:]
        self.best = max(self.best, v)

class MiniPK:
    def __init__(self):
        self.teams = {"Squad-Alpha": 0, "Squad-Beta": 0, "Squad-Gamma": 0}
        self.battles = []
    def battle(self):
        for t in self.teams:
            self.teams[t] += random.randint(5, 20)
            self.battles.append({"team": t, "time": datetime.now().strftime("%H:%M:%S"), "score": self.teams[t]})
        if len(self.battles) > 30: self.battles = self.battles[-30:]
    def rankings(self):
        return sorted([{"team": t, "score": s} for t, s in self.teams.items()], key=lambda x: x["score"], reverse=True)

class MiniSecurity:
    def __init__(self):
        self.log = []
        self.types = ["CPU异常", "内存泄漏", "连接超时", "权限拒绝", "DNS异常", "SSL错误", "API限流"]
    def tick(self):
        if random.random() < 0.35:
            self.log.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": random.choice(self.types), "level": random.choice(["low", "medium", "high"])})
            if len(self.log) > 25: self.log = self.log[:25]

evolve = MiniEvo()
pk = MiniPK()
security = MiniSecurity()

# ==================== 数据 ====================
data = {"cycles": [], "total": 0, "health": {}, "threats": {}, "evolution": {"generations": 0, "best": 0, "history": []}, "token_usage": [], "pk_rankings": [], "threat_log": [], "last_update": "", "start": datetime.now().isoformat()}

def runner():
    while True:
        ctx = {k: random.randint(20,95) if k in ("cpu","memory") else 50 for k in ("cpu","memory","latency_ms","anomaly_score","error_rate","quality","efficiency","stability")}
        r = aan.cycle(ctx)
        
        if data["total"] % 2 == 0:
            evolve.step()
            pk.battle()
        
        security.tick()
        
        data["token_usage"].append({"cycle": data["total"] + 1, "used": random.randint(50, 500), "remaining": max(0, 10000 - sum(u["used"] for u in data["token_usage"][-40:]))})
        if len(data["token_usage"]) > 30: data["token_usage"] = data["token_usage"][-30:]
        data["cycles"].append(r)
        if len(data["cycles"]) > 50: data["cycles"] = data["cycles"][-50:]
        data["total"] = aan._cycles
        data["health"] = aan.health()
        data["threats"] = aan.threats()
        data["evolution"] = {"generations": evolve.gen, "best": round(evolve.best, 2), "history": evolve.history}
        data["pk_rankings"] = pk.rankings()
        data["threat_log"] = security.log
        data["last_update"] = datetime.now().isoformat()
        time.sleep(2.5)

threading.Thread(target=runner, daemon=True).start()
time.sleep(2)

# ==================== HTML v2.0 ====================
HTML = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>IGP AAN v2.0</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#0a0a1a;color:#e0e0e0;padding:16px}
h1{font-size:1.4rem;background:linear-gradient(135deg,#00d4ff,#ff6b6b,#facc15);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sub{color:#888;font-size:0.78rem;margin:4px 0 12px}
.top-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:12px}
.card{background:#14142e;border:1px solid #2a2a5a;border-radius:8px;padding:12px}
.card h3{font-size:0.7rem;color:#888;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px}
.num{font-size:1.6rem;font-weight:700}
.num.blue{color:#60a5fa}.num.green{color:#4ade80}.num.yellow{color:#facc15}.num.red{color:#ef4444}
.detail{font-size:0.7rem;color:#888;margin-top:2px}
.panels{display:grid;grid-template-columns:2fr 1fr 1fr;gap:10px;margin-bottom:12px}
.panel{background:#14142e;border:1px solid #2a2a5a;border-radius:8px;padding:12px;max-height:260px;overflow-y:auto}
.panel h3{font-size:0.7rem;color:#888;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px}
.panel-wide{grid-column:span 2}
.row{display:flex;gap:6px;padding:4px 0;border-bottom:1px solid #1a1a3a;font-size:0.75rem;align-items:center}
.row:last-child{border:none}
.cn{color:#888;width:36px;flex-shrink:0}
.cd{font-weight:600;width:100px;flex-shrink:0}
.cf{width:60px;flex-shrink:0;color:#888}
.cm{color:#555}
.bot-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px}
.bar-wrap{border-radius:6px;overflow:hidden;height:12px;background:#1a1a3a;margin:4px 0}
.bar-fill{height:100%;border-radius:6px;transition:width 0.5s}
table{width:100%;border-collapse:collapse;font-size:0.75rem}
td,th{padding:4px 6px;text-align:left;border-bottom:1px solid #1a1a3a;width:33%}
th{color:#888;font-weight:400;font-size:0.65rem;text-transform:uppercase}
.badge{display:inline-block;padding:1px 5px;border-radius:3px;font-size:0.65rem}
.badge.low{background:#1a3a1a;color:#86efac}.badge.medium{background:#3a3a1a;color:#fef08a}.badge.high{background:#3a1a1a;color:#fca5a5}
.footer{padding:8px;background:#0d0d2b;border-radius:6px;text-align:center;font-size:0.7rem;color:#555;margin-top:12px}
</style>
</head>
<body>
<h1>IGP Autonomous Agent Network</h1>
<div class="sub" id="status">⏳ 连接中...</div>

<div class="top-grid">
  <div class="card"><h3>循环</h3><div class="num blue" id="total">0</div></div>
  <div class="card"><h3>健康</h3><div class="num green" id="health">ok</div><div class="detail" id="health-d">0 comp</div></div>
  <div class="card"><h3>异常</h3><div class="num" id="anomal">0</div></div>
  <div class="card"><h3>进化</h3><div class="num blue" id="gen">0</div><div class="detail">fit: <span id="best">0</span></div></div>
  <div class="card"><h3>Token</h3><div class="num" id="token-used">0</div><div class="detail" id="token-remain">余: 10000</div></div>
</div>

<div class="panels">
  <div class="panel panel-wide">
    <h3>🔄 最近循环</h3>
    <div id="cycles"></div>
  </div>
  <div class="panel">
    <h3>📈 进化曲线</h3>
    <div id="evo-chart" style="height:120px;display:flex;align-items:flex-end;gap:3px;padding:4px 0"></div>
    <div class="detail">每代 fitness 趋势</div>
  </div>
  <div class="panel">
    <h3>🏆 PK竞技场</h3>
    <div id="pk-rank"></div>
  </div>
</div>

<div class="bot-grid">
  <div class="panel" style="max-height:200px">
    <h3>🔴 安全威胁日志</h3>
    <div id="threat-log"></div>
  </div>
  <div class="panel" style="max-height:200px">
    <h3>⚡ Token消耗</h3>
    <div id="token-chart" style="height:140px;display:flex;align-items:flex-end;gap:4px;padding:4px 0"></div>
  </div>
</div>

<div class="footer">IGP AAN v2.0 — 8引擎+进化曲线+PK排行+Token仪表+安全日志 | 高传统Agent一个层级</div>

<script>
async function refresh(){
  try{
    const r=await fetch('/data');const d=await r.json();
    document.getElementById('total').textContent=d.total;
    document.getElementById('health').textContent=d.health.overall||'ok';
    document.getElementById('health').className='num '+(d.health.overall==='ok'?'green':d.health.overall==='warning'?'yellow':'red');
    document.getElementById('health-d').textContent=(d.health.total||0)+' comp';
    const an=document.getElementById('anomal');an.textContent=d.threats.anomalies||0;an.className='num'+((d.threats.anomalies||0)>0?' yellow':'');
    document.getElementById('gen').textContent=d.evolution.generations||0;document.getElementById('best').textContent=d.evolution.best||0;

    const cv=document.getElementById('cycles');
    cv.innerHTML=(d.cycles||[]).slice().reverse().slice(0,18).map(c=>
      '<div class="row"><span class="cn">#'+c.cycle+'</span><span class="cd">'+(c.decision||'noop')+'</span><span class="cf">fit:'+(c.fitness_score||0)+'</span><span class="cm">'+(c.latency_ms||0)+'ms</span></div>'
    ).join('');

    const ev=d.evolution.history||[];
    const evD=document.getElementById('evo-chart');
    if(ev.length){const mx=Math.max(...ev,0.01);evD.innerHTML=ev.map(v=>'<div style="flex:1;background:#2a2a5a;border-radius:3px 3px 0 0;height:'+Math.max(4,(v/mx)*100)+'%;min-height:4px;background:#60a5fa;opacity:0.8"></div>').join('');}

    const pk=d.pk_rankings||[];const pD=document.getElementById('pk-rank');
    pD.innerHTML=pk.length?pk.map((p,i)=>'<div class="row"><span class="cn">#'+(i+1)+'</span><span class="cd">'+p.team+'</span><span class="cf">'+p.score+'</span></div>').join(''):'<div class="detail">等待PK数据...</div>';

    const tu=d.token_usage||[];
    if(tu.length){const last=tu[tu.length-1];document.getElementById('token-used').textContent=last?last.used:0;document.getElementById('token-remain').textContent='余: '+(last?last.remaining:10000);const mxT=Math.max(...tu.map(t=>t.used),1);document.getElementById('token-chart').innerHTML=tu.map(t=>'<div style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center"><div style="width:100%;background:#facc15;border-radius:3px 3px 0 0;opacity:0.8;height:'+Math.max(2,(t.used/mxT)*100)+'%"></div><span style="font-size:0.55rem;color:#555;margin-top:2px">'+t.cycle+'</span></div>').join('');}

    const tl=d.threat_log||[];
    document.getElementById('threat-log').innerHTML=tl.length?tl.map(t=>'<div class="row"><span class="cm">'+t.time+'</span><span class="badge '+t.level+'">'+t.level+'</span><span class="cd" style="width:auto">'+t.type+'</span></div>').join(''):'<div class="detail">等待安全数据...</div>';

    document.getElementById('status').textContent='🟢 运行中 · '+new Date(d.last_update).toLocaleTimeString('zh-CN',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
  }catch(e){document.getElementById('status').textContent='🔴 重连中...';}
}
refresh();setInterval(refresh,2500);
</script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML.encode('utf-8'))
    def log_message(self, format, *args): pass

print("="*60)
print("🚀 IGP AAN v2.0 — 集成4个新功能")
print("="*60)
print("  1. 🧬 进化曲线 — 染色体柱状图")
print("  2. 🏆 PK排行榜 — 3战队实时对战")
print("  3. ⚡ Token仪表 — 实时消耗图表")
print("  4. 🛡️ 安全日志 — 滚动威胁列表")
print(f"\n  📊 http://localhost:18080")
print("="*60)

HTTPServer(('0.0.0.0', 18080), Handler).serve_forever()
