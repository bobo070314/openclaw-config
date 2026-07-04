# _test_v4_mcp.py
# 测试MCP客户端功能

import unittest
from igp_mcp_client import MCPClient

class TestMCPClient(unittest.TestCase):
    def setUp(self):
        self.client = MCPClient(host='localhost', port=5000)
        self.client.connect()

    def tearDown(self):
        self.client.close()

    def test_connect(self):
        self.assertTrue(self.client.connected)

    def test_call_tool(self):
        def callback(response):
            self.assertIn('result', response)

        self.client.call_tool('example_tool', {'param': 'value'}, callback)

    def test_get_resource(self):
        def callback(response):
            self.assertIn('content', response)

        self.client.get_resource('example_resource', callback)

if __name__ == '__main__':
    unittest.main()