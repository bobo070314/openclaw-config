
import unittest
import sys
from pathlib import Path

# 添加正确的infra目录到sys.path
sys.path.insert(0, r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5')

class Testv5_job_engine(unittest.TestCase):
    def test_example_1(self):
        # 示例测试函数1
        self.assertTrue(True)

    def test_example_2(self):
        # 示例测试函数2
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
