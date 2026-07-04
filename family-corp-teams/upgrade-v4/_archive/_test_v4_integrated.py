# 测试IGP v4集成功能

import unittest
from igp_provider_router import ProviderRouter, Provider
from igp_plan_act import PlanActManager
from igp_code_review import CodeReviewAgent

class TestIGPV4Integration(unittest.TestCase):
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
        self.plan_manager = PlanActManager()
        self.reviewer = CodeReviewAgent()

    def test_provider_routing(self):
        self.assertEqual(self.router.route('simple'), 'qwen')
        self.assertEqual(self.router.route('complex'), 'openai')
        self.assertEqual(self.router.route('embedding'), 'ollama')
        self.assertEqual(self.router.route('unknown'), 'qwen')

    def test_plan_act_flow(self):
        plan = self.plan_manager.generate_plan('update_file', 'example.txt')
        self.assertTrue(plan['approval_required'])
        self.assertTrue(self.plan_manager.approve_plan(plan['id']))
        self.assertTrue(self.plan_manager.execute_plan(plan['id']))
        self.assertTrue(self.plan_manager.create_checkpoint('example.txt'))
        self.assertTrue(self.plan_manager.rollback('checkpoint_12345'))

    def test_code_review_flow(self):
        pr_data = {'pr_id': 123, 'files': ['file1.py', 'file2.py']}
        review = self.reviewer.analyze_pr(pr_data)
        self.assertEqual(review['status'], 'pending')
        findings = self.reviewer.check_syntax('file1.py')
        self.assertEqual(findings, [])
        findings = self.reviewer.check_types('file1.py')
        self.assertEqual(findings, [])
        findings = self.reviewer.check_security('file1.py')
        self.assertEqual(findings, [])
        findings = self.reviewer.check_style('file1.py')
        self.assertEqual(findings, [])
        report = self.reviewer.generate_report(findings)
        self.assertEqual(report['status'], 'pass')

if __name__ == "__main__":
    unittest.main()