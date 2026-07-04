import os
import json
import datetime
from pathlib import Path
from unified_engine import UnifiedIGPEngine

# 配置
TEST_DIR = Path(r"D:\bobo\openclaw-foreign\workspace\family-corp-teams\upgrade-v3")

# 初始化引擎
unified_engine = UnifiedIGPEngine()

# 1. 心跳检查
def test_heartbeat():
    print("\n[1/3] 数字生命体心跳检查...")
    result = unified_engine.run_heartbeat_check()
    print(f"    状态: {result['status']} at {result['last_heartbeat']}")
    return result

# 2. 派发工单
def test_ticket_dispatch():
    print("\n[2/3] 派发工单到 quality 部门...")
    ticket_id = unified_engine.execute_task("执行质量检查", "quality")
    print(f"    工单ID: {ticket_id}")
    return ticket_id

# 3. 运行PK
def test_pk_run(ticket_id):
    print("\n[3/3] 运行PK...")
    pk_result = unified_engine.pk_manager.run_pk("quality", "执行质量检查", verbose=True)
    print(f"    胜者: {pk_result['winner']}")
    print(f"    败者: {pk_result['loser']}")
    print(f"    得分: {pk_result['scores']}")
    return pk_result

# 执行测试
def run_test():
    print("="*70)
    print("  IGP 统一引擎验证测试")
    print("="*70)

    # 1. 心跳检查
    heartbeat_result = test_heartbeat()

    # 2. 派发工单
    ticket_id = test_ticket_dispatch()

    # 3. 运行PK
    pk_result = test_pk_run(ticket_id)

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
        "heartbeat": heartbeat_result,
        "ticket_id": ticket_id,
        "pk_result": pk_result
    }

if __name__ == "__main__":
    result = run_test()
    print("\n" + "="*70)
    print("  测试完成 | 等待老板指令")
    print("="*70)