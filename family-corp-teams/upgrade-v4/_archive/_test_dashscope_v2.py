#!/usr/bin/env python3
"""使用igp_llm_agent正确初始化并验证DashScope"""
import sys, os
sys.path.insert(0, r"D:\\bobo\\openclaw-foreign\\workspace\\family-corp-teams\\upgrade-v3")
from igp_llm_agent import IGPAgent
from igp_rag_index import RAGIndex

# 正确的初始化方式
rag = RAGIndex()
agent = IGPAgent(dept="test", team_num=0, rag_db=rag)
result = agent.chat("Say 'hello world' in exactly two words.")
print(f"DashScope Result: {result}")
print(f"Token usage: {agent.last_token_usage}")
