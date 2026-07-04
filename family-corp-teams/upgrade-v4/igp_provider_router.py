# 负责团队: ai-team3 + backend-team3
# 吸收来源: OpenCode AI SDK + Cline provider 设计
# 产出: IGP不再限于qwen，多个模型按需路由
# TODO: v4研发阶段实现

from abc import ABC, abstractmethod
import os
from typing import Dict, Any, List, Optional

# 假设的外部模型接口
class Provider(ABC):
    @abstractmethod
    def chat(self, prompt: str, model: str) -> str:
        pass

    @abstractmethod
    def invoke(self, command: str, model: str) -> Any:
        pass

    @abstractmethod
    def embed(self, text: str, model: str) -> List[float]:
        pass

class ProviderRouter:
    def __init__(self, providers: Dict[str, Provider]):
        self.providers = providers
        self.default_model = os.getenv('IGP_DEFAULT_MODEL', 'qwen')
        self.model_routes = {
            'simple': 'qwen',
            'chat': 'qwen',
            'complex': 'openai',
            'embedding': 'ollama'
        }

    def route(self, task: str) -> str:
        # 根据任务类型选择模型
        return self.model_routes.get(task, self.default_model)

    def chat(self, prompt: str, model: str = None) -> str:
        model = model or self.default_model
        provider = self.providers.get(model)
        if not provider:
            raise ValueError(f"Provider {model} not found")
        try:
            return provider.chat(prompt, model)
        except Exception as e:
            print(f"Error with provider {model}: {str(e)}")
            # 自动降级到默认模型
            return self.chat(prompt, self.default_model)

    def invoke(self, command: str, model: str = None) -> Any:
        model = model or self.default_model
        provider = self.providers.get(model)
        if not provider:
            raise ValueError(f"Provider {model} not found")
        try:
            return provider.invoke(command, model)
        except Exception as e:
            print(f"Error with provider {model}: {str(e)}")
            # 自动降级到默认模型
            return self.invoke(command, self.default_model)

    def embed(self, text: str, model: str = None) -> List[float]:
        model = model or self.default_model
        provider = self.providers.get(model)
        if not provider:
            raise ValueError(f"Provider {model} not found")
        try:
            return provider.embed(text, model)
        except Exception as e:
            print(f"Error with provider {model}: {str(e)}")
            # 自动降级到默认模型
            return self.embed(text, self.default_model)

# 示例用法
if __name__ == "__main__":
    # 假设的提供者实例
    class DummyProvider(Provider):
        def chat(self, prompt: str, model: str) -> str:
            return f"Dummy response for {prompt} using {model}"

        def invoke(self, command: str, model: str) -> Any:
            return f"Dummy invocation result for {command} using {model}"

        def embed(self, text: str, model: str) -> List[float]:
            return [0.1, 0.2, 0.3]  # 假设的嵌入向量

    providers = {
        'qwen': DummyProvider(),
        'openai': DummyProvider(),
        'ollama': DummyProvider()
    }

    router = ProviderRouter(providers)
    print(router.chat("Hello, world!"))
    print(router.invoke("some_command"))
    print(router.embed("Some text"))