"""
IGP-MCP HTTP Server
兼容MCP JSON-RPC 2.0 over HTTP
直接用Python http.server, 0外部依赖
"""
import os, json
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

FAMILY = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams"
PROJECTS = os.path.join(FAMILY, 'projects')

# 导入协议引擎
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from igp_mcp import IGPMCPProtocol

protocol = IGPMCPProtocol()

class MCPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8') if length else '{}'
        
        try:
            req = json.loads(body)
        except:
            req = {}
        
        method = req.get('method', '')
        params = req.get('params', {})
        req_id = req.get('id', 1)
        
        result = protocol.handle_jsonrpc(method, params)
        
        response = {
            'jsonrpc': '2.0',
            'id': req_id,
            'result': result,
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('MCP-Protocol-Version', '2026-07-28')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            info = protocol.handle_jsonrpc('server/discover', {})
            self.wfile.write(json.dumps(info, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # 静默

def main():
    port = 28791
    server = HTTPServer(('0.0.0.0', port), MCPHandler)
    print(json.dumps({'status': 'running', 'port': port, 
                      'discover': f'http://localhost:{port}/',
                      'jsonrpc': f'POST http://localhost:{port}/'}))

if __name__ == '__main__':
    main()
