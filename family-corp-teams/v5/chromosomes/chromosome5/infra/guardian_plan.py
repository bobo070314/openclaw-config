'''
Guardian Plan Module - Read-only Analysis
风险分析引擎：识别操作的风险等级
'''

import os
import re
from typing import Dict, Any, List, Optional


class GuardianPlan:
    """Plan阶段：只读分析，不执行任何修改"""

    RISK_LEVELS = ['read-only', 'safe', 'dangerous', 'critical']

    def __init__(self):
        self.request = None
        self._actions = []
        self.report = {}

    def receive_request(self, request: Dict[str, Any]) -> None:
        """接收操作请求"""
        self.request = request
        self._actions.append(request)
        self.report = {}

    def analyze_risk(self) -> str:
        """分析风险等级"""
        if not self.request:
            return 'read-only'

        action = self.request.get('action', '').lower()
        file_path = self.request.get('file_path', '')
        command = self.request.get('command', '')

        # Critical: 删除/覆盖/格式化/系统级操作
        if action in ('delete', 'rm', 'format', 'dd', 'shutdown'):
            return 'critical'
        if 'rm -rf' in command or 'del /f' in command:
            return 'critical'

        # Dangerous: 修改系统文件/执行危险命令
        if action in ('write', 'edit', 'modify', 'chmod', 'mv'):
            dangerous_patterns = [
                r'system32', r'/etc/', r'/boot/',
                r'passwd', r'shadow', r'sudoers',
            ]
            for p in dangerous_patterns:
                if re.search(p, file_path, re.IGNORECASE):
                    return 'critical'
            return 'dangerous'

        # Safe: 读操作
        if action in ('read', 'list', 'search', 'query'):
            return 'safe'

        return 'read-only'

    def generate_report(self) -> Dict[str, Any]:
        """生成Plan报告"""
        risk = self.analyze_risk()
        self.report = {
            'request': self.request,
            'risk_level': risk,
            'status': 'blocked' if risk == 'critical' else 'pending_approval',
            'verdict': 'DENIED' if risk == 'critical' else 'REQUIRES_APPROVAL' if risk == 'dangerous' else 'AUTO_APPROVED',
        }
        return self.report

    def get_actions(self) -> List[Dict]:
        """获取已记录的操作请求"""
        return self._actions

    def execute(self) -> None:
        """不执行任何修改"""
        pass
