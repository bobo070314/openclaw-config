import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
from ap2_protocol import AP2Protocol
from ap2_wallet import AP2Wallet

class AP2PaymentGateway:
    def __init__(self):
        self.protocol = AP2Protocol()
        self.wallets = {}
        self.transaction_id_counter = 0

    def register_wallet(self, wallet_id, currency="USD"):
        if wallet_id not in self.wallets:
            self.wallets[wallet_id] = AP2Wallet(wallet_id)
            return True, "Wallet registered successfully"
        return False, "Wallet already exists"

    def process_payment_request(self, payment_request):
        # Verify the payment request
        is_valid, message = self.protocol.verify_payment_request(payment_request)
        if not is_valid:
            return False, message
        
        # Get the sender and receiver wallets
        sender_wallet = self.wallets.get(payment_request["sender"])
        receiver_wallet = self.wallets.get(payment_request["receiver"])
        
        if not sender_wallet or not receiver_wallet:
            return False, "Sender or receiver wallet not found"
        
        # Process the payment
        success, message = sender_wallet.process_payment(payment_request)
        if not success:
            return False, message
        
        # Update the receiver's wallet
        receiver_wallet.update_balance(payment_request["amount"])
        
        # Create a transaction ID
        self.transaction_id_counter += 1
        transaction_id = f"TX{self.transaction_id_counter}"
        
        # Create a receipt and invoice
        receipt = self.protocol.create_receipt(payment_request, transaction_id)
        invoice = self.protocol.create_invoice(payment_request, transaction_id, status="completed")
        
        # Add transactions to both wallets
        sender_wallet.add_transaction(receipt)
        sender_wallet.add_transaction(invoice)
        receiver_wallet.add_transaction(receipt)
        receiver_wallet.add_transaction(invoice)
        
        return True, "Payment processed successfully"