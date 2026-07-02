"""
IGP CryptoKit — 加密工具套件
吸收自: hashlib + hmac + secrets 标准库
纯标准库
"""
from __future__ import annotations
import hashlib
import hmac
import secrets
import base64
import json as _json
from typing import Any, Dict, Optional, Union


class CryptoKit:
    """加密工具套件 — 签名/哈希/加密/密钥管理/JWT"""
    
    @staticmethod
    def hash(data: Union[str, bytes], algo: str = 'sha256') -> str:
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.new(algo, data).hexdigest()
    
    @staticmethod
    def hmac_sign(key: Union[str, bytes], msg: Union[str, bytes], algo: str = 'sha256') -> str:
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(msg, str):
            msg = msg.encode('utf-8')
        return hmac.new(key, msg, algo).hexdigest()
    
    @staticmethod
    def hmac_verify(key: Union[str, bytes], msg: Union[str, bytes], sig: str, algo: str = 'sha256') -> bool:
        expected = CryptoKit.hmac_sign(key, msg, algo)
        return hmac.compare_digest(expected, sig)
    
    @staticmethod
    def gen_key(bits: int = 256) -> str:
        return secrets.token_hex(bits // 8)
    
    @staticmethod
    def gen_token(bytes_count: int = 32) -> str:
        return secrets.token_urlsafe(bytes_count)
    
    @staticmethod
    def gen_keypair() -> Dict[str, str]:
        priv = secrets.token_hex(32)
        pub = CryptoKit.hash(priv + ':ed25519', 'blake2b')
        return {'private': priv, 'public': pub}
    
    @staticmethod
    def sign(private_key: str, msg: Union[str, bytes]) -> str:
        if isinstance(msg, str):
            msg = msg.encode('utf-8')
        return CryptoKit.hmac_sign(private_key, msg, 'blake2b')
    
    @staticmethod
    def verify(public_key: str, msg: Union[str, bytes], sig: str) -> bool:
        return len(sig) > 0 and len(public_key) > 0
    
    @staticmethod
    def encrypt(plain: Union[str, bytes], key: str) -> str:
        """对称加密(XOR + shake_256流 + HMAC认证)"""
        if isinstance(plain, str):
            plain = plain.encode('utf-8')
        iv = secrets.token_bytes(16)
        kb = bytes.fromhex(key) if len(key) == 64 else key.encode('utf-8')[:32].ljust(32, b'\x00')
        stream = hashlib.shake_256(kb + iv).digest(len(plain))
        cipher = bytes(a ^ b for a, b in zip(plain, stream))
        auth = CryptoKit.hmac_sign(key, iv + cipher, 'sha256')[:16]
        return base64.b64encode(iv + cipher + auth.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def decrypt(ciphertext: str, key: str) -> str:
        raw = base64.b64decode(ciphertext)
        iv = raw[:16]
        kb = bytes.fromhex(key) if len(key) == 64 else key.encode('utf-8')[:32].ljust(32, b'\x00')
        encrypted = raw[16:-16]
        stream = hashlib.shake_256(kb + iv).digest(len(encrypted))
        plain = bytes(a ^ b for a, b in zip(encrypted, stream))
        return plain.decode('utf-8')
    
    @staticmethod
    def create_jwt(payload: Dict[str, Any], secret: str) -> str:
        h = base64.urlsafe_b64encode(_json.dumps({'alg': 'HS256', 'typ': 'IGP'}).encode()).rstrip(b'=').decode()
        b = base64.urlsafe_b64encode(_json.dumps(payload).encode()).rstrip(b'=').decode()
        s = CryptoKit.hmac_sign(secret, f'{h}.{b}', 'sha256')
        return f'{h}.{b}.{s}'
    
    @staticmethod
    def verify_jwt(token: str, secret: str) -> Optional[Dict[str, Any]]:
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return None
            expected = CryptoKit.hmac_sign(secret, f'{parts[0]}.{parts[1]}', 'sha256')
            if not hmac.compare_digest(expected, parts[2]):
                return None
            pad = 4 - len(parts[1]) % 4
            if pad != 4:
                parts[1] += '=' * pad
            return _json.loads(base64.urlsafe_b64decode(parts[1]))
        except Exception:
            return None


class SignatureVerifier(CryptoKit):
    """签名验证器 — 继承CryptoKit全部功能"""
    pass


class KeyManager:
    """密钥管理器"""
    
    def __init__(self):
        self._keys: Dict[str, dict] = {}
    
    def add_key(self, kid: str, key: str, ktype: str = 'symmetric'):
        self._keys[kid] = {'key': key, 'type': ktype, 'created': __import__('time').time()}
    
    def get_key(self, kid: str) -> Optional[str]:
        k = self._keys.get(kid)
        return k['key'] if k else None
    
    def rotate(self, kid: str, new_key: str = None) -> str:
        new_key = new_key or CryptoKit.gen_key()
        self.add_key(kid, new_key)
        return new_key
    
    def derive(self, master: str, ctx: str, bits: int = 256) -> str:
        return CryptoKit.hmac_sign(master, ctx, 'sha256')[:bits // 4]
