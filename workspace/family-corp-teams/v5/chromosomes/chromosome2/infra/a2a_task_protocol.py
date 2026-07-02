import json
from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class TaskMessage:
    """A2A任务协议消息结构"""
    message_id: str  # 消息唯一ID
    timestamp: str  # ISO8601时间戳
    sender: str  # 发送方 (department:team)
    receiver: str  # 接收方 (department:team)
    action: str  # 操作类型 (task/send, task/sendSubscribe)
    payload: Dict[str, Any]  # 有效载荷
    correlation_id: str = None  # 关联ID

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'message_id': self.message_id,
            'timestamp': self.timestamp,
            'sender': self.sender,
            'receiver': self.receiver,
            'action': self.action,
            'payload': self.payload,
            'correlation_id': self.correlation_id
        }

    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'TaskMessage':
        """从JSON字符串解析"""
        data = json.loads(json_str)
        return cls(**data)

    def is_streaming(self) -> bool:
        """判断是否为流式消息"""
        return self.action == 'task/sendSubscribe'

# JSON-RPC 2.0 兼容方法
def json_rpc_request(method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    return {
        'jsonrpc': '2.0',
        'method': method,
        'params': params or {},
        'id': str(uuid.uuid4())[:8]
    }

def json_rpc_response(result: Any, request_id: str) -> Dict[str, Any]:
    return {
        'jsonrpc': '2.0',
        'result': result,
        'id': request_id
    }

def json_rpc_error(code: int, message: str, request_id: str) -> Dict[str, Any]:
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': code,
            'message': message
        },
        'id': request_id
    }