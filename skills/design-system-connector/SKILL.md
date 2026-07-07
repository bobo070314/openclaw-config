# Design System Connector

## 描述
专业的设计系统连接专家，帮助用户连接和使用设计系统，确保设计一致性和开发效率。

## 功能列表

### 1. parse-design-tokens
解析设计Token——从设计文件中提取设计Token
- **输入**：设计文件（Figma/Sketch/JSON）
- **输出**：设计Token

### 2. generate-css-vars
生成CSS变量——从设计Token生成CSS变量
- **输入**：设计Token
- **输出**：CSS变量

### 3. sync-components
同步组件——同步设计和代码组件
- **输入**：设计组件、代码组件
- **输出**：同步结果

### 4. check-consistency
检查一致性——检查实现与设计的一致性
- **输入**：设计规范、代码实现
- **输出**：一致性检查结果

### 5. export-specs
导出规范——导出设计规范文档
- **输入**：设计系统
- **输出**：规范文档

## 使用示例

### 示例1：解析设计Token
```json
{
  "function": "parse-design-tokens",
  "params": {
    "designFile": "design-system.fig",
    "source": "figma"
  }
}
```

### 示例2：生成CSS变量
```json
{
  "function": "generate-css-vars",
  "params": {
    "tokens": {
      "colors": {
        "primary": "#0056b3",
        "secondary": "#f0f4f8"
      },
      "spacing": {
        "sm": "8px",
        "md": "16px",
        "lg": "24px"
      }
    },
    "framework": "tailwind"
  }
}
```

### 示例3：检查一致性
```json
{
  "function": "check-consistency",
  "params": {
    "design": {
      "button": {"height": 40, "color": "#0056b3"}
    },
    "implementation": {
      "button": {"height": 40, "color": "#004a9e"}
    }
  }
}
```

## 输出格式

### 设计Token
```json
{
  "colors": {
    "primary": {"value": "#0056b3", "type": "color"},
    "secondary": {"value": "#f0f4f8", "type": "color"}
  },
  "spacing": {
    "sm": {"value": "8px", "type": "dimension"},
    "md": {"value": "16px", "type": "dimension"}
  },
  "typography": {
    "h1": {"size": 32, "weight": "bold"}
  }
}
```

### 一致性检查
```json
{
  "consistent": true,
  "differences": [
    {
      "component": "Button",
      "property": "color",
      "design": "#0056b3",
      "code": "#004a9e",
      "status": "mismatch"
    }
  ],
  "matchRate": 95
}
```

## 分配部门

### 主要分配
- **设计部**：设计系统维护
- **研发部**：前端开发
- **IT部**：系统开发

### 协作分配
- **数据部**：数据处理
- **质管部**：质量检查
- **文化部**：品牌管理

## 限制条件

1. **版本一致性**：设计与代码版本必须一致
2. **Token标准化**：设计Token必须标准化
3. **自动同步**：设计与代码自动同步
4. **及时更新**：设计变更及时通知

## 最佳实践

1. **单源设计系统**：设计系统是唯一的真实来源
2. **自动同步**：设计变更自动同步到代码
3. **定期检查**：定期检查设计与代码的一致性
4. **版本控制**：设计系统和代码一起版本控制

## 常见问题

**Q: 如何连接设计和代码？**
A: 使用设计Token连接设计和代码，设计变更自动生成Token。

**Q: 如何检查一致性？**
A: 使用check-consistency函数，输入设计规范和代码实现。

**Q: 如何处理设计与代码的差异？**
A: 评估差异原因，更新设计或修复代码，确保一致性。

---

**Skill名称**：design-system-connector
**版本**：1.0.0
**创建时间**：2026-06-30
**创建人**：龙家科技集团-设计部
