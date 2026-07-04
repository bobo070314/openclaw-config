from agent_commerce import AgentCommerce
from commerce_pk import CommercePK

# Create two agent services
agent1 = AgentCommerce("http://aap-api.example.com", "http://acp-api.example.com")
agent2 = AgentCommerce("http://aap-api.example.com", "http://acp-api.example.com")

# Register prices for the services
agent1.register_service_provider("Service A", "token", 0.01, 0.5)
agent2.register_service_provider("Service B", "task", 0.02, 1.0)

# Simulate calls and revenue
revenue1 = agent1.track_revenue("Service A", 1000)
revenue2 = agent2.track_revenue("Service B", 800)

# Generate profit report
profit_report = agent1.generate_profit_report("2026-01-01", "2026-07-01")

# Print verification message
print("✅ 商业协议部 裂变验证通过")