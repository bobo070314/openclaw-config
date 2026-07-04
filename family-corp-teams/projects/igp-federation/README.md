# IGP Federation — 联邦系统

## 核心理念
连接国内版(18789)和国际版(18791) OpenClaw 实例之间的桥梁。

## 架构
```
国内版实例 ←→ 共享文件目录 (shared/) ←→ 国际版实例
```
不依赖 HTTP，靠文件交换数据。

## 组件
1. **bridge_v2.py** — 文件级联邦桥
   - 连接两个实例
   - 消息交换
   - 项目状态同步

2. **shared/** — 共享数据目录
   - igp-global/ — 国际版出站
   - igp-china/ — 国内版出站

## 使用
```powershell
$env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'; python projects/igp-federation/bridge_v2.py
```

## 路线图
- v2: 文件级联邦 ✅ 已运行
- v3: 跨实例 Agent 同步
- v4: 联邦仲裁（跨实例决策）
