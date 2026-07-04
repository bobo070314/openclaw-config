"""
IGP 研发部 V6 — 生命周期管理器
管理产品的 Research→Alpha→Beta→GA→Deprecated→EOL 全生命周期
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# 生命周期阶段的合法转换路径
STAGE_TRANSITIONS = {
    "research": ["alpha", "deprecated"],
    "alpha": ["beta", "deprecated"],
    "beta": ["ga", "deprecated"],
    "ga": ["deprecated"],
    "deprecated": ["eol"],
    "eol": [],
}

STAGE_ORDER = {"research": 0, "alpha": 1, "beta": 2, "ga": 3, "deprecated": 4, "eol": 5}


class LifecycleManager:
    """生命周期管理器"""
    
    def __init__(self, registry_path: str):
        self.registry_path = registry_path
        self._data = self._load()
    
    def _load(self) -> Dict:
        if os.path.exists(self.registry_path):
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"products": {}}
    
    def _save(self):
        self._data["updated_at"] = datetime.now(timezone.utc).isoformat()
        os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)
    
    def list_products(self, stage: Optional[str] = None) -> List[Dict]:
        """列出所有产品或按stage筛选"""
        results = []
        for key, info in self._data.get("products", {}).items():
            if stage is None or info.get("stage") == stage:
                results.append({"key": key, **info})
        return sorted(results, key=lambda x: x.get("key", ""))
    
    def get_product(self, key: str) -> Optional[Dict]:
        return self._data.get("products", {}).get(key)
    
    def upgrade_stage(self, key: str, target_stage: str) -> Dict:
        """将产品升级到下一阶段"""
        products = self._data.get("products", {})
        if key not in products:
            return {"error": f"Product '{key}' not found"}
        
        current = products[key]["stage"]
        allowed = STAGE_TRANSITIONS.get(current, [])
        
        if target_stage not in allowed:
            return {
                "error": f"Cannot transition from '{current}' to '{target_stage}'. Allowed: {allowed}",
                "current": current,
                "allowed": allowed,
            }
        
        products[key]["stage"] = target_stage
        products[key]["changelog"] = products[key].get("changelog", [])
        products[key]["changelog"].append(
            f"{products[key]['version']}: Stage {current} -> {target_stage}"
        )
        self._save()
        
        return {"success": True, "key": key, "from": current, "to": target_stage}
    
    def record_call(self, key: str, latency_ms: float, success: bool, error: str = ""):
        """记录一次调用（度量数据）"""
        products = self._data.get("products", {})
        if key not in products:
            return
        m = products[key].setdefault("metrics", {"calls": 0, "avg_latency_ms": 0, "error_rate": 0})
        old_calls = m["calls"]
        m["calls"] = old_calls + 1
        # 滚动平均
        m["avg_latency_ms"] = (m["avg_latency_ms"] * old_calls + latency_ms) / m["calls"]
        if not success:
            m["error_rate"] = (m["error_rate"] * old_calls + 1) / m["calls"]
        else:
            m["error_rate"] = (m["error_rate"] * old_calls) / m["calls"]
        self._save()
    
    def set_version(self, key: str, version: str) -> Dict:
        products = self._data.get("products", {})
        if key not in products:
            return {"error": f"Product '{key}' not found"}
        products[key]["version"] = version
        products[key]["changelog"].append(f"{version}: Version bump")
        self._save()
        return {"success": True, "key": key, "version": version}
    
    def get_version(self, key: str) -> str:
        products = self._data.get("products", {})
        return products.get(key, {}).get("version", "0.0.0-dev")
    
    def get_changelog(self, key: str) -> List[str]:
        products = self._data.get("products", {})
        return products.get(key, {}).get("changelog", [])
    
    def summary(self) -> Dict:
        """整体概览"""
        products = self._data.get("products", {})
        stages = {}
        chroms = {}
        for info in products.values():
            s = info.get("stage", "unknown")
            stages[s] = stages.get(s, 0) + 1
            c = info.get("chromosome", 0)
            chroms[c] = chroms.get(c, 0) + 1
        return {
            "total": len(products),
            "stages": stages,
            "chromosomes": dict(sorted(chroms.items())),
        }


if __name__ == '__main__':
    import sys
    registry_path = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\product_registry.json'
    lm = LifecycleManager(registry_path)
    
    print("IGP 研发部 V6 生命周期状态")
    print("=" * 50)
    
    summary = lm.summary()
    print(f"总产品数: {summary['total']}")
    print(f"生命周期分布: {summary['stages']}")
    print()
    
    # 按stage分组建表
    for stage in ["research", "alpha", "beta", "ga", "deprecated", "eol"]:
        prods = lm.list_products(stage=stage)
        if prods:
            print(f"\n[{stage.upper()}] {len(prods)} 个产品:")
            for p in prods[:10]:
                print(f"  {p['key']:<30} v{p['version']}")
            if len(prods) > 10:
                print(f"  ... (+{len(prods)-10} more)")
    
    print(f"\n{'='*50}")
    print(f"版本示例:")
    for key in ["v5_closed_loop_pipeline", "v5_bug_doctor", "v5_symbolic_engine"]:
        info = lm.get_product(key)
        if info:
            print(f"  {info['display_name']:20} v{info['version']:20} [{info['stage']}]")
