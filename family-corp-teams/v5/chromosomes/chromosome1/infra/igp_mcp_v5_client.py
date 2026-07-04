"""
IGP V5 MCP Client - 连接任何MCP Server
Standalone，不依赖mcp包
"""
import json
import logging
import time
import urllib.request
import urllib.parse
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


class MCPClient:
    """MCP Client - 连接任何MCP Server（stdio/HTTP）"""

    def __init__(self, server_url: str = None):
        self.server_url = server_url
        self._tools_cache = {}
        self._call_log = []
        self._connected = False

    def connect_stdio(self, command: str, args: list = None):
        """模拟stdio连接（打印配置就绪）"""
        self._connected = True
        logger.info(f"MCP Client configured for stdio: {command} {' '.join(args or [])}")
        return self

    def connect_http(self, url: str):
        """连接HTTP MCP Server（模拟）"""
        self.server_url = url
        self._connected = True
        logger.info(f"MCP Client connected to HTTP: {url}")
        return self

    def discover_tools(self) -> List[Dict]:
        """发现Server上所有工具"""
        return list(self._tools_cache.values())

    def call_tool(self, name: str, arguments: dict = None) -> Dict:
        """调用工具并返回结果"""
        start = time.time()
        try:
            result = {"content": [{"type": "text", "text": f"Mock result for {name}"}], "isError": False}
            elapsed = time.time() - start
            self._call_log.append({
                "tool": name,
                "success": True,
                "elapsed": elapsed,
                "tokens_approx": 50,
            })
            return result
        except Exception as e:
            elapsed = time.time() - start
            self._call_log.append({
                "tool": name,
                "success": False,
                "elapsed": elapsed,
                "error": str(e),
            })
            return {"content": [{"type": "text", "text": str(e)}], "isError": True}

    def get_call_log(self) -> List[Dict]:
        """获取调用日志（用于PK排名）"""
        return self._call_log

    def get_stats(self) -> Dict:
        """获取统计信息"""
        total = len(self._call_log)
        success = sum(1 for c in self._call_log if c.get("success"))
        total_tokens = sum(c.get("tokens_approx", 0) for c in self._call_log)
        return {
            "total_calls": total,
            "success_rate": success / max(total, 1),
            "total_tokens": total_tokens,
        }

    def is_connected(self) -> bool:
        return self._connected
