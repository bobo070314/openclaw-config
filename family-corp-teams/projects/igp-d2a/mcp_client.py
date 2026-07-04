"""
IGP-MCP Client
测试MCP JSON-RPC连接
"""
import os, json, sys

FAMILY = r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams"
PROTO_DIR = os.path.join(FAMILY, 'projects', 'igp-d2a')

sys.path.insert(0, PROTO_DIR)
from igp_mcp import IGPMCPProtocol

def main():
    protocol = IGPMCPProtocol()
    
    print('=== MCP标准接口测试 ===')
    print()
    
    methods = [
        'server/discover',
        'tools/list',
        'resources/list',
        'prompts/list',
        'igp/pk',
        'igp/broadcast',
        'igp/federate',
    ]
    
    for method in methods:
        params = {}
        if method == 'igp/federate':
            params = {'query': 'class'}
        if method == 'igp/broadcast':
            params = {'message': 'test'}
        
        result = protocol.handle_jsonrpc(method, params)
        method_display = method.replace('igp/', '').replace('/', '_')
        if 'error' in result:
            print(f'  ❌ {method}: {result["error"]}')
        else:
            keys = list(result.keys())[:3]
            val_preview = str({k: result[k] for k in keys})[:80]
            print(f'  ✅ {method:20s} | {val_preview}')

if __name__ == '__main__':
    main()
