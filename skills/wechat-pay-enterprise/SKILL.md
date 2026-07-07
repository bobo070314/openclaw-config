# wechat-pay-enterprise-integration

> 微信支付与企业收款集成 — 微信支付V3/企业付款到零钱/商家转账到零钱

## 使用场景
- 网站/APP/小程序接入微信支付
- 企业付款到用户零钱（红包、返佣）
- 商家转账到零钱（提现、结算）

## 环境要求
- 微信商户平台账号（https://pay.weixin.qq.com）
- APIv3密钥和证书
- Node.js或Java

## 核心API

### 1. JSAPI支付（公众号/小程序）
```javascript
const wxpay = require('wxpay-v3');

const result = await wxpay.transactions.jsapi({
    appid: 'wx...',
    mchid: '商户号',
    description: '商品描述',
    out_trade_no: '订单号',
    notify_url: 'https://your-domain.com/notify',
    amount: {
        total: 1,  // 分
        currency: 'CNY'
    },
    payer: {
        openid: '用户openid'
    }
});
```

### 2. H5支付
```javascript
const result = await wxpay.transactions.h5({
    appid: 'wx...',
    mchid: '商户号',
    description: 'H5支付测试',
    out_trade_no: '订单号',
    notify_url: 'https://your-domain.com/notify',
    amount: { total: 1, currency: 'CNY' },
    scene_info: {
        payer_client_ip: '127.0.0.1',
        h5_info: {
            type: 'Wap',
            app_name: '网站名称',
            site_url: 'https://your-domain.com'
        }
    }
});
```

### 3. Native支付（扫码）
```javascript
const result = await wxpay.transactions.native({
    appid: 'wx...',
    mchid: '商户号',
    description: '扫码支付测试',
    out_trade_no: '订单号',
    notify_url: 'https://your-domain.com/notify',
    amount: { total: 1, currency: 'CNY' }
});
// result.code_url 是二维码链接
```

### 4. 企业付款到零钱
```javascript
// 需要开通企业付款功能
const result = await wxpay.transfer.batch({
    appid: 'wx...',
    out_batch_no: '批次号',
    batch_name: '返佣结算',
    batch_remark: '6月返佣',
    total_amount: 100,  // 分
    total_num: 1,
    transfer_detail_list: [{
        out_detail_no: '明细号',
        transfer_amount: 100,
        transfer_remark: '返佣',
        openid: '用户openid'
    }]
});
```

### 5. 退款
```javascript
const result = await wxpay.refunds.create({
    out_refund_no: '退款单号',
    transaction_id: '微信订单号',
    amount: {
        refund: 1,       // 退款金额
        total: 1,        // 原订单金额
        currency: 'CNY'
    }
});
```

### 6. 订单查询
```javascript
// 按微信订单号查询
const result = await wxpay.transactions.queryByTransactionId('微信订单号');

// 按商户订单号查询
const result = await wxpay.transactions.queryByOutTradeNo('订单号');
```

## Node.js SDK (wechatpay-nodejs)
```bash
npm install wechatpay-nodejs
```

```javascript
const { Wechatpay } = require('wechatpay-nodejs');
const wxpay = new Wechatpay({
    appid: 'wx...',
    mchid: '商户号',
    key: 'APIv3密钥',       // 微信商户平台设置
    serialNo: '证书序列号',
    publicKey: fs.readFileSync('./apiclient_cert.pem'),
    privateKey: fs.readFileSync('./apiclient_key.pem'),
});
```

## 企业微信支付
```javascript
// 企业微信红包
const result = await wxpay.transfer.redpacket({
    wxappid: 'wx...',
    send_name: '公司名称',
    re_openid: '用户openid',
    total_amount: 100,
    total_num: 1,
    wishing: '恭喜发财',
    act_name: '红包活动'
});
```

## 注意事项
- **APIv3密钥**在微信商户平台->账户中心->API安全设置
- 证书：`apiclient_cert.pem` + `apiclient_key.pem`
- 异步通知：接收POST回调，验证签名，返回`{"code":"SUCCESS","message":"成功"}`
- 企业付款需要额外开通权限，联系微信支付运营经理
- 境外汇款、国际卡支付需要单独签约

## 参考来源
- 微信支付文档: https://pay.weixin.qq.com/docs/merchant/products
- APIv3指南: https://pay.weixin.qq.com/docs/merchant/development
