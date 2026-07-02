#!/usr/bin/env python3
"""
IGP V5 商业协议部 v2 — 收入追踪 + PK排名
"""

import json, os, sys, time, math
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

now_iso = lambda: datetime.now(timezone.utc).isoformat()


class CommercePKRank:
    """商业PK排名引擎 v2"""
    
    def __init__(self):
        self.services = {}
        self.rank_history = []
    
    def register(self, agent_id: str, name: str = "") -> Dict:
        """注册一个商业服务"""
        svc = {
            "agent_id": agent_id,
            "name": name or agent_id,
            "revenue": 0.0,
            "tasks": 0,
            "costs": 0.0,
            "profit": 0.0,
            "margin": 0.0,
            "rating": 5.0,
            "review_count": 0,
            "registered_at": now_iso(),
        }
        self.services[agent_id] = svc
        return svc
    
    def record_transaction(self, agent_id: str, revenue: float, cost: float = 0, 
                           rating: float = 5.0) -> Dict:
        """记录一笔交易"""
        svc = self.services.get(agent_id)
        if not svc:
            svc = self.register(agent_id)
        
        svc["revenue"] += revenue
        svc["costs"] += cost
        svc["tasks"] += 1
        svc["profit"] = svc["revenue"] - svc["costs"]
        svc["margin"] = svc["profit"] / max(svc["revenue"], 0.001) * 100
        svc["rating"] = (svc["rating"] * svc["review_count"] + rating) / (svc["review_count"] + 1)
        svc["review_count"] += 1
        
        return svc
    
    def get_ranking(self) -> List[Dict]:
        """获取排名（按综合得分）"""
        ranked = []
        for aid, svc in self.services.items():
            # 评分公式: 利润率*30 + 收入*权重 + 评分*20 - 任务数系数调整
            revenue_score = min(math.log2(svc["revenue"] * 10 + 1), 30) if svc["revenue"] > 0 else 0
            profit_score = svc["margin"] * 0.3
            rating_score = svc["rating"] * 2
            task_score = min(svc["tasks"] * 0.5, 10)
            
            total_score = revenue_score + profit_score + rating_score + task_score
            
            ranked.append({
                "agent_id": aid,
                "name": svc["name"],
                "score": round(total_score, 1),
                "revenue": round(svc["revenue"], 2),
                "profit": round(svc["profit"], 2),
                "margin": round(svc["margin"], 1),
                "rating": round(svc["rating"], 1),
                "tasks": svc["tasks"],
            })
        
        ranked.sort(key=lambda x: x["score"], reverse=True)
        
        # Assign ranks and grades
        for i, r in enumerate(ranked):
            r["rank"] = i + 1
            r["grade"] = "S" if r["score"] >= 80 else "A" if r["score"] >= 60 else "B" if r["score"] >= 40 else "C" if r["score"] >= 20 else "D"
            # 淘汰判定
            r["eliminated"] = r["score"] < 10 and r["tasks"] >= 3
        
        return ranked
    
    def eliminate(self, min_score: float = 10) -> List[str]:
        """淘汰低分服务"""
        eliminated = []
        ranking = self.get_ranking()
        for r in ranking:
            if r["eliminated"] and r["score"] < min_score:
                del self.services[r["agent_id"]]
                eliminated.append(r["agent_id"])
        return eliminated
    
    def score_summary(self) -> Dict:
        """生成评分摘要"""
        ranking = self.get_ranking()
        return {
            "total_services": len(self.services),
            "total_revenue": sum(s["revenue"] for s in self.services.values()),
            "total_profit": sum(s["profit"] for s in self.services.values()),
            "ranking": ranking,
            "eliminations": self.eliminate(),
        }
