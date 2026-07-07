# vehicle-model-db — 汽车型号数据库

> 汽车型号参数对比数据库 — 支持品牌/车型/配置/价格/动力/尺寸查询

## 使用场景
- 查看某个车型的详细参数
- 多车型横向对比
- 根据条件筛选推荐车型
- 查找同级别竞品

## 车型数据库结构

```python
class CarModelDatabase:
    """汽车型号数据库（内置常见车型参数）"""
    
    # 品牌索引
    BRANDS = {
        # 国产
        "比亚迪": {
            "country": "中国",
            "type": "国产",
            "models": ["海鸥", "海豚", "海豹", "汉", "唐", "元PLUS", "宋PLUS", "秦PLUS"]
        },
        "蔚来": {
            "country": "中国",
            "type": "新势力",
            "models": ["ES6", "ES8", "ET5", "ET7", "EC6"]
        },
        "理想": {
            "country": "中国", 
            "type": "新势力",
            "models": ["L6", "L7", "L8", "L9", "MEGA"]
        },
        "小鹏": {
            "country": "中国",
            "type": "新势力",
            "models": ["P7", "G6", "G9", "X9"]
        },
        "小米": {
            "country": "中国",
            "type": "新势力",
            "models": ["SU7"]
        },
        "吉利": {
            "country": "中国",
            "type": "国产",
            "models": ["星瑞", "星越L", "博越L", "极氪001", "极氪007"]
        },
        "长城": {
            "country": "中国",
            "type": "国产",
            "models": ["哈弗H6", "坦克300", "坦克500", "魏牌蓝山"]
        },
        # 合资/进口
        "特斯拉": {
            "country": "美国",
            "type": "进口/国产",
            "models": ["Model 3", "Model Y", "Cybertruck"]
        },
        "宝马": {
            "country": "德国",
            "type": "豪华",
            "models": ["3系", "5系", "X3", "X5", "i3", "iX3"]
        },
        "奔驰": {
            "country": "德国",
            "type": "豪华",
            "models": ["C级", "E级", "GLC", "GLE", "EQS"]
        },
        "奥迪": {
            "country": "德国",
            "type": "豪华",
            "models": ["A4L", "A6L", "Q5L", "Q7"]
        },
        "大众": {
            "country": "德国",
            "type": "合资",
            "models": ["帕萨特", "迈腾", "途观L", "ID.3", "ID.4"]
        },
        "丰田": {
            "country": "日本",
            "type": "合资",
            "models": ["卡罗拉", "凯美瑞", "RAV4", "汉兰达", "普拉多"]
        },
        "本田": {
            "country": "日本",
            "type": "合资",
            "models": ["思域", "雅阁", "CR-V", "皓影"]
        }
    }
    
    # 车型详细参数（示例）
    MODELS = {
        "特斯拉Model 3": {
            "brand": "特斯拉",
            "level": "中型轿车",
            "price_range": "(24.59万-33.59万)",
            "power_type": "BEV",
            "range_cltc": "606-713km",
            "size": "4720×1848×1442mm",
            "wheelbase": "2875mm",
            "0-100": "3.1-6.1s",
            "motor": "后驱/四驱",
            "battery": "60-78.4kWh",
            "charge": "250kW超充",
            "competitors": ["比亚迪海豹", "小鹏P7", "小米SU7", "蔚来ET5"]
        },
        "比亚迪汉EV": {
            "brand": "比亚迪",
            "level": "中大型轿车",
            "price_range": "(17.98万-24.98万)",
            "power_type": "BEV",
            "range_cltc": "506-715km",
            "size": "4995×1910×1495mm",
            "wheelbase": "2920mm",
            "0-100": "3.9-7.9s",
            "motor": "前驱/四驱",
            "battery": "60.48-85.44kWh(刀片电池)",
            "charge": "120kW快充",
            "competitors": ["特斯拉Model 3", "小鹏P7", "蔚来ET5"]
        },
        "理想L7": {
            "brand": "理想",
            "level": "中大型SUV",
            "price_range": "(30.18万-37.98万)",
            "power_type": "EREV(增程)",
            "range_cltc": "1100km(综合)",
            "size": "5050×1995×1750mm",
            "wheelbase": "3005mm",
            "0-100": "5.3s",
            "motor": "双电机四驱",
            "battery": "42.8kWh",
            "fuel_tank": "65L",
            "competitors": ["宝马X5", "问界M7", "蔚来ES6"]
        },
        "丰田卡罗拉": {
            "brand": "丰田",
            "level": "紧凑型轿车",
            "price_range": "(11.68万-15.58万)",
            "power_type": "燃油/HEV",
            "fuel_consumption": "5.1-5.9L/100km",
            "size": "4635×1780×1455mm",
            "wheelbase": "2700mm",
            "engine": "1.2T/1.8L混动",
            "transmission": "CVT/E-CVT",
            "competitors": ["日产轩逸", "大众朗逸", "本田思域"]
        }
    }
    
    def search_by_brand(self, brand):
        """按品牌搜索所有车型"""
        brand_info = self.BRANDS.get(brand)
        if not brand_info:
            return f"未找到品牌: {brand}"
        
        result = f"=== {brand} ({brand_info['type']}) ===\n"
        for model in brand_info['models']:
            if model in self.MODELS:
                info = self.MODELS[model]
                result += f"  {model}: {info['level']}, {info['price_range']}\n"
            else:
                result += f"  {model}\n"
        return result
    
    def compare_models(self, *model_names):
        """横向对比多个车型"""
        result = []
        for name in model_names:
            if name in self.MODELS:
                m = self.MODELS[name]
                result.append({
                    "name": name,
                    "level": m['level'],
                    "price": m['price_range'],
                    "type": m['power_type'],
                    "range": m.get('range_cltc', m.get('fuel_consumption', '-')),
                    "size": m['size'],
                    "0-100": m.get('0-100', '-'),
                    "wheelbase": m['wheelbase'],
                })
        return result
    
    def recommend(self, budget_max=None, budget_min=None, power_type=None, level=None):
        """条件筛选推荐"""
        results = []
        for name, info in self.MODELS.items():
            price = info['price_range']
            matches = True
            if power_type and info['power_type'] != power_type:
                matches = False
            if level and info['level'] != level:
                matches = False
            if matches:
                results.append((name, info))
        return results
```

## 使用示例

```python
db = CarModelDatabase()

# 查品牌
print(db.search_by_brand("比亚迪"))

# 对比
compare = db.compare_models("特斯拉Model 3", "比亚迪汉EV", "小米SU7")
import json
print(json.dumps(compare, ensure_ascii=False, indent=2))

# 推荐
recommendations = db.recommend(budget_max=30, power_type="BEV", level="中型轿车")
for name, info in recommendations:
    print(f"{name}: {info['price_range']}")
```

## 竞品分析表（热门级别）

| 级别 | 车型1 | 车型2 | 车型3 | 车型4 |
|------|-------|-------|-------|-------|
| 紧凑型轿车 | 卡罗拉 | 轩逸 | 朗逸 | 思域 |
| 中型轿车 | 特斯拉Model 3 | 比亚迪海豹 | 小鹏P7 | 宝马3系 |
| 中大型轿车 | 比亚迪汉 | 蔚来ET7 | 小米SU7 | 奔驰E级 |
| 中型SUV | Model Y | 比亚迪宋PLUS | 理想L6 | 大众途观L |
| 中大型SUV | 理想L7/L8 | 问界M7 | 宝马X5 | 蔚来ES6 |
| MPV | 腾势D9 | 丰田赛那 | 极氪009 | 理想MEGA |

## 数据源推荐
- 懂车帝车型库 API: https://www.dongchedi.com
- 汽车之家规格对比: https://www.autohome.com.cn
- 工信部新车申报目录: https://www.miit.gov.cn
