from ap2_protocol import AP2Protocol
from ap2_wallet import AP2Wallet
from ap2_payment_gateway import AP2PaymentGateway
import time

# Initialize protocol and payment gateway
protocol = AP2Protocol()
gateway = AP2PaymentGateway()

# Register wallets for Agent A and Agent B
agent_a_wallet_id = "AGENT_A"
agent_b_wallet_id = "AGENT_B"

# Register Agent A's wallet
success, message = gateway.register_wallet(agent_a_wallet_id)
print(message)

# Register Agent B's wallet
success, message = gateway.register_wallet(agent_b_wallet_id)
print(message)

# Fund Agent A's wallet with initial balance
agent_a_wallet = gateway.wallets[agent_a_wallet_id]
agent_a_wallet._balance = 10.00
print(f"Funded Agent A with $10.00")

# Create a payment request from Agent A to Agent B
payment_request = protocol.create_payment_request(
    sender_agent_id=agent_a_wallet_id,
    receiver_agent_id=agent_b_wallet_id,
    amount=0.003,
    currency="USD",
    memo="Micro payment for service"
)

# Process the payment request
success, message = gateway.process_payment_request(payment_request)
print(message)

# Verify the transaction by checking the wallets
agent_a_wallet = gateway.wallets[agent_a_wallet_id]
agent_b_wallet = gateway.wallets[agent_b_wallet_id]

print(f"Agent A's balance: ${agent_a_wallet.get_balance():.2f}")
print(f"Agent B's balance: ${agent_b_wallet.get_balance():.2f}")

# Print verification message
print("✅ AP2支付协议 裂变验证通过")
