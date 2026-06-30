# Icon Selector

## 描述
专业的图标选择专家，帮助用户为UI/PPT设计选择最合适的图标。

## 功能列表

### 1. suggest-icons
建议图标
- **输入**：功能描述、风格要求
- **输出**：推荐的图标列表

### 2. match-style
匹配图标风格
- **输入**：现有图标风格
- **输出**：风格匹配图标

### 3. create-iconset
创建图标集
- **输入**：图标需求列表
- **输出**：完整的图标集

### 4. check-consistency
检查图标一致性
- **输入**：多图标
- **输出**：一致性检查结果

### 5. alternative-icons
提供替代图标
- **输入**：已选图标
- **输出**：替代方案

## 使用示例

### 示例1：建议图标
```json
{
  "function": "suggest-icons",
  "params": {
    "description": "用户设置页面",
    "actions": ["编辑", "删除", "添加", "搜索"],
    "style": "线性"
  }
}
```

### 示例2：匹配风格
```json
{
  "function": "match-style",
  "params": {
    "existingIconUrl": "https://example.com/icon.svg",
    "newDescriptions": ["主页", "消息", "个人中心"]
  }
}
```

## 输出格式

### 图标建议
```json
{
  "icons": [
    {
      "name": "settings",
      "description": "设置图标",
      "weight": "regular",
      "ligature": "settings"
    }
  ],
  "source": "Material Icons / Font Awesome / 自定义"
}
```

## 分配部门

### 主要分配
- **设计部**：UI设计
- **研发部**：前端开发
- **市场部**：营销素材

### 协作分配
- **运营部**：产品运营

---

**Skill名称**：icon-selector
**版本**：1.0.0
**创建时间**：2026-06-30
