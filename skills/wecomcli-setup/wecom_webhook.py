"""
企微 Webhook 桥接服务器
接收企微回调消息 → 转发给 OpenClaw Gateway → 将回复送回企微

Usage: python wecom_webhook.py --port 18800 --gateway http://127.0.0.1:18791
"""
import sys
import os
import json
import hashlib
import base64
import struct
import socket
import time
import xml.etree.ElementTree as ET
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))

# ---- Crypto (企微消息加解密 - AES) ----
try:
    from Crypto.Cipher import AES
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False
    print("[WARN] pycryptodome not installed. Run: pip install pycryptodome")
    print("[WARN] Message decryption disabled. Set encryption mode to 'plaintext' in WeCom admin.")


class WXBizMsgCrypt:
    """企微消息加解密"""
    def __init__(self, token, encoding_aes_key, corp_id):
        self.token = token
        self.corp_id = corp_id
        self.aes_key = base64.b64decode(encoding_aes_key + "=")

    def verify_url(self, msg_signature, timestamp, nonce, echostr):
        """验证回调URL"""
        sort_list = sorted([self.token, timestamp, nonce, echostr])
        sha1 = hashlib.sha1("".join(sort_list).encode()).hexdigest()
        if sha1 != msg_signature:
            return None
        return self._decrypt(echostr)

    def decrypt_msg(self, msg_signature, timestamp, nonce, post_data):
        """解密消息"""
        try:
            xml_tree = ET.fromstring(post_data)
            encrypt = xml_tree.find("Encrypt")
            if encrypt is None:
                return None
            sort_list = sorted([self.token, timestamp, nonce, encrypt.text])
            sha1 = hashlib.sha1("".join(sort_list).encode()).hexdigest()
            if sha1 != msg_signature:
                return None
            return self._decrypt(encrypt.text)
        except Exception:
            return None

    def _decrypt(self, encrypt_text):
        cipher = AES.new(self.aes_key, AES.MODE_CBC, self.aes_key[:16])
        plain_text = cipher.decrypt(base64.b64decode(encrypt_text))
        pad = plain_text[-1]
        content = plain_text[16:-pad]
        xml_len = socket.ntohl(struct.unpack("I", content[:4])[0])
        return content[4:4+xml_len].decode("utf-8")

    def encrypt_msg(self, reply_msg, nonce, timestamp=None):
        """加密回复"""
        if timestamp is None:
            timestamp = str(int(time.time()))
        raw = self._get_random_str(16).encode() + struct.pack("I", socket.htonl(len(reply_msg.encode()))) + reply_msg.encode() + self.corp_id.encode()
        pad = 32 - len(raw) % 32
        raw += bytes([pad] * pad)
        cipher = AES.new(self.aes_key, AES.MODE_CBC, self.aes_key[:16])
        encrypt = base64.b64encode(cipher.encrypt(raw)).decode()
        sort_list = sorted([self.token, timestamp, nonce, encrypt])
        sha1 = hashlib.sha1("".join(sort_list).encode()).hexdigest()
        return f"<xml><Encrypt><![CDATA[{encrypt}]]></Encrypt><MsgSignature><![CDATA[{sha1}]]></MsgSignature><TimeStamp>{timestamp}</TimeStamp><Nonce><![CDATA[{nonce}]]></Nonce></xml>"

    @staticmethod
    def _get_random_str(length):
        import random, string
        return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


# ---- OpenClaw Gateway client ----
def send_to_gateway(gateway_url, message, user_id="wecom_user"):
    """发送消息到 OpenClaw Gateway"""
    payload = {
        "message": message,
        "userId": user_id,
        "channel": "wecom-webhook",
    }
    try:
        req = Request(
            f"{gateway_url}/api/message",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}


# ---- HTTP Handler ----
class WeComHandler(BaseHTTPRequestHandler):
    crypt = None
    gateway_url = "http://127.0.0.1:18791"

    def log_message(self, format, *args):
        ts = datetime.now(TZ).strftime("%H:%M:%S")
        print(f"[{ts}] {args[0]}", file=sys.stderr)

    def do_GET(self):
        """企微回调URL验证"""
        params = self._parse_params()
        msg_sig = params.get("msg_signature", [""])[0]
        timestamp = params.get("timestamp", [""])[0]
        nonce = params.get("nonce", [""])[0]
        echostr = params.get("echostr", [""])[0]

        if self.crypt:
            result = self.crypt.verify_url(msg_sig, timestamp, nonce, echostr)
            if result:
                self._reply(200, result)
                return
            self._reply(403, "verify failed")
            return

        self._reply(200, echostr)

    def do_POST(self):
        """接收企微消息"""
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")

        params = self._parse_params()
        msg_sig = params.get("msg_signature", [""])[0]
        timestamp = params.get("timestamp", [""])[0]
        nonce = params.get("nonce", [""])[0]

        # 解密消息
        if self.crypt:
            xml_str = self.crypt.decrypt_msg(msg_sig, timestamp, nonce, body)
            if xml_str is None:
                self._reply(403, "decrypt failed")
                return
        else:
            xml_str = body

        # 解析消息
        msg = self._parse_xml(xml_str)
        if not msg:
            self._reply(200, "success")
            return

        user_id = msg.get("FromUserName", "unknown")
        content = msg.get("Content", "")
        msg_type = msg.get("MsgType", "text")

        ts = datetime.now(TZ).strftime("%H:%M:%S")
        print(f"[{ts}] MSG from {user_id}: {content[:100]}")

        # 转发到 OpenClaw
        if msg_type == "text" and content.strip():
            result = send_to_gateway(self.gateway_url, content, user_id)
            reply_text = result.get("reply", result.get("error", "I received your message but couldn't process it."))
        else:
            reply_text = ""

        # 回复（如果有）
        if reply_text:
            reply_xml = f"""<xml>
<ToUserName><![CDATA[{user_id}]]></ToUserName>
<FromUserName><![CDATA[{msg.get('ToUserName', '')}]]></FromUserName>
<CreateTime>{int(time.time())}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{reply_text}]]></Content>
</xml>"""

            if self.crypt:
                reply_xml = self.crypt.encrypt_msg(reply_xml, nonce)

            self._reply(200, reply_xml)
        else:
            self._reply(200, "success")

    def _parse_params(self):
        from urllib.parse import parse_qs, urlparse
        return parse_qs(urlparse(self.path).query)

    def _parse_xml(self, xml_str):
        try:
            root = ET.fromstring(xml_str)
            return {child.tag: child.text for child in root}
        except Exception:
            return {}

    def _reply(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/xml" if body.startswith("<") else "text/plain")
        self.end_headers()
        self.wfile.write(body.encode("utf-8") if isinstance(body, str) else body)


def main():
    import argparse
    ap = argparse.ArgumentParser(description="WeCom Webhook Bridge for OpenClaw")
    ap.add_argument("--port", type=int, default=18800, help="Webhook listen port (default: 18800)")
    ap.add_argument("--gateway", default="http://127.0.0.1:18791", help="OpenClaw Gateway URL")
    ap.add_argument("--token", default=os.environ.get("WECOM_TOKEN", ""), help="WeCom callback token")
    ap.add_argument("--aes-key", default=os.environ.get("WECOM_ENCODING_AES_KEY", ""), help="WeCom encoding AES key")
    ap.add_argument("--corpid", default=os.environ.get("WECOM_CORPID", ""), help="WeCom CorpID")
    args = ap.parse_args()

    if args.token and args.aes_key and args.corpid and HAS_CRYPTO:
        WeComHandler.crypt = WXBizMsgCrypt(args.token, args.aes_key, args.corpid)
        print("[OK] Message encryption enabled", flush=True)
    else:
        print("[WARN] Encryption disabled (set WECOM_TOKEN/WECOM_ENCODING_AES_KEY/WECOM_CORPID)")

    WeComHandler.gateway_url = args.gateway

    server = HTTPServer(("0.0.0.0", args.port), WeComHandler)
    print(f"[OK] WeCom Webhook listening on port {args.port}", flush=True)
    print(f"[OK] Forwarding to Gateway: {args.gateway}", flush=True)
    print(f"[OK] Configure WeCom callback URL: http://YOUR_IP:{args.port}/", flush=True)
    print()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[OK] Shutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
