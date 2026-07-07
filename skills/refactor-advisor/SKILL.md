# Skill: refactor-advisor

**Skill名称**: refactor-advisor
**功能**: 代码重构建议系统
**作者**: 龙家科技集团 - 研发部
**版本**: v1.0
**创建时间**: 2026-06-30

---

## 📋 Skill概述

### 功能描述

自动识别代码异味（Code Smells），分析代码质量问题，提供详细的重构方案和重构步骤建议。

### 核心价值

- ✅ 识别代码异味，预防技术债积累
- ✅ 提供详细的重构方案，降低重构风险
- ✅ 自动生成重构前后对比，验证重构效果
- ✅ 支持多种重构模式（SOLID原则、设计模式、性能优化等）

### 适用场景

- 代码审查阶段
- 代码重构前评估
- 技术债清理
- 代码质量提升

---

## 🎯 核心功能

### 1. 代码异味检测

| 异味类型 | 检测内容 | 优先级 |
|---------|---------|--------|
| **过长函数** | 函数超过100行 | P0 |
| **重复代码** | 重复代码超过3次 | P0 |
| **过类** | 类超过500行 | P0 |
| **过长参数列表** | 参数超过5个 | P1 |
| **循环依赖** | 循环依赖检测 | P1 |
| **魔法数字** | 魔法数字检测 | P1 |
| **硬编码字符串** | 硬编码字符串检测 | P2 |
| **注释代码** | 注释代码检测 | P2 |

### 2. 重构方案生成

| 重构类型 | 说明 | 示例 |
|---------|------|------|
| **提取方法** | 将大函数拆分为小函数 | `extract-method` |
| **提取类** | 将大类拆分为小类 | `extract-class` |
| **提取接口** | 提取接口定义 | `extract-interface` |
| **简化条件** | 简化复杂条件 | `simplify-condition` |
| **合并重复代码** | 消除重复 | `merge-duplicate-code` |
| **引入设计模式** | 应用设计模式 | `introduce-pattern` |
| **性能优化** | 性能重构建议 | `performance-optimize` |

### 3. 重构前后对比

- ✅ 重构前代码片段
- ✅ 重构后代码片段
- ✅ 重构说明
- ✅ 重构效果指标

---

## 🚀 使用方式

### 基本用法

```bash
# 调用Skill
refactor-advisor analyze <code-snippet>
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `code-snippet` | string | 是 | 需要分析代码片段 |
| `language` | string | 否 | 编程语言（默认自动识别） |
| `mode` | string | 否 | 分析模式（default/performance/safety） |
| `level` | string | 否 | 分析级别（quick/standard/deep） |

### 使用示例

#### 示例1: 基础代码异味分析

```bash
refactor-advisor analyze "def calculate_total(items): total = 0 for item in items: total += item['price'] * item['quantity'] return total"
```

#### 示例2: 性能优化分析

```bash
refactor-advisor analyze "def process_data(data): result = [] for item in data: if item['active']: result.append(item['name']) return result" mode=performance
```

#### 示例3: 深度分析

```bash
refactor-advisor analyze "def complex_function(a, b, c, d, e, f): ..." level=deep
```

---

## 📊 分析输出

### 输出格式

```markdown
# 代码重构建议报告

## 📋 基本信息
- 分析时间: 2026-06-30 11:00:00
- 代码语言: Python
- 分析级别: Standard
- 检测到异味: 3个

## 🔍 检测到的代码异味

### 1. 过长函数
- **位置**: Line 1-10
- **问题**: 函数超过100行
- **优先级**: P0
- **建议**: 提取方法，拆分为多个小函数

### 2. 重复代码
- **位置**: Line 5-7, 9-11
- **问题**: 重复代码出现2次
- **优先级**: P0
- **建议**: 提取公共方法

### 3. 魔法数字
- **位置**: Line 3
- **问题**: 硬编码数字100
- **优先级**: P1
- **建议**: 提取为常量

## 🛠️ 重构方案

### 方案1: 提取方法
- **重构前**:
```python
def calculate_total(items):
    total = 0
    for item in items:
        total += item['price'] * item['quantity']
    return total
```

- **重构后**:
```python
def calculate_total(items):
    total = 0
    for item in items:
        total += _calculate_item_total(item)
    return total

def _calculate_item_total(item):
    return item['price'] * item['quantity']
```

- **重构效果**:
  - 代码行数: 10行 → 5行
  - 函数复杂度: 8 → 3
  - 可读性: ⬆️ 提升
  - 可维护性: ⬆️ 提升

## 📈 重构建议优先级

1. **P0**: 提取方法（消除过长函数）
2. **P0**: 提取公共方法（消除重复代码）
3. **P1**: 提取常量（消除魔法数字）
```

---

## 🔧 配置参数

### Skill配置文件

```yaml
# SKILL.yaml

# 分析配置
analysis:
  max_function_length: 100  # 最大函数长度
  max_class_length: 500     # 最大类长度
  max_parameters: 5         # 最大参数数量
  duplicate_threshold: 3    # 重复代码阈值

# 优先级配置
priority:
  P0: critical               # 严重问题
  P1: high                    # 高优先级
  P2: medium                  # 中优先级

# 模式配置
modes:
  default:
    check: [long-function, duplicate-code, magic-number]
    level: standard

  performance:
    check: [long-function, duplicate-code, magic-number, performance-bottleneck]
    level: deep

  safety:
    check: [long-function, duplicate-code, magic-number, security-risk]
    level: standard

# 输出配置
output:
  format: markdown
  include_diff: true
  include_metrics: true
  include_example: true
```

---

## 🎯 集成到Agent

### 对应Agent

| Agent | 部门 | 职责 | 集成方式 |
|-------|------|------|---------|
| **代码导航专家** | 研发部 | 代码导航、审查、优化 | 核心技能 |
| **自进化专家** | 研发部 | 技能创建、自动优化 | 技能开发 |
| **安全审计专家** | 质管部 | 代码安全审计 | 辅助技能 |

### 使用流程

```
代码导航专家
    ↓
调用 refactor-advisor
    ↓
分析代码异味
    ↓
生成重构建议
    ↓
提供重构方案
    ↓
执行重构
    ↓
验证重构效果
```

---

## 📊 质量指标

### 分析准确率

- **代码异味检测准确率**: ≥95%
- **重构方案合理性**: ≥90%
- **重构效果验证准确率**: ≥85%

### 性能指标

- **分析速度**: <5秒/100行
- **内存占用**: <100MB
- **并发处理能力**: 100个请求/秒

---

## 🔒 安全考虑

### 安全检查

- ✅ 不修改用户代码
- ✅ 仅提供建议，不自动执行
- ✅ 支持代码脱敏
- ✅ 支持私有代码保护

### 数据隐私

- ✅ 分析数据本地处理
- ✅ 不上传代码到云端
- ✅ 支持数据加密

---

## 📚 参考文档

### 相关概念

- **代码异味**: Martin Fowler, "Refactoring: Improving the Design of Existing Code"
- **重构模式**: "Refactoring Patterns" by Martin Fowler
- **设计原则**: SOLID原则、DRY原则、KISS原则

### 工具推荐

- **SonarQube**: 代码质量分析工具
- **ESLint**: JavaScript代码检查
- **Pylint**: Python代码检查
- **RuboCop**: Ruby代码检查

---

## 🔄 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v1.0 | 2026-06-30 | 初始版本发布 |

---

## 👥 维护团队

- **负责人**: 代码导航专家
- **技术支持**: 自进化专家
- **审核**: 安全审计专家
- **反馈**: 通过家族集团公司反馈系统

---

## 📞 反馈与支持

### 反馈渠道

- **家族会议**: 每月周会反馈
- **问题报告**: 通过家族集团公司系统提交
- **改进建议**: 通过自进化专家技能创建

### 联系方式

- **部门**: 研发部
- **负责人**: 代码导航专家
- **邮箱**: rd@dragon-family-corp.com

---

**Skill状态**: ✅ 开发中
**下次更新**: 2026-07-07
