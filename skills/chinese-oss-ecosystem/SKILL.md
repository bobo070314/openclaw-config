# chinese-oss-ecosystem

> 国产开源生态工具集 — 常用国内开源中间件/框架操作指南

## 核心组件

### 1. 数据库/中间件 (Apache 2.0 / 国产开源)
```bash
# Apache ShardingSphere 分库分表
# https://shardingsphere.apache.org
# 读写分离 + 数据分片 + 分布式事务

# Seata 分布式事务
# https://seata.io
# AT模式 / TCC / Saga / XA

# Apache Dubbo RPC框架
# https://dubbo.apache.org
# 微服务RPC调用

# Nacos 配置中心/注册中心
# https://nacos.io
# 服务发现 + 配置管理

# SkyWalking APM
# https://skywalking.apache.org
# 链路追踪 + 性能监控

# Sentinel 流量控制
# https://sentinelguard.io
# 限流降级 + 熔断

# RocketMQ 消息队列
# https://rocketmq.apache.org
# 分布式消息 + 事务消息 + 顺序消息
```

### 2. 快速启动

**Nacos (本地测试)**
```bash
# Windows
startup.cmd -m standalone
# 访问 http://localhost:8848/nacos
# 默认账号密码: nacos/nacos
```

**RocketMQ**
```bash
# Docker
docker run -d --name rmqnamesrv -p 9876:9876 apache/rocketmq:latest sh mqnamesrv
docker run -d --name rmqbroker -p 10911:10911 -p 10909:10909 \
  -e "NAMESRV_ADDR=localhost:9876" \
  apache/rocketmq:latest sh mqbroker
```

**Seata**
```yaml
# application.yml
seata:
  enabled: true
  application-id: my-app
  tx-service-group: my_tx_group
  service:
    grouplist:
      default: 127.0.0.1:8091
```

### 3. Spring Boot 集成 (国产生态)
```xml
<!-- Nacos -->
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
</dependency>

<!-- Sentinel -->
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
</dependency>

<!-- Seata -->
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-seata</artifactId>
</dependency>
```

### 4. 配置示例

**Nacos配置**
```yaml
spring:
  cloud:
    nacos:
      discovery:
        server-addr: 127.0.0.1:8848
      config:
        server-addr: 127.0.0.1:8848
        file-extension: yaml
```

**Sentinel限流**
```java
@SentinelResource(value = "getOrder", 
    blockHandler = "handleBlock", 
    fallback = "handleFallback")
public Order getOrder(Long id) {
    return orderService.getById(id);
}
```

**RocketMQ消息**
```java
// 发送
@Autowired
private RocketMQTemplate rocketMQTemplate;

rocketMQTemplate.convertAndSend("order-topic", orderMessage);

// 消费
@RocketMQMessageListener(topic = "order-topic", consumerGroup = "order-group")
public class OrderConsumer implements RocketMQListener<String> {
    @Override
    public void onMessage(String message) {
        // 处理消息
    }
}
```

**ShardingSphere分片**
```yaml
spring:
  shardingsphere:
    datasource:
      names: ds0,ds1
    rules:
      sharding:
        tables:
          order:
            actual-data-nodes: ds$->{0..1}.order_$->{0..1}
            table-strategy:
              standard:
                sharding-column: id
```

### 5. 数据库连接池
```xml
<!-- Druid 数据库连接池 -->
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>druid-spring-boot-starter</artifactId>
    <version>1.2.23</version>
</dependency>
```

## 常用工具
- **Hutool** — Java工具类库（比Apache Commons更全更中国化）
- **EasyExcel** — Java Excel处理（阿里出品，大量数据场景）
- **MyBatis-Plus** — 国产MyBatis增强（自动CRUD，分页，代码生成）
- **Sa-Token** — 国产权限框架（JWT/OAuth2/单点登录）
- **JustAuth** — 第三方登录聚合（微信/支付宝/GitHub/钉钉等十几种）
- **Forest** — HTTP客户端（声明式调用，支持拦截器/重试）

## 参考来源
- Apache ShardingSphere: https://shardingsphere.apache.org
- Alibaba Nacos: https://nacos.io
- Apache Dubbo: https://dubbo.apache.org
- Apache RocketMQ: https://rocketmq.apache.org
- MyBatis-Plus: https://baomidou.com
- Sa-Token: https://sa-token.cc
