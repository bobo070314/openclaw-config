"""
IGP 研发部 V6 — API 客户端
给下游部门用：一行代码调用API
"""
from __future__ import annotations
import json
import urllib.request
import urllib.error
from typing import Any, Dict, Optional


class IGPAPIClient:
    """IGP API 客户端 — 给部门员工import用"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url.rstrip('/')
    
    def _get(self, path: str) -> Dict:
        url = f"{self.base_url}{path}"
        try:
            with urllib.request.urlopen(url) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _post(self, path: str, data: Dict) -> Dict:
        url = f"{self.base_url}{path}"
        body = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
    
    # ======== 生命周期 API ========
    def health(self) -> Dict:
        return self._get("/api/v1/health")
    
    def lifecycle_summary(self) -> Dict:
        return self._get("/api/v1/lifecycle")
    
    def list_products(self, stage: Optional[str] = None) -> Dict:
        path = "/api/v1/lifecycle/products"
        if stage:
            path += f"?stage={stage}"
        return self._get(path)
    
    def get_product(self, key: str) -> Dict:
        return self._get(f"/api/v1/lifecycle/product/{key}")
    
    def upgrade_stage(self, key: str, stage: str) -> Dict:
        return self._post("/api/v1/lifecycle/upgrade", {"key": key, "stage": stage})
    
    def get_version(self, key: str) -> Dict:
        return self._get(f"/api/v1/version/{key}")
    
    def set_version(self, key: str, version: str) -> Dict:
        return self._post("/api/v1/lifecycle/version", {"key": key, "version": version})
    
    def record_call(self, product: str, latency_ms: float, success: bool, error: str = "") -> Dict:
        return self._post("/api/v1/lifecycle/record", {
            "product": product, "latency_ms": latency_ms, "success": success, "error": error,
        })
    
    # ======== PRD API ========
    def submit_prd(self, department: str, product: str, title: str, priority: str = "normal", description: str = "") -> Dict:
        return self._post("/api/v1/prd/submit", {
            "department": department, "product": product, "title": title,
            "priority": priority, "description": description,
        })
    
    def prd_summary(self) -> Dict:
        return self._get("/api/v1/prd")
    
    def prd_list(self) -> Dict:
        return self._get("/api/v1/prd/list")
    
    # ======== 评审 API ========
    def review_file(self, filepath: str) -> Dict:
        return self._post("/api/v1/review", {"file": filepath})


if __name__ == '__main__':
    client = IGPAPIClient()
    
    print("IGP API 客户端测试")
    print("=" * 50)
    
    # health
    h = client.health()
    print(f"Health: {h}")
    
    # lifecycle
    ls = client.lifecycle_summary()
    print(f"总产品数: {ls.get('total', 'N/A')}")
    print(f"生命周期: {ls.get('stages', {})}")
    
    # 查版本（现有产品）
    v = client.get_version("v5_bug_doctor")
    print(f"BugDoctor: v{v.get('version', 'N/A')}")
    
    # PRD
    prd = client.submit_prd("market", "BugDoctor", "需要Python 3.14装饰器检测", "high")
    print(f"PRD提交: {prd.get('id', 'error')}")
    
    prds = client.prd_summary()
    print(f"PRD队列: {prds}")
    
    print("\n✅ API客户端可用")
