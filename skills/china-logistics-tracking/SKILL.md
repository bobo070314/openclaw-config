# china-logistics-tracking — 物流快递查询

> 国内物流快递一站式查询 — 支持所有主流快递公司（顺丰/京东/菜鸟/通达系/邮政）

## 使用场景
- 查询快递单号物流轨迹
- 批量查询多个单号
- 快递公司识别（自动匹配单号归属）
- 物流时效预估

## 核心API

### 方式1：快递100（最通用，免费额度）
```python
import requests
import json

# 自动识别快递公司
def auto_identify(num):
    url = "https://www.kuaidi100.com/autonumber/autoComNum"
    resp = requests.post(url, data={"text": num})
    data = resp.json()
    if data.get("auto"):
        return data["auto"][0]["comCode"]
    return None

# 查询物流轨迹
def track(num, com_code=None):
    """com_code 为空则自动识别"""
    if not com_code:
        com_code = auto_identify(num)
    if not com_code:
        return {"error": "无法识别快递公司"}
    
    url = "https://www.kuaidi100.com/query"
    params = {
        "type": com_code,
        "postid": num,
        "temp": int(time.time() * 1000),
        "phone": ""  # 顺丰需要填手机号后4位
    }
    resp = requests.get(url, params=params, headers={
        "User-Agent": "Mozilla/5.0"
    })
    return resp.json()

# 返回示例
{
    "status": "200",       # 200=正常
    "message": "ok",
    "nu": "SF1234567890",  # 单号
    "com": "shunfeng",     # 快递公司
    "state": "3",          # 0=在途,1=揽收,2=疑难,3=签收,4=退签,5=派件,8=清关
    "data": [
        {"time": "2026-06-30 15:30:00", "context": "快件已签收"},
        {"time": "2026-06-30 10:00:00", "context": "正在派件中"},
        {"time": "2026-06-30 06:00:00", "context": "到达派件站点"},
    ]
}

# 批量查询
def batch_track(nums, com_codes=None):
    results = []
    for i, num in enumerate(nums):
        com = com_codes[i] if com_codes else None
        results.append(track(num, com))
    return results
```

### 方式2：快递鸟（需要注册Key）
```bash
pip install kdniao
```

```python
from kdniao import KdNiaoApi

api = KdNiaoApi("EBusinessID", "AppKey")

# 即时查询
result = api.track(
    logistic_code="SF1234567890",
    shipper_code="SF"  # SF=顺丰, YTO=圆通, STO=申通, ZTO=中通
)
```

### 方式3：顺丰API（官方）
```python
import requests
import hashlib
import time

def sf_track(num, phone_last4=""):
    url = "https://api-sf.51tracking.com/v1/tracking"
    headers = {
        "Content-Type": "application/json",
        "Tracking-Api-Key": "your_key"
    }
    resp = requests.post(url, json={
        "tracking_number": num,
        "carrier_code": "shunfeng",
        "phone": phone_last4
    }, headers=headers)
    return resp.json()
```

## 快递公司代号表
| 代号 | 快递公司 | 识别规则 |
|------|----------|----------|
| shunfeng | 顺丰 | 以SF开头 |
| jd | 京东 | 以JD开头 |
| yuantong | 圆通 | 10位纯数字 |
| zhongtong | 中通 | 12位数字 |
| shentong | 申通 | 12位数字 |
| yunda | 韵达 | 13位数字 |
| ems | EMS | 以E开头 |
| debang | 德邦 | 8-10位数字 |
| huitong | 百世 | 12-13位 |

## 电商物流状态机
```
待揽收 → 已揽收 → 运输中 → 到达分拨
                                         ↓
             已签收 ← 派送中 ← 到达派件站
```

## 最佳实践
- 优先用快递100（免费、覆盖面最全）
- 顺丰单号需要手机号后4位才能查
- 京东物流不需要手机号
- 批量查询建议限速（每秒最多10次）
- 国际物流用17TRACK（支持1000+物流商）

## 参考来源
- 快递100: https://www.kuaidi100.com
- 快递鸟: https://www.kdniao.com
- 17TRACK: https://www.17track.net
