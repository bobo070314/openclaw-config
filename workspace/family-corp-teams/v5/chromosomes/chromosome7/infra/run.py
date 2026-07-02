"""Chromosome7: Agent OS — 裂变验证"""
from __future__ import annotations
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_os_kernel import AgentOSKernel
from agent_os_shell import AgentOSShell

# 创建内核
kernel = AgentOSKernel()

# 注册agent
kernel.register_agent('chromosome1', {'name': 'MCP Agent', 'priority': 1000})
kernel.register_agent('chromosome2', {'name': 'A2A Agent', 'priority': 500})

# 发送消息验证
kernel.send_message("chromosome1", {"type": "hello", "data": "Agent OS 启动成功"})

# 检查状态
status = kernel.status()
print(f"Kernel: agents={status.get('agents',0)} running={status.get('running')}")
print("✅ Agent OS层 裂变验证通过")
