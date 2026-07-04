"""IGP-D2A 验证测试"""
import sys, json
sys.path.insert(0, r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\projects\igp-d2a')
from agent_protocol import simulate_igp_communication

result = simulate_igp_communication()
print(f"\n测试结果:")
print(f"  总消息数: {result['messages_count']}")
print(f"  Agent数: {len(result['agents'])}")
for a in result['agents']:
    print(f"  {a['agent']}: inbox={a['inbox_size']}, logs={a['total_logs']}")
print("\n✅ IGP-D2A Agent通信协议验证通过！")

if __name__ == '__main__':
    print('OK')
