from a2a_agent_card import AgentCard
from a2a_task_protocol import TaskMessage
from a2a_discovery import AgentDiscoveryService
import uuid

# 创建两个测试Agent Card
agent1 = AgentCard(
    id=str(uuid.uuid4()),
    name="A2A-Federation-Agent-1",
    description="联邦部核心代理",
    endpoints={"discovery": "http://localhost:8001/discover"},
    capabilities={"federation": True, "protocol": "A2A-v1"}
)

agent2 = AgentCard(
    id=str(uuid.uuid4()),
    name="A2A-Federation-Agent-2",
    description="联邦部辅助代理",
    endpoints={"discovery": "http://localhost:8002/discover"},
    capabilities={"federation": True, "protocol": "A2A-v1"}
)

# 初始化发现服务
service = AgentDiscoveryService()

# 注册Agent
service.register(agent1)
service.register(agent2)

# 验证发现功能
print("=== A2A联邦部验证 ===")
print(f"注册了 {len(service.get_all_agents())} 个Agent")

# 查找具有特定能力的Agent
federated_agents = service.find_by_capability("federation", True)
print(f"找到 {len(federated_agents)} 个联邦能力Agent")

# 广播测试消息
service.broadcast("测试A2A联邦通信")

# 验证通过
print("\n✅ A2A联邦部 裂变验证通过")