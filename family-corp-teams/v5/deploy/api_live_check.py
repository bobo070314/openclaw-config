#!/usr/bin/env python3
"""IGP V5 外接真实API检查 — GitHub / Stripe / AP2"""
import os, sys, json, socket, hashlib, time, urllib.request, urllib.error
from datetime import datetime, timezone

tw = lambda: datetime.now(timezone.utc).isoformat()

def check_github():
    """检测GitHub API"""
    token = os.environ.get('GITHUB_TOKEN', '')
    if not token:
        return '⏸️ 无Token (mock就绪)'
    try:
        req = urllib.request.Request('https://api.github.com/user')
        req.add_header('Authorization', f'token {token}')
        req.add_header('User-Agent', 'IGP-V5')
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            return f'✅ 已连接 ({data.get("login","?")})'
    except Exception as e:
        return f'⏸️ 连接失败 ({str(e)[:40]})'

def check_stripe():
    """检测Stripe API Key"""
    key = os.environ.get('STRIPE_API_KEY', '')
    if not key:
        return '⏸️ 无Key (FREE_MODE=mock)'
    # FREE_MODE下不发出真实请求
    return '⏸️ 有Key但FREE_MODE=ON (设FREE_MODE=False才live)'

def check_ap2():
    """AP2本地Agent通信"""
    try:
        from ap2_protocol import AP2Protocol
    except ImportError:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'chromosomes', 'chromosome8', 'infra'))
        from ap2_protocol import AP2Protocol
    from ap2_wallet import AP2Wallet
    from ap2_payment_gateway import AP2PaymentGateway

    gateway = AP2PaymentGateway()
    gateway.register_wallet('AGENT_A', currency='USD')
    gateway.register_wallet('AGENT_B', currency='USD')
    gateway.wallets['AGENT_A'].update_balance(1.00)

    proto = AP2Protocol()
    req = proto.create_payment_request('AGENT_A', 'AGENT_B', 0.003, 'USD', 'AP2 micro test')
    gateway.process_payment_request(req)

    bal_a = gateway.wallets['AGENT_A'].get_balance()
    bal_b = gateway.wallets['AGENT_B'].get_balance()
    if bal_a != bal_b and bal_b > 0:
        return f'✅ 本地Agent通信成功 (A:${bal_a:.3f} → B:${bal_b:.3f})'
    else:
        return f'⚠️ 通信但余额异常 (A:${bal_a:.3f}, B:${bal_b:.3f})'

def main():
    print('='*50)
    print('  🔌 IGP V5 外接API检查')
    print(f'  {tw()}')
    print('='*50)
    print(f'  GitHub:  {check_github()}')
    print(f'  Stripe:  {check_stripe()}')
    print(f'  AP2:     {check_ap2()}')
    print('='*50)

if __name__ == '__main__':
    main()
