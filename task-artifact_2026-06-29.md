# OpenClaw Foreign 启动问题诊断

## 问题描述
用户点击桌面快捷方式后：
1. ✅ CMD 窗口正常弹出
2. ✅ 浏览器打开
3. ❌ VS Code 自动弹出（不应该）
4. ❌ 浏览器显示的是 QClaw 页面（"Foreign系统启动指南"），而非 OpenClaw Foreign

## 根本原因分析
- 浏览器连接到了 QClaw 网关（端口 18789），而非 Foreign 网关（端口 18900）
- 说明 Foreign 网关启动失败或未正确启动
- VS Code 可能是之前已打开，或 Foreign 启动失败后的 fallback 行为

## 已执行的修复
1. 创建了新的启动脚本 `start-foreign-v2.bat`，完全隔离 QClaw 环境变量
2. 设置了 `OPENCLAW_CONFIG_PATH` 指向 Foreign 专属配置
3. 清理了可能冲突的 QClaw 环境变量

## 待验证
需要用户测试新的启动脚本是否正常工作
