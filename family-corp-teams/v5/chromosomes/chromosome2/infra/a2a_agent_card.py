import json
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AgentCard:
    """Agent身份/能力/端点描述"""
    id: str  # 唯一标识符
    name: str  # 易读名称
    description: str  # 功能描述
    endpoints: Dict[str, str]  # 端点地址
    capabilities: Dict[str, Any]  # 能力清单

    def to_dict(self) -> dict:
        """JSON序列化"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'endpoints': self.endpoints,
            'capabilities': self.capabilities
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'AgentCard':
        """JSON反序列化"""
        return cls(**data)

    def save(self, path: str):
        """保存为.card.json文件"""
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: str) -> 'AgentCard':
        """从.card.json文件加载"""
        with open(path, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
