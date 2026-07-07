# vehicle-registration — 车辆手续办理指南

> 国内车辆全生命周期手续办理 — 新车/二手车/过户/上牌/年检/保险/报废

## 一、新车手续

### 提车流程
```
验车 → 付款 → 交强险 → 临牌 → 购置税 → 选号上牌 → 正式牌照
```

### 所需材料
- 身份证原件
- 购车发票（4联）
- 车辆合格证
- 交强险保单（电子版即可）
- 购置税完税证明

### 购置税计算
```python
def calc_purchase_tax(price_without_vat):
    """不含增值税的购车价"""
    tax_rate = 0.10  # 10%
    return price_without_vat * tax_rate

def calc_from_msrp(msrp):
    """从指导价算（含13%增值税）"""
    without_vat = msrp / 1.13
    return round(without_vat * 0.10)

# 举例：20万的车购置税
# 200000 / 1.13 * 0.10 = 17,699元

# 新能源车：2025-2027年免征购置税
```

## 二、二手车过户

### 流程（当日可完成）
```
交易双方到场 → 车辆查验 → 开交易发票 → 过户选号 → 领取新行驶证
```

### 费用
| 项目 | 费用 |
|------|------|
| 交易费 | 300-1000元（按排量/车型） |
| 提档费 | 500-2000元（跨省） |
| 牌照费 | 100-150元 |
| 行驶证 | 10-15元 |
| 总合计 | 约500-3000元 |

### 注意事项
- 车辆无违章、无抵押、无查封
- 交强险在有效期内
- 改装车需还原
- 排放标准：国6b（大部分城市），国5以下限制迁入
- 原车主不用的：号牌可保留2年

```python
def check_transfer_eligibility(car_info):
    """过户可行性检查"""
    issues = []
    if car_info.get("has_penalty"):
        issues.append("有未处理违章")
    if car_info.get("mortgage"):
        issues.append("车辆处于抵押状态")
    if car_info.get("seized"):
        issues.append("车辆被查封")
    if (2026 - car_info.get("year", 2026)) > 15:
        issues.append("超过15年，部分城市限入")
    if car_info.get("emission_standard") in ["国4", "国3"]:
        issues.append("排放标准过低，大部分城市不能迁入")
    return issues or ["过户条件满足"]
```

## 三、年检

### 检测周期
| 车辆类型 | 检测周期 |
|----------|----------|
| 非营运小型客车（6座以下） | 第2/4/8年免检领标，第6/10年上线 |
| 非营运小型客车（7-9座） | 第2/4/8年免检，第6/10年上线 |
| 营运车辆 | 每年1检 |
| 15年以上 | 半年1检 |

### 年检项目
```
外观检查 → 灯光 → 尾气 → 刹车 → 底盘 → 侧滑 → 车速表
```

### 费用
- 上线检测：200-400元
- 逾期未检：罚款200元 + 扣3分

```python
def next_inspection_due(year, month, seats=5):
    """计算下次年检时间"""
    age = 2026 - year
    due_years = []
    
    if seats <= 6:  # 6座以下
        if age < 6:
            if age == 2:
                due_years.append(year + 2)
            if age == 4:
                due_years.append(year + 4)
            due_years.append(year + 6)
        elif age < 10:
            due_years.append(year + 10)
        else:
            # 15年后半年一检
            for y in range(year + 1, 2100):
                due_years.extend([f"{y}-06", f"{y}-12"])
                if y - year > 15:
                    break
    return due_years
```

## 四、保险指南

### 交强险（强制）
```python
# 家庭自用车（6座以下）
COMPULSORY_INSURANCE = {
    "base": 950,  # 基础保费
    "no_claim_bonus": {
        1: 0.9,    # 连续1年无事故打9折
        2: 0.8,    # 连续2年打8折
        3: 0.7,    # 连续3年以上打7折
        "new": 1.0
    },
    "accident_surcharge": {
        1: 1.0,    # 1次事故不打折
        2: 1.1,    # 2次事故上浮10%
        3: 1.2     # 3次事故上浮20%
    },
    "coverage": {
        "death": 180000,   # 死亡伤残
        "medical": 18000,   # 医疗费用
        "property": 2000    # 财产损失
    }
}
```

### 商业险推荐
| 险种 | 推荐 | 说明 |
|------|------|------|
| 车损险 | ✅ | 必买，包含盗抢/玻璃/涉水/自燃/不计免赔 |
| 三者险 | ✅ | 建议200万+（大城市300万） |
| 座位险 | ✅ | 每座1-2万 |
| 划痕险 | ❌ | 出险影响次年保费 |
| 涉水险 | 看地区 | 南方多雨地区建议 |
| 玻璃险 | 看车型 | 高端车建议 |

```python
def calc_insurance(car_value, seats=5, last_year_claims=0, city="一线"):
    """估算保险费用"""
    # 交强险
    compulsory = 950
    if last_year_claims == 0:
        compulsory *= 0.7
    elif last_year_claims >= 3:
        compulsory *= 1.2
    
    # 商业险
    third_party = 1200 if city == "一线" else 800  # 三者200万
    car_damage = car_value * 0.012  # 车损约1.2%
    seat = 200  # 座位险
    
    total = compulsory + third_party + car_damage + seat
    return {
        "compulsory": round(compulsory),
        "third_party": third_party,
        "car_damage": round(car_damage),
        "seat": seat,
        "total": round(total)
    }
```

## 五、违章处理

```
查询渠道：交管12123 APP / 支付宝 + 微信
处理时效：3-15个工作日
异地违章：全国通办（交管12123）
```

```python
VIOLATION_PENALTIES = {
    "闯红灯": ("罚款200元", 6),
    "超速50%以上": ("罚款2000元", 12),
    "违停": ("罚款200元", 0),
    "压实线": ("罚款200元", 3),
    "逆行": ("罚款200元", 3),
    "酒驾": ("罚款5000元", 12, "暂扣驾照6个月"),
    "无证驾驶": ("罚款2000元", 0, "拘留15天")
}
```

## 六、报废流程
```
确认达到报废标准 → 交报废回收企业 → 
注销登记 → 领取报废证明 → 补贴申领（如有）
```

### 报废补贴（以旧换新）
- 新能源车报废：原车价值0-2万元补贴
- 燃油车报废：原车价值0-1万元补贴
- 各地方政策不同，以当地为准

## 七、地区差异
- 北京：需摇号/排号，外地车限行
- 上海：拍牌（约9万），新能源送牌
- 广州/深圳：摇号+竞价
- 杭州：摇号+竞价
- 成都/重庆：直接上牌

## 参考来源
- 交管12123: https://www.122.gov.cn
- 车管所业务流程: 各地车管所官网
- 保险计算: 各保险公司官网
