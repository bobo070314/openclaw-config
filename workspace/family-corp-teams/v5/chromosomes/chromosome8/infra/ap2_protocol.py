import json
import hashlib
import time

class AP2Protocol:
    def __init__(self):
        self.version = "1.0"
        self.signature_algorithm = "SHA256"
        
    def create_payment_request(self, sender_agent_id, receiver_agent_id, amount, currency, memo=""):
        payment_request = {
            "version": self.version,
            "sender": sender_agent_id,
            "receiver": receiver_agent_id,
            "amount": amount,
            "currency": currency,
            "memo": memo,
            "timestamp": int(time.time())
        }
        
        # Generate signature
        payload = json.dumps(payment_request).encode('utf-8')
        signature = hashlib.sha256(payload).hexdigest()
        payment_request["signature"] = signature
        
        return payment_request

    def verify_payment_request(self, payment_request):
        # Check if required fields are present
        required_fields = ["version", "sender", "receiver", "amount", "currency", "timestamp", "signature"]
        for field in required_fields:
            if field not in payment_request:
                return False, f"Missing required field: {field}"
        
        # Verify signature
        payload = json.dumps({k: v for k, v in payment_request.items() if k != 'signature'}).encode('utf-8')
        expected_signature = hashlib.sha256(payload).hexdigest()
        if payment_request["signature"] != expected_signature:
            return False, "Invalid signature"
        
        # Check timestamp (within 5 minutes)
        current_time = int(time.time())
        if abs(current_time - payment_request["timestamp"]) > 300:
            return False, "Expired payment request"
        
        return True, "Payment request verified successfully"

    def aggregate_micro_payments(self, payments):
        # Aggregate micro payments into a single transaction
        aggregated = {}
        for payment in payments:
            key = (payment["sender"], payment["receiver"], payment["currency"])
            if key not in aggregated:
                aggregated[key] = {
                    "sender": payment["sender"],
                    "receiver": payment["receiver"],
                    "currency": payment["currency"],
                    "total_amount": 0
                }
            aggregated[key]["total_amount"] += payment["amount"]
        
        return list(aggregated.values())

    def create_receipt(self, payment_request, transaction_id):
        receipt = {
            "transaction_id": transaction_id,
            "sender": payment_request["sender"],
            "receiver": payment_request["receiver"],
            "amount": payment_request["amount"],
            "currency": payment_request["currency"],
            "timestamp": payment_request["timestamp"],
            "status": "pending"
        }
        return receipt

    def create_invoice(self, payment_request, transaction_id, status="pending"):
        invoice = {
            "transaction_id": transaction_id,
            "sender": payment_request["sender"],
            "receiver": payment_request["receiver"],
            "amount": payment_request["amount"],
            "currency": payment_request["currency"],
            "timestamp": payment_request["timestamp"],
            "status": status
        }
        return invoice