# alipay-ijpay-integration

> 支付宝微信聚合支付集成指南 — 基于 IJPay 开源支付工具包

## 环境要求
- Java 8+
- Maven
- GitHub: https://github.com/Javen205/IJPay

## 特性
- 支持微信支付、支付宝、QQ钱包、银联支付、京东支付
- 支持普通商户、服务商、境外支付
- 支持 Api-v3 与 Api-v2 接口
- 不依赖MVC框架，可嵌入任何系统

## Maven 引入
```xml
<dependency>
    <groupId>com.github.javen205</groupId>
    <artifactId>IJPay-All</artifactId>
    <version>latest-version</version>
</dependency>
```

## 支付宝支付

### 普通支付
```java
// 统一下单
AlipayTradeAppPayResponse response = AliPayApi.tradeAppPay(
    AliPayModel.builder()
        .outTradeNo("202606300001")
        .totalAmount("0.01")
        .subject("测试商品")
        .body("商品描述")
        .build(),
    aliPayConfig
);

// 查询
AlipayTradeQueryResponse query = AliPayApi.tradeQuery(
    AlipayTradeQueryModel.builder()
        .outTradeNo("202606300001")
        .build(),
    aliPayConfig
);

// 退款
AlipayTradeRefundResponse refund = AliPayApi.tradeRefund(
    AlipayTradeRefundModel.builder()
        .outTradeNo("202606300001")
        .refundAmount("0.01")
        .build(),
    aliPayConfig
);
```

### 手机网站支付
```java
// WAP支付
AlipayTradeWapPayResponse wapResponse = AliPayApi.tradeWapPay(
    AliPayModel.builder()
        .outTradeNo("202606300002")
        .totalAmount("0.01")
        .subject("WAP支付")
        .quitUrl("https://your-domain.com/return")
        .build(),
    aliPayConfig
);
```

## 微信支付

### JSAPI支付（公众号/小程序）
```java
// 统一下单
Map<String, String> params = new HashMap<>();
params.put("appid", "wx...");
params.put("mch_id", "商户号");
params.put("nonce_str", WxPayKit.generateStr());
params.put("body", "商品描述");
params.put("out_trade_no", "202606300001");
params.put("total_fee", "1");  // 单位:分
params.put("spbill_create_ip", "127.0.0.1");
params.put("notify_url", "https://your-domain.com/notify");
params.put("trade_type", "JSAPI");
params.put("openid", "用户openid");

String xmlResult = WxPayApi.pushOrder(false, params);
Map<String, String> resultMap = WxPayKit.xmlToMap(xmlResult);
```

### H5支付
```java
// H5支付
params.put("trade_type", "MWEB");
String xmlResult = WxPayApi.pushOrder(false, params);
```

## 回调处理
```java
// 支付宝异步通知
@RequestMapping("/ali/notify")
public String aliNotify(HttpServletRequest request) {
    Map<String, String> params = AliPayApi.toMap(request);
    if (AliPayApi.verifyNotify(params, aliPayConfig)) {
        // 验证成功，处理业务逻辑
        return "success";
    }
    return "failure";
}

// 微信异步通知
@RequestMapping("/wx/notify")
public String wxNotify(HttpServletRequest request) {
    String xmlMsg = IOUtils.toString(request.getInputStream(), "UTF-8");
    Map<String, String> params = WxPayKit.xmlToMap(xmlMsg);
    if (WxPayKit.verifyNotify(params, wxPayConfig.getApiKey())) {
        // 处理业务逻辑
        return WxPayKit.xmlNotifySuccess();
    }
    return WxPayKit.xmlNotifyFailure();
}
```

## 最佳实践
- 多商户场景用服务商模式（sub_mch_id）
- 异步通知要幂等处理（避免重复到账）
- 证书过期提前更换
- 退款用原路返回
- 测试环境用沙箱：https://open.alipay.com/platform/appDaily.htm

## 参考来源
- GitHub: https://github.com/Javen205/IJPay
- 支付宝文档: https://opendocs.alipay.com
- 微信支付文档: https://pay.weixin.qq.com
