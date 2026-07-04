'''
IGP 统一引擎 v3.0
整合v1 KPI系统 + v3真实LLM Agent能力
'''
import os
import sys
import json
import datetime
import time
import random
import re
import subprocess
from pathlib import Path
import threading
from typing import Dict, List, Tuple, Optional

# 添加上层目录到path（igp_engine.py 在那个目录）
V3_DIR = Path(__file__).parent
PARENT_DIR = V3_DIR.parent
sys.path.insert(0, str(PARENT_DIR))
sys.path.insert(0, str(V3_DIR))

# 从v1引擎导入核心机制
from igp_engine import (
    create_ticket, dispatch_ticket, run_pk, fast_review,
    check_elimination, trigger_regeneration, update_kpi, monthly_kpi_report,
    scan_external_tools, trigger_absorption, headquarters_report,
    load_evolution_data, save_evolution_data, goal_create_tool, goal_update_tool, goal_get_tool, has_active_goal, boss_progress_summary, boss_speak, boss_mark_complete, boss_mark_blocked
)

# 从v3组件导入新能力
from igp_mcp_bridge import IGP_MCP
from igp_llm_agent import IGPAgent, PKManager
from v3_engine import V3Engine

# 常量定义
BASE_DIR = Path(r"D:\bobo\openclaw-foreign\workspace")
TEAMS_DIR = BASE_DIR / "family-corp-teams"
HEADQUARTERS_DIR = TEAMS_DIR / "headquarters"

# 通用配置
OPENCLAW_DASHSCOPE_KEY = os.environ.get("OPENCLAW_DASHSCOPE_KEY")
DASHSCOPE_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen-plus"

# 模块初始化
mcp = IGP_MCP()
engine_v3 = V3Engine()

# 数字生命体心跳
class DigitalLife:
    def __init__(self, name: str):
        self.name = name
        self.last_heartbeat = datetime.datetime.now()
        self.status = "active"

    def _heartbeat(self):
        self.last_heartbeat = datetime.datetime.now()
        self.status = "active"
        print(f"[Heartbeat] {self.name} is alive at {self.last_heartbeat}")

    def get_status(self):
        return {
            "name": self.name,
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "status": self.status
        }

# 整合后的引擎类
class UnifiedIGPEngine:
    def __init__(self):
        self.digital_life = DigitalLife("IGP Engine")
        self.mcp = IGP_MCP()
        self.v3_engine = V3Engine()
        self.pk_manager = PKManager()
        self.agents = {}
        self._init_agents()

    def _init_agents(self):
        """初始化所有部门的LLM Agent"""
        depts = [
            "frontend", "backend", "infrastructure", "ai",
            "mobile", "design", "quality", "pmo",
            "growth", "compliance", "advertising-anime", "ecommerce-marketing"
        ]
        for dept in depts:
            for tn in [1, 2, 3]:
                agent = IGPAgent(dept, tn)
                self.agents[f"{dept}-team{tn}"] = agent
        print(f"  ✅ 已加载 {len(self.agents)} 个LLM Agent")

    def run_full_cycle(self, task: str, department: str) -> dict:
        """运行完整的IGP进化周期"""
        print(f"\n{'='*60}")
        print(f"  IGP 统一引擎执行周期")
        print(f"  任务: {task}")
        print(f"  部门: {department}")
        print(f"{'='*60}")

        # 1. 创建工单
        ticket_id = create_ticket("IGP Engine", task, department)
        dispatch_ticket(ticket_id)

        # 2. 运行PK（使用真实LLM Agent）
        pk_result = self.pk_manager.run_pk(department, task, verbose=False)

        # 3. 更新KPI
        winner_team = pk_result.get("winner")
        loser_team = pk_result.get("loser")
        
        # 4. 更新v1的KPI系统
        update_kpi(department, winner_team, pk_result['scores'][0][1], loser_team)

        # 5. 记录进化数据
        data = load_evolution_data()
        round_entry = {
            "round_id": len(data['rounds']) + 1,
            "ticket_id": ticket_id,
            "department": department,
            "submitted": datetime.datetime.now().isoformat(),
            "solutions": [],
            "winner": winner_team,
            "loser": loser_team,
            "winner_score": pk_result['scores'][0][1],
            "loser_score": pk_result['scores'][-1][1],
        }
        data['rounds'].append(round_entry)
        save_evolution_data(data)

        # 6. 返回结果
        return {
            "ticket_id": ticket_id,
            "department": department,
            "winner": winner_team,
            "loser": loser_team,
            "scores": pk_result['scores'],
            "status": "completed"
        }

    def execute_task(self, task: str, department: str) -> dict:
        """执行单个任务"""
        print(f"\n{'='*60}")
        print(f"  IGP 统一引擎执行任务")
        print(f"  任务: {task}")
        print(f"  部门: {department}")
        print(f"{'='*60}")

        # 1. 创建工单
        ticket_id = create_ticket("IGP Engine", task, department)
        dispatch_ticket(ticket_id)

        # 2. 执行PK
        pk_result = self.pk_manager.run_pk(department, task, verbose=False)

        # 3. 更新KPI
        winner_team = pk_result.get("winner")
        loser_team = pk_result.get("loser")
        update_kpi(department, winner_team, pk_result['scores'][0][1], loser_team)

        # 4. 返回结果
        return {
            "ticket_id": ticket_id,
            "department": department,
            "winner": winner_team,
            "loser": loser_team,
            "scores": pk_result['scores'],
            "status": "completed"
        }

    def run_heartbeat_check(self):
        """运行数字生命体心跳检查"""
        self.digital_life._heartbeat()
        return self.digital_life.get_status()

    def run_test(self):
        """运行验证测试"""
        print("\n{'='*60}")
        print("  IGP 统一引擎验证测试")
        print("{'='*60}")

        # 1. 心跳检查
        print("\n  [1/3] 数字生命体心跳...")
        heartbeat_result = self.run_heartbeat_check()
        print(f"    状态: {heartbeat_result['status']} at {heartbeat_result['last_heartbeat']}")

        # 2. 派发工单
        print("\n  [2/3] 派发工单到 quality 部门...")
        ticket_id = create_ticket("IGP Engine", "执行质量检查", "quality")
        dispatch_ticket(ticket_id)

        # 3. 运行PK
        print("\n  [3/3] 运行PK...")
        pk_result = self.pk_manager.run_pk("quality", "执行质量检查", verbose=True)

        # 4. 输出结果报告
        print(f"\n  {'='*60}")
        print(f"  验证结果报告")
        print(f"{'='*60}")
        print(f"  工单ID: {ticket_id}")
        print(f"  胜者: {pk_result['winner']}")
        print(f"  败者: {pk_result['loser']}")
        print(f"  得分: {pk_result['scores']}")
        print(f"{'='*60}")

        return {
            "ticket_id": ticket_id,
            "pk_result": pk_result
        }

# 实例化统一引擎
unified_engine = UnifiedIGPEngine()

# 主函数（用于测试）
if __name__ == "__main__":
    print("="*70)
    print("  IGP 统一引擎 v3.0 启动")
    print("="*70)

    # 运行验证测试
    unified_engine.run_test()

    print("\n" + "="*70)
    print("  测试完成 | 等待老板指令")
    print("="*70)