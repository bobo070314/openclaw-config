"""
DocMind v5 — LLM接入版
把每一个分支从"正则匹配"进化到"真正理解语义"
用硅基流动免费 Qwen2.5-72B 驱动
"""
import os, json, re
from datetime import datetime
from openai import OpenAI

FAMILY = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams'
DOCMIND_DIR = os.path.join(FAMILY, 'projects', 'igp-docmind')

# 从openclaw.json读硅基流动的API Key
cfg_path = r'D:\bobo\openclaw-foreign\openclaw.json'
cfg = json.load(open(cfg_path, encoding='utf-8'))

providers = cfg.get('models', {}).get('providers', {})
silicon_key = ''
if 'siliconflow' in providers:
    silicon_info = providers['siliconflow']
    if isinstance(silicon_info, dict):
        silicon_key = silicon_info.get('apiKey', '') or silicon_info.get('apikey', '') or ''
    elif isinstance(silicon_info, list):
        for item in silicon_info:
            if isinstance(item, dict):
                silicon_key = item.get('apiKey', '') or silicon_key

# fallback: 通用的provider配置结构
api_key = silicon_key
base_url = "https://api.siliconflow.cn/v1"
model = "Qwen/Qwen2.5-72B-Instruct"

print(f'[DocMind v5] API: siliconflow | Model: {model}')
print(f'[DocMind v5] Key: {api_key[:8]}...{api_key[-4:]}')
print()


class LLMBranch:
    """LLM驱动分支 — 每个分支用不同prompt理解文档"""
    
    def __init__(self, name, system_prompt, api_key, base_url, model):
        self.name = name
        self.system_prompt = system_prompt
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
    
    def analyze(self, text):
        """用LLM理解一段文档"""
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"分析这段文档:\n\n{text[:2000]}"}
                ],
                max_tokens=200,
                temperature=0.3,
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f'[LLM Error: {str(e)[:60]}]'


# 测试文档
test_doc = '''# 2026-Q2 风险管理报告

Author: Risk Committee | Date: 2026-07-01

## 市场风险概览

全球市场波动率指数(VIX)从Q1的18.5上升至Q2的24.3，增长31.4%。
主要风险因素包括美联储利率决议和欧洲主权债务利差扩大至180bp。

## 组合风险敞口

| 固收 | 权益 | 大宗商品 | 外汇 |
|------|------|---------|------|
| 42.5M | 38.2M | 18.0M | 12.3M |

夏普比率0.85，低于目标值1.2。建议降低权益占比5%。'''


# 定义5个不同方向的Prompt分支
branches_config = [
    ('金融风险', '你是一个顶级金融风控分析师。分析文档中的风险信号、数字趋势和建议。回答要简短精确，突出关键风险指标。'),
    ('技术审计', '你是一个代码审计专家。分析文档的技术架构、依赖关系和潜在bug。关注安全性、可维护性和性能。'),
    ('知识图谱', '你是一个知识图谱工程师。从文档中提取实体和关系，输出格式为: 实体1 --[关系]--> 实体2。每个一行。'),
    ('DNA视角', '你是一个遗传学研究员。把文档当作DNA序列分析——找模式、突变、进化关系。从生物学视角解释文档内容。'),
    ('投资视角', '你是一个对冲基金经理。把文档内容当投资决策依据，给出买入/卖出/持有建议和置信度。'),
]

# 跑一遍看看效果
print('= ' * 35)
print('  DocMind v5 — LLM接入 5分支同时分析')
print(f'  模型: Qwen2.5-72B (硅基流动免费)')
print('= ' * 35)
print()

branches = []
for name, prompt in branches_config:
    branch = LLMBranch(name, prompt, api_key, base_url, model)
    branches.append(branch)

for branch in branches:
    print(f'🌿 {branch.name}:')
    result = branch.analyze(test_doc)
    # 缩进显示
    for line in result.split('\n'):
        print(f'  {line}')
    print()

# 全部5分支的分析写一份报告
print('- ' * 30)
print(f'✅ DocMind v5 5分支接入LLM完成')
print(f'  时间: {datetime.now().strftime("%H:%M:%S")}')
print(f'  下一步: 把v4的4大引擎 + DNA + 金融 + LLM融合成终极框架')
print('- ' * 30)

if __name__ == '__main__':
    print('OK')
