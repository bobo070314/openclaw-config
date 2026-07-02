import json
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

@dataclass
class AgentDiscoveryService:
    """Agent发现服务实现"""
    registry: Dict[str, AgentCard] = None

    def __post_init__(self):
        self.registry = {}

    def register(self, agent_card: AgentCard):
        """注册Agent Card"""
        self.registry[agent_card.id] = agent_card

    def find_by_capability(self, capability: str, value: Any) -> List[AgentCard]:
        """根据能力查找Agent"""
        return [
            card for card in self.registry.values()
            if capability in card.capabilities and card.capabilities[capability] == value
        ]

    def broadcast(self, message: str, exclude_ids: List[str] = None):
        """广播消息到所有Agent"""
        for agent_id, agent_card in self.registry.items():
            if exclude_ids and agent_id in exclude_ids:
                continue
            # 实际实现中会调用agent_card.endpoints['discovery']发送消息
            print(f"Broadcasting to {agent_card.name} ({agent_id}): {message}")

    def get_all_agents(self) -> List[AgentCard]:
        """获取所有注册的Agent"""
        return list(self.registry.values())

    def save_registry(self, path: str):
        """保存注册表到文件"""
        with open(path, 'w') as f:
            json.dump({agent_id: card.to_dict() for agent_id, card in self.registry.items()}, f, indent=2)

    def load_registry(self, path: str) -> 'AgentDiscoveryService':
        """从文件加载注册表"""
        with open(path, 'r') as f:
            data = json.load(f)
        self.registry = {agent_id: AgentCard.from_dict(card_data) for agent_id, card_data in data.items()}
        return self