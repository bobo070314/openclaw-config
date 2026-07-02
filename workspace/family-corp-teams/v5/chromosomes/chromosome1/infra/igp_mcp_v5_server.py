"""
IGP V5 MCP Server 导出器 - 把IGP Skills 导出为 MCP Server
Standalone，不依赖mcp包
"""
import json
import logging

logger = logging.getLogger(__name__)


class MCPServer:
    """MCP Server exporter for IGP Skills"""

    def __init__(self, skills_package: str = "default"):
        self.name = skills_package
        self.tools = {}
        self.resources = {}
        self.is_running = False
        logger.info(f"MCP Server '{self.name}' created")

    def register_tool(self, name: str, func, description: str, input_schema: dict = None):
        """注册一个工具到MCP Server"""
        self.tools[name] = {
            "name": name,
            "description": description,
            "input_schema": input_schema or {"type": "object", "properties": {}},
            "handler": func,
        }
        return self

    def register_resource(self, uri: str, data_getter, mime_type: str = "text/plain"):
        """注册一个资源"""
        self.resources[uri] = {
            "uri": uri,
            "mime_type": mime_type,
            "getter": data_getter,
        }
        return self

    def get_tool_list(self) -> list:
        """返回工具列表（符合MCP格式）"""
        return [
            {"name": n, "description": v["description"], "inputSchema": v["input_schema"]}
            for n, v in self.tools.items()
        ]

    def call_tool(self, name: str, arguments: dict = None):
        """调用工具"""
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")
        tool = self.tools[name]
        return tool["handler"](**(arguments or {}))

    def start(self):
        """模拟启动Server"""
        self.is_running = True
        logger.info(f"MCP Server '{self.name}' started with {len(self.tools)} tools")
        return {"status": "started", "name": self.name, "tools": len(self.tools)}

    def stop(self):
        self.is_running = False

    def tool_count(self) -> int:
        return len(self.tools)
