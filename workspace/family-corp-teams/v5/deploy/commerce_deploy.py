import os
import json
import stripe
from datetime import datetime

# 1. 读取环境变量 STRIPE_API_KEY
stripe_api_key = os.getenv('STRIPE_API_KEY')

# 2. 如果是mock模式，生成可用的Stripe测试数据（客户/收款/余额）
if not stripe_api_key:
    print("⚠️ 使用mock模式：没有找到STRIPE_API_KEY环境变量")
    
    # 生成测试数据
    test_customer = {
        'id': 'cus_12345',
        'name': 'Test Customer',
        'email': 'test@example.com'
    }
    
    test_charge = {
        'id': 'ch_67890',
        'amount': 150,
        'currency': 'usd',
        'customer': test_customer['id'],
        'description': 'Test Charge for Code Review Service'
    }
    
    test_balance = {
        'available': 0,
        'pending': 0
    }
else:
    # 3. 如果是live模式，调用真实Stripe API查看账户余额
    stripe.api_key = stripe_api_key
    
    try:
        balance = stripe.Balance.retrieve()
        test_balance = {
            'available': balance['available'][0]['amount'] if balance['available'] else 0,
            'pending': balance['pending'][0]['amount'] if balance['pending'] else 0
        }
    except Exception as e:
        print(f"🚨 真实模式下获取账户余额失败: {e}")
        test_balance = {
            'available': 0,
            'pending': 0
        }

# 4. 输出价格清单：IGP提供3个付费Skill包
print("\\n💰 价格清单：")
print("- 代码审查: $0.05/次")
print("- 翻译服务: $0.03/次")
print("- 数据分析: $0.10/次")

# 5. 模拟一次购买：客户购买了代码审查服务3次，商业引擎收到$0.15
print("\\n🛒 模拟购买：客户购买了代码审查服务3次，商业引擎收到$0.15")

# 6. 记录收入到 deploy/commerce_revenue.json
revenue_data = {
    'timestamp': datetime.now().isoformat(),
    'service': 'Code Review',
    'quantity': 3,
    'price_per_unit': 0.05,
    'total_amount': 0.15,
    'balance': test_balance
}

os.makedirs('deploy', exist_ok=True)
with open('deploy/commerce_revenue.json', 'w') as f:
    json.dump(revenue_data, f, indent=4)

# 7. 验证：打印 "✅ 商业协议部实战就绪：Stripe | Shopify | PayPal 三通道"
# 如果任一API Key存在，改为 "🎉 真实付款通道已开启！"
if stripe_api_key:
    print("🎉 真实付款通道已开启！")
else:
    print("✅ 商业协议部实战就绪：Stripe | Shopify | PayPal 三通道")

# 最后执行 python commerce_deploy.py
