"""
IGP 研发部 V6 - HTTP API 服务器
纯 stdlib http.server,0依赖
研发部所有产品通过RESTful API对外开放
"""
from __future__ import annotations
import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Any, Dict

# 添加路径
V6_DIR = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6'
sys.path.insert(0, v6_dir := V6_DIR)
sys.path.insert(0, os.path.join(v6_dir, '..'))

# IGP 全部门注册表 - 全员可通过API查询
DEPARTMENT_REGISTRY = {
    'chromosome0': {'name': '变异裂变中心', 'files': 2, 'tests': 3},
    'chromosome1': {'name': 'MCP协议部', 'files': 5, 'tests': 1},
    'chromosome2': {'name': 'A2A协议部', 'files': 1, 'tests': 0},
    'chromosome3': {'name': '市场扩展部', 'files': 2, 'tests': 0},
    'chromosome4': {'name': 'Provider路由器', 'files': 6, 'tests': 4},
    'chromosome5': {'name': '治理/政策部', 'files': 5, 'tests': 2},
    'chromosome6': {'name': '商业部', 'files': 2, 'tests': 1},
    'chromosome7': {'name': 'Agent OS部', 'files': 4, 'tests': 1},
    'chromosome8': {'name': 'AP2协议部', 'files': 4, 'tests': 5},
    'chromosome9': {'name': 'Bug检查部', 'files': 2, 'tests': 2},
    'chromosome10': {'name': '逻辑推理部', 'files': 2, 'tests': 3},
    'chromosome11': {'name': '类型/度量部', 'files': 1, 'tests': 1},
    'chromosome12': {'name': '自动测试部', 'files': 5, 'tests': 6},
    'chromosome13': {'name': '硅胶体记忆部 🧠', 'files': 3, 'tests': 2, 'routes': ['consolidate', 'fusion', 'hot', 'timeline']},
    'chromosome14': {'name': '智能路由部', 'files': 0, 'tests': 0},
    'chromosome15': {'name': '审计安全部', 'files': 0, 'tests': 0},
    'chromosome16': {'name': 'IGP基础设施部', 'files': 6, 'tests': 0},
    'chromosome17': {'name': 'DevOps部', 'files': 4, 'tests': 0},
    'chromosome18': {'name': '核心引擎部', 'files': 8, 'tests': 0},
    'chromosome19': {'name': '产品交付部', 'files': 5, 'tests': 5},
    'hq_swat': {'name': 'SWAT突击队', 'desc': '紧急事件、跨部门难题'},
    'hq_audit': {'name': '审计部', 'desc': '绩效追溯、淘汰核查'},
    'hq_strategy': {'name': '战略投资部', 'desc': '外部扫描、新部门立项'},
}

# 延迟导入(避免启动报错)
_lifecycle = None
_review = None
_prd = None
_memory = None


_memory_registry = {}
"""
部门记忆注册表 - 所有19个IGP部门可通过API存取记忆
每个部门有独立的记忆槽(slot),互不干扰
"""


def _reg_memory():
    """初始化硅胶体记忆,全员/全部门共享"""
    global _memory
    if _memory is None:
        try:
            mem_dir = os.path.join(V6_DIR, 'silicon_memory')
            sys.path.insert(0, mem_dir)
            from v5_silicon_memory import SiliconMemory
            _memory = SiliconMemory()
        except Exception as e:
            print(f"[WARN] 硅胶体记忆初始化失败: {e}")
            _memory = None
    return _memory


def get_lifecycle():
    global _lifecycle
    if _lifecycle is None:
        from v6.v6_lifecycle import LifecycleManager
        _lifecycle = LifecycleManager(os.path.join(V6_DIR, 'product_registry.json'))
    return _lifecycle


def get_review():
    global _review
    if _review is None:
        from v6.review.v6_review_agents import review_file
        _review = review_file
    return _review


def get_prd():
    global _prd
    if _prd is None:
        from v6.prd.prd_queue import PRDQueue
        _prd = PRDQueue(V6_DIR)
    return _prd


class IGPAPIHandler(BaseHTTPRequestHandler):
    """IGP API 请求处理"""

    def _send_json(self, data: Any, status: int = 200):
        body = json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> Dict:
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode('utf-8'))

    # ======== GET ========

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        params = parse_qs(parsed.query)

        try:
            if path == '/api/v1/health':
                self._send_json({"status": "ok", "version": "v6.0.0", "service": "IGP RD API"})

            elif path == '/api/v1/lifecycle':
                lm = get_lifecycle()
                self._send_json(lm.summary())

            elif path == '/api/v1/lifecycle/products':
                lm = get_lifecycle()
                stage = params.get('stage', [None])[0]
                prods = lm.list_products(stage=stage)
                self._send_json({"total": len(prods), "products": prods})

            elif path.startswith('/api/v1/lifecycle/product/'):
                key = path.split('/')[-1]
                lm = get_lifecycle()
                p = lm.get_product(key)
                if p:
                    self._send_json(p)
                else:
                    self._send_json({"error": f"Product '{key}' not found"}, 404)

            elif path.startswith('/api/v1/version/'):
                key = path.split('/')[-1]
                lm = get_lifecycle()
                ver = lm.get_version(key)
                changelog = lm.get_changelog(key)
                self._send_json({"product": key, "version": ver, "changelog": changelog})

            elif path == '/api/v1/prd':
                prd = get_prd()
                self._send_json(prd.summary())

            elif path == '/api/v1/prd/list':
                prd = get_prd()
                self._send_json(prd.list_all())

            # ======== 硅胶体记忆路由 ========
            elif path == '/api/v1/memory':
                """GET: 查询记忆 /api/v1/memory?q=关键字&dept=all&k=3"""
                mem = _reg_memory()
                if not mem:
                    self._send_json({"error": "记忆系统未初始化"}, 503)
                    return
                query = params.get('q', [''])[0]
                dept = params.get('dept', ['all'])[0]
                k = int(params.get('k', ['3'])[0])
                if dept == 'all':
                    results = mem.recall(query, k)
                else:
                    # 按部门过滤
                    results = mem.recall(query, k * 3)
                    results['episodic'] = [e for e in results['episodic'] if dept in e.get('tags', [])][:k]
                    results['semantic'] = [s for s in results['semantic'] if dept in str(s)][:k]
                self._send_json({"query": query, "department": dept, "results": results})

            elif path == '/api/v1/memory/episodic':
                """GET: 查询情节记忆"""
                mem = _reg_memory()
                if not mem:
                    self._send_json({"error": "记忆系统未初始化"}, 503)
                    return
                query = params.get('q', [''])[0]
                results = mem.episodic.search(query, int(params.get('k', ['5'])[0]))
                self._send_json({"query": query, "count": len(results), "results": results})

            elif path == '/api/v1/memory/semantic':
                """GET: 查询语义知识图谱"""
                mem = _reg_memory()
                if not mem:
                    self._send_json({"error": "记忆系统未初始化"}, 503)
                    return
                entity = params.get('entity', [''])[0]
                results = mem.semantic.query(entity, limit=int(params.get('limit', ['10'])[0]))
                self._send_json({"entity": entity, "count": len(results), "results": results})

            elif path == '/api/v1/memory/skills':
                """GET: 查询程序记忆(最佳实践)"""
                mem = _reg_memory()
                if not mem:
                    self._send_json({"error": "记忆系统未初始化"}, 503)
                    return
                context = params.get('context', [''])[0]
                results = mem.procedural.match(context)
                self._send_json({"context": context, "count": len(results), "results": results})

            # ======== 全部门 API ========
            elif path == '/api/v1/dept':
                """GET: 查询所有部门注册表"""
                self._send_json({
                    "department_count": len(DEPARTMENT_REGISTRY),
                    "departments": DEPARTMENT_REGISTRY
                })

            elif path.startswith('/api/v1/dept/'):
                """GET: 查询特定部门信息"""
                dept_key = path.split('/')[-1]
                info = DEPARTMENT_REGISTRY.get(dept_key)
                if info:
                    self._send_json(info)
                else:
                    self._send_json({"error": f"部门 '{dept_key}' 未找到"}, 404)

            # ======== 记忆融合路由 ========
            elif path == '/api/v1/memory/consolidate':
                """POST: 融合多源记忆为统一结果"""
                mem = _reg_memory()
                if not mem:
                    self._send_json({"error": "记忆系统未初始化"}, 503)
                    return
                sources = body.get('sources', ['episodic', 'semantic', 'procedural'])
                query = body.get('query', '')
                result = mem.consolidate(sources, query)
                self._send_json({"consolidated": result})

            elif path == '/api/v1/memory/fusion':
                """POST: 记忆融合 — 合并相似记忆去重"""
                mem = _reg_memory()
                if not mem:
                    self._send_json({"error": "记忆系统未初始化"}, 503)
                    return
                threshold = float(body.get('threshold', 0.7))
                result = mem.fusion(threshold)
                self._send_json({"fused_count": len(result), "merged": result})

            elif path == '/api/v1/memory/hot':
                """GET: 获取热记忆 — 近期高频访问"""
                mem = _reg_memory()
                if not mem:
                    self._send_json({"error": "记忆系统未初始化"}, 503)
                    return
                hours = int(body.get('hours', 24))
                result = mem.hot_memories(hours)
                self._send_json({"hot_count": len(result), "memories": result})

            elif path == '/api/v1/memory/timeline':
                """GET: 获取记忆时间线 — 按时间排序"""
                mem = _reg_memory()
                if not mem:
                    self._send_json({"error": "记忆系统未初始化"}, 503)
                    return
                limit = int(body.get('limit', 20))
                result = mem.timeline(limit)
                self._send_json({"timeline_count": len(result), "entries": result})

            else:
                self._send_json({"error": "Not found", "path": path}, 404)

        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    # ======== POST ========

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')

        try:
            body = self._read_body()

            if path == '/api/v1/lifecycle/upgrade':
                lm = get_lifecycle()
                key = body.get('key', '')
                stage = body.get('stage', '')
                result = lm.upgrade_stage(key, stage)
                if 'error' in result:
                    self._send_json(result, 400)
                else:
                    self._send_json(result)

            elif path == '/api/v1/lifecycle/version':
                lm = get_lifecycle()
                key = body.get('key', '')
                version = body.get('version', '')
                result = lm.set_version(key, version)
                if 'error' in result:
                    self._send_json(result, 400)
                else:
                    self._send_json(result)

            elif path == '/api/v1/prd/submit':
                prd = get_prd()
                result = prd.submit(
                    department=body.get('department', 'rd'),
                    product=body.get('product', ''),
                    title=body.get('title', ''),
                    priority=body.get('priority', 'normal'),
                    description=body.get('description', ''),
                )
                self._send_json(result)

            # ======== 硅胶体记忆写入 ========
            elif path == '/api/v1/memory':
                """POST: 写入记忆(任何部门/任何人都可调用)"""
                mem = _reg_memory()
                if not mem:
                    self._send_json({"error": "记忆系统未初始化"}, 503)
                    return
                context_type = body.get('type', 'general')
                payload = body.get('payload', {})
                tags = body.get('tags', [])
                dept = body.get('dept', 'rd')  # 来自哪个部门
                tags.append(f'dept:{dept}')
                eid = mem.remember(context_type, payload, tags)
                self._send_json({"status": "remembered", "id": eid, "department": dept})

            elif path == '/api/v1/memory/skill':
                """POST: 添加最佳实践"""
                mem = _reg_memory()
                if not mem:
                    self._send_json({"error": "记忆系统未初始化"}, 503)
                    return
                mem.procedural.add_skill(
                    name=body.get('name', ''),
                    pattern=body.get('pattern', ''),
                    instruction=body.get('instruction', ''),
                    category=body.get('category', 'general'),
                    confidence=float(body.get('confidence', 0.5)),
                )
                self._send_json({"status": "skill_added", "name": body.get('name', '')})

            elif path == '/api/v1/memory/entity':
                """POST: 添加知识图谱实体"""
                mem = _reg_memory()
                if not mem:
                    self._send_json({"error": "记忆系统未初始化"}, 503)
                    return
                eid = mem.semantic.add_entity(
                    name=body.get('name', ''),
                    entity_type=body.get('type', 'unknown'),
                    properties=body.get('properties', {}),
                )
                self._send_json({"status": "entity_added", "id": eid})

            # ======== 跨部门消息通道 ========
            elif path == '/api/v1/notify':
                """POST: 部门间通知(自动记录到记忆)"""
                mem = _reg_memory()
                dept_from = body.get('from_dept', 'rd')
                dept_to = body.get('to_dept', 'all')
                message = body.get('message', '')
                urgency = body.get('urgency', 'normal')
                if mem:
                    eid = mem.remember('notification', {
                        'from': dept_from, 'to': dept_to,
                        'message': message, 'urgency': urgency
                    }, [f'dept:{dept_from}', f'to:{dept_to}', 'notification'])
                    self._send_json({"status": "notified", "id": eid, "from": dept_from, "to": dept_to})
                else:
                    self._send_json({"status": "notified_no_memory", "note": "记忆系统未初始化,通知仅日志记录"})

            elif path == '/api/v1/review':
                filepath = body.get('file', '')
                if not filepath or not os.path.exists(filepath):
                    self._send_json({"error": "File not found"}, 400)
                else:
                    review_fn = get_review()
                    result = review_fn(filepath)
                    self._send_json(result)

            elif path == '/api/v1/lifecycle/record':
                lm = get_lifecycle()
                lm.record_call(
                    key=body.get('product', ''),
                    latency_ms=float(body.get('latency_ms', 0)),
                    success=bool(body.get('success', True)),
                    error=body.get('error', ''),
                )
                self._send_json({"recorded": True})

            else:
                self._send_json({"error": "Not found", "path": path}, 404)

        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def log_message(self, format, *args):
        sys.stderr.write(f"[IGP API] {args[0]} {args[1]} {args[2]}\n")


def start_server(host: str = 'localhost', port: int = 8080):
    server = HTTPServer((host, port), IGPAPIHandler)
    print(f"IGP 研发部 API 服务: http://{host}:{port}")
    print(f"  GET  /api/v1/health")
    print(f"  GET  /api/v1/lifecycle")
    print(f"  GET  /api/v1/lifecycle/products?stage=beta")
    print(f"  GET  /api/v1/version/BugDoctor")
    print(f"  POST /api/v1/prd/submit")
    print(f"  POST /api/v1/review")
    print(f"\n按 Ctrl+C 停止")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器停止.")
        server.server_close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='IGP 研发部 HTTP API')
    parser.add_argument('--port', type=int, default=8080, help='端口')
    parser.add_argument('--host', type=str, default='localhost', help='主机')
    parser.add_argument('--test', action='store_true', help='测试模式(不启动服务器,只检查路由)')
    args = parser.parse_args()

    if args.test:
        print("API 测试模式 - 路由列表:")
        routes = [
            "GET  /api/v1/health",
            "GET  /api/v1/lifecycle",
            "GET  /api/v1/lifecycle/products",
            "GET  /api/v1/lifecycle/product/<key>",
            "GET  /api/v1/version/<key>",
            "POST /api/v1/lifecycle/upgrade",
            "POST /api/v1/lifecycle/version",
            "POST /api/v1/lifecycle/record",
            "POST /api/v1/prd/submit",
            "GET  /api/v1/prd",
            "GET  /api/v1/prd/list",
            "POST /api/v1/review",
            "",
            "--- 硅胶体记忆 (全员可用) ---",
            "GET  /api/v1/memory?q=<keyword>&dept=<dept>&k=<n>",
            "GET  /api/v1/memory/episodic?q=<keyword>",
            "GET  /api/v1/memory/semantic?entity=<name>",
            "GET  /api/v1/memory/skills?context=<text>",
            "POST /api/v1/memory  (body: type, payload, tags, dept)",
            "POST /api/v1/memory/skill  (body: name, pattern, instruction)",
            "POST /api/v1/memory/entity  (body: name, type, properties)",
            "POST /api/v1/notify  (body: from_dept, to_dept, message, urgency)",
            "",
            "--- 全员部门查询 ---",
            "GET  /api/v1/dept  (所有部门列表)",
            "GET  /api/v1/dept/<chromosome_key>",
            "",
            "--- 记忆融合路由 ---",
            "POST /api/v1/memory/consolidate  (融合多源记忆)",
            "POST /api/v1/memory/fusion  (记忆去重合并)",
            "GET  /api/v1/memory/hot?hours=24  (热记忆)",
            "GET  /api/v1/memory/timeline?limit=20  (记忆时间线)",
        ]
        for r in routes:
            print(f"  {r}")
        print("\n所有路由注册完成 ✅ (共22条)")
    else:
        start_server(args.host, args.port)
