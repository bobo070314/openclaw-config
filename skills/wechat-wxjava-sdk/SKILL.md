# wechat-wxjava-sdk

> 微信开发 Java SDK 操作指南 — 支持公众号、小程序、企业微信、微信支付、视频号

## 环境要求
- Java 8+
- Maven 或 Gradle
- GitHub: https://github.com/binarywang/WxJava

## Maven 引入
```xml
<dependency>
    <groupId>com.github.binarywang</groupId>
    <artifactId>weixin-java-mp</artifactId>
    <version>4.6.0</version>
</dependency>
```

## 核心模块

### 1. 公众号开发（MP）
```java
// 配置
WxMpInMemoryConfigStorage config = new WxMpInMemoryConfigStorage();
config.setAppId("wx...");
config.setSecret("...");
WxMpService wxMpService = new WxMpServiceImpl();
wxMpService.setWxMpConfigStorage(config);

// 发送模板消息
WxMpTemplateMessage templateMsg = WxMpTemplateMessage.builder()
    .toUser("openid")
    .templateId("template_id")
    .build();
wxMpService.getTemplateMsgService().sendTemplateMsg(templateMsg);

// 创建菜单
WxMpMenuService menuService = wxMpService.getMenuService();
menuService.menuCreate(menuJson);

// 获取用户信息
WxMpUser user = wxMpService.getUserService().userInfo("openid");
```

### 2. 企业微信（CP）
```java
WxCpService cpService = new WxCpServiceImpl();
cpService.setWxCpConfigStorage(config);

// 发送应用消息
WxCpMessage message = WxCpMessage.TEXT()
    .agentId(1000004)
    .toUser("userid")
    .content("消息内容")
    .build();
cpService.getMessageService().send(message);
```

### 3. 微信支付（Pay）
```java
// 统一下单
WxPayUnifiedOrderRequest request = WxPayUnifiedOrderRequest.newBuilder()
    .outTradeNo("202606300001")
    .totalFee(1)  // 单位：分
    .body("测试商品")
    .spbillCreateIp("127.0.0.1")
    .notifyUrl("https://your-domain.com/notify")
    .tradeType("JSAPI")
    .openid("用户openid")
    .build();

WxPayService wxPayService = new WxPayServiceImpl();
WxPayUnifiedOrderResult result = wxPayService.unifiedOrder(request);
```

### 4. 小程序（MiniApp）
```java
WxMaService maService = new WxMaServiceImpl();
maService.setWxMaConfig(config);

// 登录
WxMaJscode2SessionResult session = maService.jsCode2SessionInfo("code");
String openid = session.getOpenid();

// 获取用户手机号
WxMaPhoneNumberInfo phoneInfo = maService.getPhoneNoInfo("encryptedData", "sessionKey", "iv");
```

### 5. 视频号（Channel）
```java
// 视频号小店
WxChannelService channelService = wxMpService.getChannelService();
// 获取商品列表
channelService.getGoodsList(page, pageSize);
```

## 常用工具类
```java
// XML与对象互转
WxTypeUtils.fromXml(xml, WxPayUnifiedOrderResult.class);
WxTypeUtils.toXml(result);

// AES解密
WxAesUtils.decrypt(encryptedData, aesKey, iv);
```

## 最佳实践
- Token和AccessToken缓存到Redis（避免频繁刷新）
- 回调URL用HTTPS
- 微信支付异步通知要验证签名
- 企业微信消息支持Markdown格式

## 参考来源
- GitHub: https://github.com/binarywang/WxJava
- 微信官方文档: https://developers.weixin.qq.com
