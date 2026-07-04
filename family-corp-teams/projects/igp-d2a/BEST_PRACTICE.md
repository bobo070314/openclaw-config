# IGP-D2A Agent通信协议 — 最佳实践 v1

## 来源
- Google A2A Protocol (Linux Foundation, April 2025)
- MCP Python SDK v2 (2026-07-28 spec)
- IGP 内部研发闭环 2026-07-01

## 核心理念
Digest → Act: Agent 之间不直接调用 function，而是通过标准消息通信
每个Agent是独立的"节点"，接收消息、处理、回复

## 消息格式
{
    "id": "a1b2c3d4",
    "ts": "2026-07-01T09:30:00",
    "from": "quality-team1",
    "to": "infra-team2",
    "action": "request/response/report/alert",
    "data": {"check": "something"}
}

## 通信模式
1. request → response (同步)
2. report (单向汇报)
3. alert (紧急广播)

## 落地
- 模块: family-corp-teams/projects/igp-d2a/agent_protocol.py
- 消化方: IGP infra-team2 (替代旧igp_a2a_bridge.py)
- 淘汰方: igp_a2a_bridge.py (空文件, 5分)
