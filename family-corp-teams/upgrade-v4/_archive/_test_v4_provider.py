# _test_v4_provider.py
# 测试IGP Provider Router功能

import unittest
from igp_provider_router import ProviderRouter, Provider

class TestProviderRouter(unittest.TestCase):
    def setUp(self):
        # 假设的提供者实例
        class DummyProvider(Provider):
            def chat(self, prompt: str, model: str) -> str:
                return f"Dummy response for {prompt} using {model}"

            def invoke(self, command: str, model: str) -> Any:
                return f"Dummy invocation result for {command} using {model}"

            def embed(self, text: str, model: str) -> List[float]:
                return [0.1, 0.2, 0.3]  # 假设的嵌入向量

        self.providers = {
            'qwen': DummyProvider(),
            'openai': DummyProvider(),
            'ollama': DummyProvider()
        }
        self.router = ProviderRouter(self.providers)

    def test_chat(self):
        self.assertEqual(self.router.chat("Hello, world!"), "Dummy response for Hello, world! using qwen")
        self.assertEqual(self.router.chat("Hello, world!", model="openai"), "Dummy response for Hello, world! using openai")

    def test_invoke(self):
        self.assertEqual(self.router.invoke("some_command"), "Dummy invocation result for some_command using qwen")
        self.assertEqual(self.router.invoke("some_command", model="ollama"), "Dummy invocation result for some_command using ollama")

    def test_embed(self):
        self.assertEqual(self.router.embed("Some text"), [0.1, 0.2, 0.3])
        self.assertEqual(self.router.embed("Some text", model="openai"), [0.1, 0.2, 0.3])

if __name__ == "__main__":
    unittest.main()