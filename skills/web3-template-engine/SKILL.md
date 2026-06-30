# Web3 Template Engine

## 描述
专业的Web3.0模板引擎专家，帮助用户快速生成去中心化应用、NFT展示、智能合约交互等Web3相关的演示文稿和页面模板。

## 功能列表

### 1. generate-web3-presentation
生成Web3演示文稿
- **输入**：Web3项目主题、目标受众
- **输出**：完整的Web3风格PPT/页面模板

### 2. create-nft-gallery
创建NFT展示模板
- **输入**：NFT集合信息、展示方式
- **输出**：NFT画廊模板

### 3. design-dapp-intro
设计DApp介绍页
- **输入**：DApp功能描述
- **输出**：DApp介绍模板

### 4. smart-contract-diagram
智能合约架构图
- **输入**：合约逻辑描述
- **输出**：架构图模板

### 5. tokenomics-template
代币经济学模板
- **输入**：代币经济模型
- **输出**：代币经济学展示模板

## 使用示例

### 示例1：生成Web3演示
```json
{
  "function": "generate-web3-presentation",
  "params": {
    "topic": "DeFi借贷协议",
    "audience": "投资人",
    "features": ["流动性质押", "闪电贷", "跨链桥"],
    "style": "赛博朋克"
  }
}
```

### 示例2：创建NFT展示
```json
{
  "function": "create-nft-gallery",
  "params": {
    "collection": "CryptoPunks",
    "items": 5,
    "layout": "网格",
    "theme": "暗色"
  }
}
```

### 示例3：代币经济学
```json
{
  "function": "tokenomics-template",
  "params": {
    "tokenName": "TEST",
    "totalSupply": "1000000000",
    "distribution": [
      {"type": "团队", "percent": 20},
      {"type": "社区", "percent": 40},
      {"type": "投资者", "percent": 20},
      {"type": "国库", "percent": 20}
    ]
  }
}
```

## 输出格式

### Web3演示模板
```json
{
  "pages": [
    {
      "type": "title",
      "content": {
        "title": "项目名称",
        "subtitle": "子标题",
        "background": "dark-gradient"
      }
    },
    {
      "type": "slide",
      "content": {
        "title": "技术架构",
        "points": ["Layer 2解决方案", "跨链通信"],
        "diagram": "blockchain-architecture"
      }
    }
  ],
  "theme": "cyberpunk-dark",
  "animations": true
}
```

## 分配部门

### 主要分配
- **研发部**：区块链项目
- **创新部**：Web3创新项目
- **投资部**：Web3投资评估

### 协作分配
- **市场部**：Web3营销材料
- **设计部**：UI设计

## 最佳实践

1. **暗色主题优先**：Web3项目通常使用暗色主题，凸显科技感
2. **动效增强**：使用粒子特效、渐变动画等增强视觉冲击
3. **数据可视化**：代币经济学、TVL等数据用图表直观展示
4. **安全强调**：智能合约审计、安全特性需要突出展示

---

**Skill名称**：web3-template-engine
**版本**：1.0.0
**创建时间**：2026-06-30
