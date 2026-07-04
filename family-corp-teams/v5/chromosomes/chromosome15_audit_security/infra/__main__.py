"""
染色体15_审计安全部 FISSION README
从染色体12_自动测试部裂变而来

继承: v5_logger_context.py, v5_result_monad.py, v5_crypto_kit.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'infra'))

from v5_crypto_kit import CryptoKit
from v5_logger_context import LoggerContext
log = LoggerContext.get('audit_security')

class AuditLogger:
    def __init__(self):
        self.log = log.bind(chromosome='15')
    def info(self, msg): self.log.info(msg)

class AuditCrypto:
    def sign_log(self, msg: str, key: str) -> str:
        return CryptoKit.hmac_sign(key, msg)

if __name__ == '__main__':
    log.info('chromosome15_audit_security ready')
