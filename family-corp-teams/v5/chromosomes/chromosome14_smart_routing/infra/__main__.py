"""
染色体14_智能路由部 FISSION README
从染色体4_Provider路由部 + 染色体8_AP2支付部裂变而来

继承: v5_smart_router.py, v5_crypto_kit.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'infra'))

from v5_smart_router import SmartRouter
from v5_crypto_kit import CryptoKit
from v5_logger_context import LoggerContext
log = LoggerContext.get('smart_routing')

class SecureSmartRouter:
    def __init__(self):
        self.router = SmartRouter('smart14')
        self.crypto = CryptoKit
    def register(self, n, p, w=1.0):
        self.router.register(n, p, w)
    def route(self, r=None):
        return self.router.route(r)

if __name__ == '__main__':
    log.info('chromosome14_smart_routing ready')
