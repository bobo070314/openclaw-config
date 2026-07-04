import requests
from typing import Dict, Any, List

class ACPClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def create_checkout(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(f"{self.api_url}/checkout", json=payload)
        return response.json()

    def get_cart(self, cart_id: str) -> Dict[str, Any]:
        response = requests.get(f"{self.api_url}/cart/{cart_id}")
        return response.json()

    def update_cart_item(self, cart_id: str, item_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.put(f"{self.api_url}/cart/{cart_id}/item/{item_id}", json=payload)
        return response.json()

    def delete_cart_item(self, cart_id: str, item_id: str) -> Dict[str, Any]:
        response = requests.delete(f"{self.api_url}/cart/{cart_id}/item/{item_id}")
        return response.json()

    def checkout(self, cart_id: str) -> Dict[str, Any]:
        response = requests.post(f"{self.api_url}/checkout/{cart_id}")
        return response.json()

    def get_quote(self, product_id: str) -> Dict[str, Any]:
        response = requests.get(f"{self.api_url}/quote/{product_id}")
        return response.json()

    def place_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(f"{self.api_url}/order", json=order_data)
        return response.json()

    def process_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(f"{self.api_url}/payment", json=payment_data)
        return response.json()