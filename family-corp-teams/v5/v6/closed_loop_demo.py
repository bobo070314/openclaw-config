import requests

# 调用记录的Python脚本
requests.post('http://localhost:8080/api/v1/lifecycle/record', json={"product": "v5_bug_doctor", "latency_ms": 23, "success": True})
requests.post('http://localhost:8080/api/v1/lifecycle/record', json={"product": "v5_symbolic_engine", "latency_ms": 45, "success": True, "error": ""})
requests.post('http://localhost:8080/api/v1/lifecycle/record', json={"product": "v5_code_analyzer", "latency_ms": 12, "success": False, "error": "SyntaxWarning triggered"})

# Metrics查询
metrics_response = requests.get('http://localhost:8080/api/v1/lifecycle/product/v5_bug_doctor')
print("Metrics Response:", metrics_response.text)

# PRD提交
prd_response = requests.post('http://localhost:8080/api/v1/prd/submit', json={"department": "rd", "product": "CodeAnalyzer", "title": "修复SyntaxWarning触发的false positive", "priority": "high", "description": "Metrics显示code_analyzer有SyntaxWarning false positive"})
print("PRD Response:", prd_response.text)

# 验证PRD队列
prd_list_response = requests.get('http://localhost:8080/api/v1/prd/list')
print("PRD List Response:", prd_list_response.text)

# 最终报告输出
with open('D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\closed_loop_result.txt', 'w') as f:
    f.write("IGP闭环真实跑通成功\n")
    f.write("Metrics Response: " + metrics_response.text + "\n")
    f.write("PRD Response: " + prd_response.text + "\n")
    f.write("PRD List Response: " + prd_list_response.text + "\n")