"""
IGP V5 商业协议部 v2 —— 接入真实支付/电商API
Stripe + Shopify + PayPal 集成

⚠️ 安全锁定：始终为FREE_MODE（模拟模式）
   除非你亲自解开 FREE_MODE = False 并设环境变量
"""

import json, os, sys, time, hashlib, urllib.request, urllib.parse, urllib.error
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

now_iso = lambda: datetime.now(timezone.utc).isoformat()

# 🔒 安全锁定：永远是模拟模式
# 改这个 = 自己承担真实扣款风险
FREE_MODE = True


class StripeIntegration:
    """Stripe 支付集成 (FREE_MODE锁定，永远不真发请求)"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("STRIPE_API_KEY", "")
        self.base_url = "https://api.stripe.com/v1"
        self._customers = {}
        self._charges = {}
        # 🛡️ 安全保险：FREE_MODE强制mock
        self._mode = "mock"
    
    def create_customer(self, email: str, name: str = "") -> Dict:
        """创建客户"""
        customer = {
            "id": f"cus_mock_{hashlib.md5(email.encode()).hexdigest()[:8]}",
            "email": email,
            "name": name,
            "created": now_iso(),
            "mode": "mock"
        }
        self._customers[customer["id"]] = customer
        return customer
    
    def create_charge(self, amount: int, currency: str, customer_id: str, description: str = "") -> Dict:
        """创建收款"""
        charge = {
            "id": f"ch_mock_{len(self._charges)+1:04d}",
            "amount": amount,
            "currency": currency,
            "customer": customer_id,
            "description": description,
            "status": "succeeded",
            "created": now_iso(),
            "mode": "mock"
        }
        self._charges[charge["id"]] = charge
        return charge
    
    def get_balance(self) -> Dict:
        """获取余额"""
        total_charged = sum(c["amount"] for c in self._charges.values())
        return {
            "available": [{"amount": total_charged, "currency": "usd"}],
            "pending": [{"amount": 0, "currency": "usd"}],
            "mode": "mock"
        }


class ShopifyIntegration:
    """Shopify 电商集成 (FREE_MODE锁定)"""
    
    def __init__(self, access_token: str = None, store: str = None):
        self.access_token = access_token or os.getenv("SHOPIFY_ACCESS_TOKEN", "")
        self.store = store or os.getenv("SHOPIFY_STORE", "igp-demo")
        self._products = {}
        self._orders = {}
        self._mode = "mock"
    
    def list_products(self) -> List[Dict]:
        """列出商品"""
        products = [
            {"id": 1, "title": "Code Review Package", "price": 0.05, "type": "service"},
            {"id": 2, "title": "Translation Service", "price": 0.03, "type": "service"},
            {"id": 3, "title": "Data Analysis Package", "price": 0.10, "type": "service"},
        ]
        for p in products:
            self._products[p["id"]] = p
        return products
    
    def create_order(self, line_items: List[Dict]) -> Dict:
        """创建订单"""
        order = {
            "id": f"order_mock_{len(self._orders)+1:04d}",
            "line_items": line_items,
            "total_price": sum(i.get("price", 0) for i in line_items),
            "status": "active",
            "created": now_iso(),
            "mode": "mock"
        }
        self._orders[order["id"]] = order
        return order


class PayPalIntegration:
    """PayPal 支付集成 (FREE_MODE锁定)"""
    
    def __init__(self, client_id: str = None, client_secret: str = None):
        self.client_id = client_id or os.getenv("PAYPAL_CLIENT_ID", "")
        self.client_secret = client_secret or os.getenv("PAYPAL_CLIENT_SECRET", "")
        self._mode = "mock"
    
    def create_payment(self, amount: float, currency: str = "USD") -> Dict:
        """创建支付"""
        return {
            "id": f"pay_mock_{int(time.time())}",
            "amount": amount,
            "currency": currency,
            "status": "created",
            "links": [{"rel": "approval_url", "href": "https://mock.paypal.com/approve"}],
            "mode": "mock"
        }
    
    def execute_payment(self, payment_id: str, payer_id: str) -> Dict:
        """执行支付"""
        return {
            "id": payment_id,
            "status": "completed",
            "payer_id": payer_id,
            "mode": "mock"
        }


class AgentCommerceEngine:
    """Agent商业交易引擎"""
    
    def __init__(self):
        self.services = {}
        self.transactions = []
        self.revenue = {}
        self.integrations = {
            "stripe": StripeIntegration(),
            "shopify": ShopifyIntegration(),
            "paypal": PayPalIntegration()
        }
    
    def register_service(self, agent_id: str, service_name: str, price_per_task: float) -> Dict:
        """注册Agent服务"""
        service = {
            "id": f"{agent_id}-{service_name.lower().replace(' ', '-')}",
            "agent_id": agent_id,
            "name": service_name,
            "price_per_task": price_per_task,
            "registered": now_iso()
        }
        if agent_id not in self.services:
            self.services[agent_id] = {}
        self.services[agent_id][service["id"]] = service
        if agent_id not in self.revenue:
            self.revenue[agent_id] = 0.0
        return service
    
    def charge_task(self, agent_id: str, task_name: str, tokens: int) -> Dict:
        """对任务收费（模拟）"""
        # 🔒 FREE_MODE: 只记数字，不收钱
        service_charge = tokens * 0.0005  # $0.0005 per token mock pricing
        tx = {
            "id": f"tx_{int(time.time())}_{hashlib.md5(f'{agent_id}{task_name}'.encode()).hexdigest()[:6]}",
            "agent_id": agent_id,
            "task": task_name,
            "tokens": tokens,
            "charge": round(service_charge, 4),
            "timestamp": now_iso(),
            "mode": "mock"
        }
        self.transactions.append(tx)
        self.revenue[agent_id] = round(self.revenue.get(agent_id, 0.0) + service_charge, 4)
        return tx
    
    def get_revenue(self, agent_id: str = None) -> float:
        """获取收入"""
        if agent_id:
            return self.revenue.get(agent_id, 0.0)
        return sum(self.revenue.values())
    
    def get_report(self) -> Dict:
        """生成收入报告"""
        return {
            "total_transactions": len(self.transactions),
            "total_revenue": round(self.get_revenue(), 4),
            "agent_revenues": {k: round(v, 4) for k, v in sorted(self.revenue.items(), key=lambda x: -x[1])},
            "mode": "mock",
            "disclaimer": "🔒 FREE_MODE: 所有金额为模拟数据，未发生真实交易"
        }
