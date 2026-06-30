# used-car-valuation — 二手车评估与估值

> 二手车评估系统 — 基于品牌/车型/年份/里程/车况的智能估值

## 使用场景
- 二手车买家：查询市场行情、估价
- 二手车卖家：估价、定价建议
- 置换评估：旧车置换时的价值计算
- 保险理赔：事故车价值计算

## 车型数据库

```python
# 常见品牌和车型简码
CAR_BRANDS = {
    "BBA": ["宝马", "奔驰", "奥迪"],
    "VW": ["大众", "斯柯达", "西雅特"],
    "JP": ["丰田", "本田", "日产", "马自达", "斯巴鲁", "三菱"],
    "KR": ["现代", "起亚", "双龙"],
    "CN": ["比亚迪", "吉利", "长城", "蔚来", "理想", "小鹏", "小米"],
    "US": ["福特", "别克", "雪佛兰", "凯迪拉克", "特斯拉"],
    "FR": ["标致", "雪铁龙", "雷诺"],
    "UK": ["路虎", "捷豹", "MINI"]
}

# 车型年款数据（示例）
MODELS = {
    "比亚迪唐DM": {
        "years": [2020, 2021, 2022, 2023, 2024],
        "new_price_min": 189800,
        "new_price_max": 289800,
        "depreciation_adjust": {  # 年份衰减
            "year1": 0.15, "year2": 0.10, "year3": 0.08,
            "year4": 0.05, "year5": 0.05, "year6": 0.03
        },
        "mileage_factor": 1.0,  # 每万公里影响
    },
    "宝马3系": {
        "years": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        "new_price_min": 291900,
        "new_price_max": 403900,
        "depreciation_adjust": [0.18, 0.12, 0.10, 0.08, 0.06, 0.05, 0.04],
        "mileage_factor": 0.03,
    }
}
```

## 估值算法

```python
class CarValuation:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.brand = None
        self.model = None
        self.year = None
        self.mileage = 0  # 万公里
        self.condition = "good"  # excellent/good/fair/poor
        self.transmission = "auto"  # auto/manual
        self.displacement = 0.0  # 排量L
        self.accident_history = False
        self.color = "white"
        self.registration_city = ""
    
    def base_value(self):
        """基础残值 = 新车价 × (1 - 年均折旧)^年数"""
        if not self.model or not self.year:
            return {"error": "请指定车型和年份"}
        
        age = 2026 - self.year
        if age < 0:
            return {"error": "年份不能大于今年"}
        
        # 折旧计算
        depr_rate = 0.15  # 首年15%
        if age == 0:
            depr_rate = 0.05  # 准新车衰减5%
        elif age <= 3:
            depr_rate = 0.12  # 2-3年每年12%
        elif age <= 6:
            depr_rate = 0.08  # 4-6年每年8%
        else:
            depr_rate = 0.05  # 7年以上每年5%
        
        # 参考新车价
        new_price = self.new_price_estimate()
        resale = new_price * (1 - depr_rate) ** age
        
        return {
            "new_price": new_price,
            "current_value": round(resale),
            "depreciation_rate": depr_rate,
            "age_years": age
        }
    
    def mileage_adjustment(self):
        """里程调整：每超1万公里/年减3%"""
        expected_mileage = self.age_years * 2  # 年均2万公里
        diff = self.mileage - expected_mileage
        return max(diff * 0.03, -0.15)  # 最多减15%
    
    def condition_adjustment(self):
        """车况调整"""
        factors = {
            "excellent": 1.05,
            "good": 1.0,
            "fair": 0.90,
            "poor": 0.75
        }
        return factors.get(self.condition, 1.0)
    
    def accident_penalty(self):
        """事故减损"""
        if self.accident_history:
            return 0.80  # 事故车打8折
        return 1.0
    
    def color_premium(self):
        """颜色溢价"""
        premium_colors = ["白色", "黑色", "银色"]  # 保值色
        if self.color in premium_colors:
            return 1.0
        return 0.98
    
    def final_value(self):
        base = self.base_value()
        if "error" in base:
            return base
        
        value = base["current_value"]
        value *= self.condition_adjustment()
        value *= self.accident_penalty()
        value *= self.color_premium()
        
        return {
            "estimated_value": round(value),
            "confidence": "high" if self.condition == "excellent" else "medium",
            "age": base["age_years"],
            "factors": {
                "original_price": base["new_price"],
                "depreciation": base["current_value"],
                "condition_factor": self.condition_adjustment(),
                "accident_penalty": self.accident_penalty()
            }
        }
    
    def new_price_estimate(self):
        """估算新车指导价（简化版）"""
        # 实际应查数据库或爬取汽车之家
        return 200000  # 默认20万

# 使用示例
cv = CarValuation()
cv.model = "比亚迪唐DM"
cv.year = 2021
cv.mileage = 5.0
cv.condition = "good"
cv.color = "白色"
result = cv.final_value()
print(f"预估价值: {result['estimated_value']:,}元")
```

## 数据来源（免费）

### 来源1：汽车之家（爬取）
```python
import requests
from bs4 import BeautifulSoup

def get_car_model_price(model_name):
    """汽车之家查车型价格"""
    url = f"https://xl.16888.com/s/{model_name}.htm"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    # 解析价格数据
    return prices
```

### 来源2：瓜子二手车估价
```python
# 瓜子二手车上的真实成交价
url = "https://www.guazi.com/估值接口"
```

## 车辆检测项目清单
```
外观：漆面/钣金/玻璃/轮胎轮毂
内饰：座椅/仪表盘/电子设备
发动机：启动/怠速/加速/异响
变速箱：换挡/顿挫/抖动
底盘：悬挂/刹车/转向
电器：空调/音响/灯光/电瓶
路试：加速/制动/跑偏/异响
事故检测：结构件/覆盖件/火烧/水泡
```

## 最佳实践
- 估价时参考3个数据源取中值：汽车之家/瓜子/优信
- 新能源车保值率普遍比燃油车低（3年保值率约50-65%）
- 事故车贬值可达20-30%
- 小众品牌/冷门颜色更难出手
- 每年二手车3-4月行情最高，7-8月最低

## 参考来源
- 汽车之家: https://www.autohome.com.cn
- 瓜子二手车: https://www.guazi.com
- 精真估: http://www.jingzhengu.com
