"""
IGP 研发部 V6 — PRD 需求管理系统
跨部门需求提交→三Agent评审→自动转GitHub搜索→吸收队列
"""
from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pathlib import Path


# 部门编码
DEPARTMENTS = {
    "mcp": "染色体1 MCP协议",
    "a2a": "染色体2 A2A协议",
    "market": "染色体3 市场",
    "router": "染色体4 路由",
    "guardian": "染色体5 安全",
    "commerce": "染色体6 商业",
    "agentos": "染色体7 AgentOS",
    "ap2": "染色体8 AP2",
    "bugdoctor": "染色体9 Bug修复",
    "logic": "染色体10 逻辑",
    "metrics": "染色体11 类型/度量",
    "tester": "染色体12 测试",
    "hr": "染色体13 HR",
    "routing": "染色体14 智能路由",
    "audit": "染色体15 审计安全",
    "rd": "研发部",
}


class PRDQueue:
    """PRD队列管理系统"""
    
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        os.makedirs(os.path.join(base_dir, 'prd', 'data'), exist_ok=True)
        self._queue_file = os.path.join(base_dir, 'prd', 'data', 'queue.json')
        self._queue = self._load()
    
    def _load(self) -> Dict:
        if os.path.exists(self._queue_file):
            try:
                with open(self._queue_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"pending": [], "reviewing": [], "searching": [], "done": [], "rejected": []}
    
    def _save(self):
        with open(self._queue_file, 'w', encoding='utf-8') as f:
            json.dump(self._queue, f, indent=2, ensure_ascii=False)
    
    def submit(self, department: str, product: str, title: str, priority: str = "normal", description: str = "") -> Dict:
        """提交一个新PRD"""
        prd = {
            "id": f"PRD-{datetime.now(timezone.utc).timestamp():.0f}-{len(self._queue['pending'])}",
            "department": department,
            "department_name": DEPARTMENTS.get(department, department),
            "product": product,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "pending",
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            "review_score": 0,
            "search_keywords": [],
        }
        self._queue["pending"].append(prd)
        self._save()
        return prd
    
    def list_pending(self) -> List[Dict]:
        return self._queue["pending"]
    
    def list_all(self) -> Dict:
        return self._queue
    
    def auto_search_keywords(self, prd: Dict) -> List[str]:
        """自动将PRD标题转化为GitHub搜索关键词"""
        title = prd["title"]
        product = prd["product"]
        # 简单关键词提取
        words = title.replace("的", " ").replace("了", " ").replace("和", " ").split()
        keywords = [w for w in words if len(w) > 1]
        return keywords[:5]
    
    def summary(self) -> Dict:
        return {
            "pending": len(self._queue["pending"]),
            "reviewing": len(self._queue["reviewing"]),
            "searching": len(self._queue["searching"]),
            "done": len(self._queue["done"]),
            "rejected": len(self._queue["rejected"]),
            "total": sum(len(v) for v in self._queue.values()),
        }


if __name__ == '__main__':
    base = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6'
    queue = PRDQueue(base)
    
    print("IGP PRD 需求队列")
    print("=" * 50)
    summary = queue.summary()
    print(f"待审批: {summary['pending']}")
    print(f"评审中: {summary['reviewing']}")
    print(f"搜索中: {summary['searching']}")
    print(f"已完成: {summary['done']}")
    print(f"已驳回: {summary['rejected']}")
    print(f"总计: {summary['total']}")
    
    print("\n可用部门:")
    for code, name in DEPARTMENTS.items():
        print(f"  {code:15} {name}")
    
    print("\n模拟提交PRD:")
    prd = queue.submit(
        department="market",
        product="BugDoctor",
        title="需要TypeScript文件检测支持",
        priority="high",
    )
    print(f"  PRD ID: {prd['id']}")
    print(f"  部门: {prd['department_name']}")
    print(f"  标题: {prd['title']}")
    print(f"  自动关键词: {queue.auto_search_keywords(prd)}")
