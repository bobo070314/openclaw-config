# skill-auto-engine — 自动化Skill发现与迭代引擎

> 自动扫描GitHub热榜、技术社区、用户需求，生成Skill → 部署 → 迭代推优

## 一、需求解读

用户要的不是手动一个个写Skill，而是一个**自动流水线**：
1. 自动发现「值得做成Skill的东西」
2. 自动生成SKILL.md
3. 自动部署到skills/目录
4. 自动评估好坏（通过使用频率、用户反馈、自我检测）
5. 自动淘汰差的，保留好的，迭代优化

## 二、技能发现源（自动扫描）

### 来源1：GitHub Trending（每日）
- 爬GitHub Trending：`https://github.com/trending`
- 识别高星项目（>500 Star）
- 判断是否适合做成Skill（判断标准：有CLI/API/SDK，可以AI操作，可复用）
- 生成SKILL.md

### 来源2：用户对话（实时）
- 用户提到某个工具/平台/技术 → 自动记录候选
- 如果出现3次以上 → 生成Skill草稿

### 来源3：OpenClaw Skills社区
- https://github.com/openclaw/skills 有新Skill → 自动分析

### 来源4：国内技术平台
- 掘金/知乎/InfoQ热门技术标签 → 提取为Skill候选

## 三、用户当前提到的Skill需求

以下是用户本轮提到的，全部需要创建：

| 领域 | Skill需求 | 优先级 |
|------|-----------|--------|
| 🐂 股票/金融 | A股/港股/美股行情、技术分析、量化交易 | ⭐⭐⭐ |
| 🚚 物流 | 快递查询、物流跟踪、运力调度 | ⭐⭐⭐ |
| 🚗 二手车 | 车况评估、价格估值、交易流程 | ⭐⭐⭐ |
| 📄 车辆手续 | 过户、上牌、年检、保险 | ⭐⭐⭐ |
| 🔧 车辆维修 | 故障码诊断、维修指南、保养周期 | ⭐⭐⭐ |
| ⚡ 新能源车 | 充电桩、电池健康、续航评估 | ⭐⭐⭐ |
| 🏎️ 车辆模型 | 汽车型号库、参数对比、配置推荐 | ⭐⭐ |
| ☯️ 风水 | 风水咨询、家居布局、办公室方位 | ⭐⭐ |
| 💡 未知补充 | 用户说"还没想到" → 持续发现 | 自动 |

## 四、自动化流程设计

```
[发现层]
GitHub Trending → 候选池
用户对话 → 候选池  
技术社区 → 候选池

[生成层]
候选池 → 信息提取 → 写SKILL.md → 部署到skills/
                              ↓
                          SKILLS-INDEX.md 更新

[评估层]
使用频率统计 → 用户反馈收集 → 质量打分
                            ↓
                    分数 > 阈值 → 保留优化
                    分数 < 阈值 → 标记淘汰

[迭代层]
保留Skill → 定期用新信息更新SKILL.md
淘汰Skill → 移入archive/目录，记录经验
```

## 五、候选Skill清单（待生成）

按优先级排序，用户提到和未提到的：

### P0 - 立刻创建（用户明确提到）
1. `stock-market-china` — 中国股市（A股/港股行情+技术分析）
2. `china-logistics` — 物流快递查询（菜鸟/顺丰/京东/通达系）
3. `used-car-valuation` — 二手车评估估值
4. `vehicle-registration` — 车辆过户上牌年检手续
5. `vehicle-maintenance` — 车辆维修保养指南
6. `new-energy-vehicle` — 新能源车知识（充电/电池/续航）
7. `vehicle-model-database` — 汽车型号参数库

### P1 - 值得创建（用户提到但非核心）
8. `fengshui-consultant` — 风水咨询（家居/办公布局）
9. `crypto-trading` — 加密货币/Web3交易（结合已有web3 skill）
10. `china-stock-quant` — 中国A股量化交易分析
11. `car-insurance` — 车险计算与比对
12. `auto-parts-database` — 汽车零部件查询
13. `charging-station-navigation` — 充电桩地图导航

### P2 - 自动发现候选（用户没想到但相关）
14. `house-valuation` — 房价评估与楼市分析
15. `insurance-planner` — 保险方案配置
16. `education-exam` — 考试/资格证查询
17. `health-tcm` — 中医养生/中药查询
18. `travel-china` — 国内旅游指南/攻略
19. `pet-care` — 宠物饲养指南
20. `home-renovation` — 装修预算/材料/流程
21. `matchmaking-fortune` — 八字合婚/星座配对
22. `zhougong-dream` — 周公解梦
23. `face-reading` — 面相学

## 六、评估标准（淘汰用）

| 指标 | 优秀 | 及格 | 淘汰 |
|------|------|------|------|
| 使用频率/月 | >50次 | 5-50次 | <5次 |
| 用户反馈 | 明确点赞 | 无反馈 | 被吐槽 |
| 信息完整度 | 覆盖80%+API | 基本框架 | 内容过少 |
| 时效性 | 2025+ | 2023-2024 | <2022 |

评估触发：每周自动评估一次，得分最低的3个Skill标记淘汰。

## 七、存档经验

淘汰的Skill不移除文件，移入 `skills-archive/` 目录，并记录淘汰原因。
以后同类需求直接复用历史经验，不用从头开发。
