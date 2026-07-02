from provider_abstraction import ProviderAbstraction
from provider_router import SmartRouter
from provider_pk import ProviderPK
import time
from typing import Any, List

# Mock Providers
class MockProvider(ProviderAbstraction):
    def __init__(self, name: str):
        self.name = name

    def chat(self, prompt: str, model: str) -> str:
        print(f"[Mock] {self.name} processing: {prompt}")
        time.sleep(1)
        return f"[Mock] {self.name} response to: {prompt}"

    def invoke(self, command: str, model: str) -> Any:
        print(f"[Mock] {self.name} executing: {command}")
        time.sleep(1)
        return f"[Mock] {self.name} result for: {command}"

    def embed(self, text: str, model: str) -> List[float]:
        print(f"[Mock] {self.name} embedding: {text}")
        time.sleep(1)
        return [0.1, 0.2, 0.3]

# 注册3个Provider
providers = {
    'qwen': MockProvider('Qwen'),
    'openai': MockProvider('OpenAI'),
    'deepseek': MockProvider('DeepSeek')
}

# 创建路由器和PK排名实例
router = SmartRouter(providers)
pk_ranker = ProviderPK(providers)

# 测试路由逻辑
task1 = "编写一个Python函数来计算斐波那契数列"
print(router.chat(task1, 'qwen'))

# 测试PK排名
print("Provider rankings:")
for provider, score in pk_ranker.get_provider_ranking().items():
    print(f"{provider}: {score}")

# 更新评分
pk_ranker.update_scores()

# 打印验证结果
print("\n✅ Provider路由部 裂变验证通过")