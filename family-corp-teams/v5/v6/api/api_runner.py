"""IGP API 常驻服务启动器 + WatchDog保活 + Windows系统服务就绪"""
from __future__ import annotations
import json
import os
import signal
import subprocess
import sys
import time
import urllib.request
import urllib.error

API_PORT = 8080
V6 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6'
API_SCRIPT = os.path.join(V6, 'api', 'igp_api.py')
PID_FILE = os.path.join(V6, 'api', '.api_pid')
LOG_FILE = os.path.join(V6, 'api', 'api_access.log')


def find_pid_by_port(port: int):
    """通过netstat找到占用端口的PID"""
    try:
        r = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, timeout=5)
        for line in r.stdout.splitlines():
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.strip().split()
                if parts:
                    pid = parts[-1]
                    if pid.isdigit():
                        return int(pid)
    except Exception:
        pass
    return None


def kill_port(port: int):
    """杀掉占用端口的进程"""
    pid = find_pid_by_port(port)
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            time.sleep(0.3)
            # 检查是否还在
            if find_pid_by_port(port) == pid:
                subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True, timeout=3)
            print(f"  已杀掉旧进程 PID={pid}")
        except Exception:
            subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True, timeout=3)
            print(f"  强制杀掉旧进程 PID={pid}")


def start_api():
    """启动API服务（后台模式）"""
    kill_port(API_PORT)
    
    # 写入日志文件
    log = open(LOG_FILE, 'w', encoding='utf-8')
    log.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting API server...\n")
    log.flush()
    
    proc = subprocess.Popen(
        [sys.executable, '-W', 'ignore', '-u', API_SCRIPT, '--port', str(API_PORT)],
        stdout=log, stderr=log,
        creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0,
    )
    
    # 写PID文件
    with open(PID_FILE, 'w') as f:
        f.write(str(proc.pid))
    
    # 等待就绪
    for i in range(10):
        time.sleep(0.5)
        try:
            r = urllib.request.urlopen(f'http://localhost:{API_PORT}/api/v1/health', timeout=2)
            data = json.loads(r.read().decode('utf-8'))
            if data.get('status') == 'ok':
                print(f"  ✅ PID={proc.pid} 服务已就绪 (第{i+1}次尝试)")
                return proc
        except Exception:
            continue
    
    print(f"  ⚠️ 服务启动中但未就绪，PID={proc.pid}，日志在: {LOG_FILE}")
    return proc


def health_check():
    """健康检查"""
    try:
        r = urllib.request.urlopen(f'http://localhost:{API_PORT}/api/v1/health', timeout=3)
        return json.loads(r.read().decode('utf-8'))
    except Exception:
        return None


def restart_if_dead():
    """保活：如果挂了就重启"""
    h = health_check()
    if h and h.get('status') == 'ok':
        return False
    print("  ⚠️ 服务未响应，重启中...")
    start_api()
    time.sleep(1)
    h = health_check()
    return h is not None


def demo_routes():
    """演示所有路由可用"""
    def api_get(path):
        try:
            return json.loads(urllib.request.urlopen(f'http://localhost:{API_PORT}{path}', timeout=5).read().decode())
        except Exception as e:
            return {"error": str(e)}
    
    def api_post(path, data):
        body = json.dumps(data).encode()
        req = urllib.request.Request(f'http://localhost:{API_PORT}{path}', data=body,
                                     headers={'Content-Type': 'application/json'})
        try:
            return json.loads(urllib.request.urlopen(req, timeout=5).read().decode())
        except Exception as e:
            return {"error": str(e)}
    
    routes = [
        ("GET  /api/v1/health", lambda: api_get('/api/v1/health')),
        ("GET  /api/v1/lifecycle", lambda: {"total": api_get('/api/v1/lifecycle').get('total')}),
        ("GET  /api/v1/version/v5_bug_doctor", lambda: api_get('/api/v1/version/v5_bug_doctor')),
        ("POST /api/v1/lifecycle/record", lambda: api_post('/api/v1/lifecycle/record',
            {"product": "v5_bug_doctor", "latency_ms": 10, "success": True})),
        ("POST /api/v1/prd/submit", lambda: api_post('/api/v1/prd/submit',
            {"department": "market", "product": "BugDoctor", "title": "测试PRD", "priority": "low"})),
        ("POST /api/v1/review", lambda: api_post('/api/v1/review',
            {"file": os.path.join(V6, 'v6_lifecycle.py')})),
    ]
    
    print(f"\n{'='*60}")
    print(f"IGP API 路由演示 — http://localhost:{API_PORT}")
    print(f"{'='*60}")
    all_ok = 0
    for route, fn in routes:
        try:
            r = fn()
            if 'error' not in r:
                print(f"  ✅ {route:<45} {list(r.keys())[0]}={list(r.values())[0]}")
                all_ok += 1
            else:
                print(f"  ❌ {route:<45} {r.get('error', 'unknown')}")
        except Exception as e:
            print(f"  ❌ {route:<45} {e}")
    print(f"{'='*60}")
    print(f"  通过: {all_ok}/{len(routes)}")
    return all_ok == len(routes)


if __name__ == '__main__':
    action = sys.argv[1] if len(sys.argv) > 1 else "start"
    
    if action == "start":
        print("启动 IGP API 常驻服务...")
        proc = start_api()
        demo_routes()
        print(f"\n✅ 服务已就绪: http://localhost:{API_PORT}")
        print(f"   PID文件: {PID_FILE}")
        print(f"   日志文件: {LOG_FILE}")
        
    elif action == "stop":
        kill_port(API_PORT)
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
            print("  PID文件已清理")
        print(" ️ 服务已停止")
        
    elif action == "restart":
        kill_port(API_PORT)
        time.sleep(1)
        start_api()
        demo_routes()
        
    elif action == "health":
        h = health_check()
        if h:
            print(f"  ✅ 运行中: {json.dumps(h, ensure_ascii=False)}")
        else:
            print(f"  ❌ 未运行")
            
    elif action == "watch":
        print(f"WatchDog模式 — 每60秒检查 http://localhost:{API_PORT}/api/v1/health")
        print("按 Ctrl+C 退出")
        check_count = 0
        restart_count = 0
        while True:
            check_count += 1
            h = health_check()
            if h and h.get('status') == 'ok':
                ts = time.strftime('%H:%M:%S')
                print(f"  [{ts}] ✅ 运行中 (检查#{check_count})")
            else:
                print(f"  ⚠️ 服务异常，正在重启...")
                start_api()
                restart_count += 1
                h = health_check()
                if h and h.get('status') == 'ok':
                    print(f"  ✅ 重启成功")
                else:
                    print(f"  ❌ 重启失败，等待下轮...")
            time.sleep(60)
            
    elif action == "routes":
        # 不启动服务，仅打印路由
        print(f"\nIGP API 路由表 — http://localhost:{API_PORT}")
        print(f"{'='*60}")
        routes = [
            ("GET", "/api/v1/health", "健康检查"),
            ("GET", "/api/v1/lifecycle", "产品总览（按stage分组）"),
            ("GET", "/api/v1/lifecycle/products?stage=ga", "按stage筛选"),
            ("GET", "/api/v1/lifecycle/product/<key>", "单个产品详情+metrics"),
            ("GET", "/api/v1/version/<key>", "版本号+变更日志"),
            ("POST", "/api/v1/lifecycle/record", "提交调用记录"),
            ("POST", "/api/v1/lifecycle/upgrade", "升级产品stage"),
            ("POST", "/api/v1/lifecycle/version", "设置版本号"),
            ("POST", "/api/v1/lifecycle/record", "记录调用（含latency/success）"),
            ("GET", "/api/v1/v5", "调试：存活产品列表"),
            ("POST", "/api/v1/prd/submit", "提交PRD需求"),
            ("GET", "/api/v1/prd", "PRD队列摘要"),
            ("GET", "/api/v1/prd/list", "PRD全队列（按status分组）"),
            ("POST", "/api/v1/review", "三Agent评审文件"),
        ]
        for method, path, desc in routes:
            print(f"  {method:<6} {path:<40} {desc}")
        
    else:
        print(f"用法: python {__file__} [start|stop|restart|health|watch|routes]")
        print(f"  start   — 启动服务（默认）")
        print(f"  stop    — 停止服务")
        print(f"  restart — 重启服务")
        print(f"  health  — 健康检查")
        print(f"  watch   — 保活模式（每分钟检查）")
        print(f"  routes  — 打印路由表")
