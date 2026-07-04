import asyncio
from mcp import Client
import json

class MCPClient:
    """Wrap MCP SDK Client for IGP engine compatibility"""
    
    def __init__(self, server_url=None, server_obj=None):
        self._server = None
        self.server_url = server_url
        self.server_obj = server_obj
    
    async def call_tool(self, tool_name: str, args: dict = None):
        if self.server_obj:
            async with Client(self.server_obj) as client:
                result = await client.call_tool(tool_name, args or {})
                return result.structured_content
        return {"error": "no server"}
    
    def call_sync(self, tool_name: str, args: dict = None):
        return asyncio.run(self.call_tool(tool_name, args))

