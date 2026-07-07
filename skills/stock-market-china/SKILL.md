# stock-market-china — A股/港股/美股行情与交易

> 中国股市行情查询与技术分析工具 — 支持实时行情、K线、财务报表、新股申购

## 环境要求
- 网络连接（无需API Key即可使用公开行情API）
- 可选：东方财富/同花顺账号（需要交易功能）

## 数据获取方式

### 方式1：Akshare（Python，免费）
```bash
pip install akshare
```

```python
import akshare as ak

# 实时行情（所有A股）
df = ak.stock_zh_a_spot_em()
print(df[['代码', '名称', '最新价', '涨跌幅', '成交量']])

# 个股历史K线
df = ak.stock_zh_a_hist(symbol="000001", period="daily", 
                        start_date="20260101", end_date="20260630",
                        adjust="qfq")  # qfq=前复权
print(df.tail(10))

# 港股行情
df = ak.stock_hk_spot_em()

# 北向资金
df = ak.stock_hsgt_north_net_flow_in_em(symbol="沪股通")

# 龙虎榜
df = ak.stock_lhb_ggtj_em()
```

### 方式2：新浪财经API（免费，无依赖）
```python
import requests
import json

# 实时行情
def get_realtime(code):
    """code格式: sh600036 / sz000001 / hk00700"""
    url = f"http://hq.sinajs.cn/list={code}"
    headers = {"Referer": "https://finance.sina.com.cn"}
    resp = requests.get(url, headers=headers)
    # 解析返回数据
    data = resp.text.split('=')[1].strip('"').split(',')
    return {
        "name": data[0],
        "open": data[1],
        "close": data[2],
        "price": data[3],
        "high": data[4],
        "low": data[5],
        "volume": data[8]
    }

# 历史K线
def get_history(code, scale=60, datalen=169):
    """scale=60日线, datalen=169最新"""
    url = f"https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={code}&scale={scale}&ma=no&datalen={datalen}"
    resp = requests.get(url)
    return json.loads(resp.text)
```

### 方式3：Tushare Pro（需注册免费Token）
```bash
pip install tushare
```

```python
import tushare as ts
pro = ts.pro_api('your_token')

# 日线行情
df = pro.daily(ts_code='000001.SZ', start_date='20260101', end_date='20260630')

# 财务数据
df = pro.fina_indicator(ts_code='600036.SH', fields='eps,roe,profit_dedt')

# 实时行情
df = pro.realtime_tick(ts_code='600036.SH')
```

## 常用技术指标

```python
import pandas as pd
import numpy as np

def calc_ma(df, n=5):
    df[f'MA{n}'] = df['close'].rolling(window=n).mean()
    return df

def calc_macd(df, fast=12, slow=26, signal=9):
    df['EMA_fast'] = df['close'].ewm(span=fast).mean()
    df['EMA_slow'] = df['close'].ewm(span=slow).mean()
    df['DIF'] = df['EMA_fast'] - df['EMA_slow']
    df['DEA'] = df['DIF'].ewm(span=signal).mean()
    df['MACD'] = 2 * (df['DIF'] - df['DEA'])
    return df

def calc_kdj(df, n=9):
    low_n = df['low'].rolling(window=n).min()
    high_n = df['high'].rolling(window=n).max()
    df['RSV'] = (df['close'] - low_n) / (high_n - low_n) * 100
    df['K'] = df['RSV'].ewm(com=2).mean()
    df['D'] = df['K'].ewm(com=2).mean()
    df['J'] = 3 * df['K'] - 2 * df['D']
    return df

def calc_rsi(df, n=14):
    diff = df['close'].diff()
    gain = diff.where(diff > 0, 0).rolling(window=n).mean()
    loss = (-diff.where(diff < 0, 0)).rolling(window=n).mean()
    df['RSI'] = 100 - 100 / (1 + gain / loss)
    return df
```

## 美股行情
```python
# 通过新浪获取美股
# code=gb_aapl, gb_tsla, gb_msft
def get_us_stock(code):
    url = f"http://hq.sinajs.cn/list=gb_{code.lower()}"
    headers = {"Referer": "https://finance.sina.com.cn"}
    resp = requests.get(url, headers=headers)
    data = resp.text.split('=')[1].strip('"').split(',')
    return {
        "name": data[0],
        "price": data[1],
        "change": data[2],
        "change_pct": data[3]
    }
```

## 基金查询
```python
# 基金实时净值
df = ak.fund_etf_spot_em()

# 基金持仓
df = ak.fund_portfolio_hold_detail_em(symbol="110011")
```

## 最佳实践
- 实时行情优先用新浪（最快，无限制）
- 历史数据和财务分析用AkShare（数据结构化好）
- 批量分析用Tushare Pro（效率高）
- 界面展示推荐用mplfinance画K线图
- 交易策略建议用backtrader（本地回测）

## 参考来源
- AkShare: https://akshare.akfamily.xyz
- Tushare: https://tushare.pro
- 新浪财经: https://finance.sina.com.cn
- 东方财富: https://quote.eastmoney.com
