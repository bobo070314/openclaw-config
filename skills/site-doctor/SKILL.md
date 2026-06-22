---
name: site-doctor
description: >
  Website health check — diagnoses port conflicts, dependency versions,
  config completeness, build readiness, and runtime health for
  Next.js/FastAPI/Django projects. Use when user says "site doctor",
  "health check", "diagnose project", "why won't it start", "check port".
version: 0.2.0
status: implemented
category: dev
---

# Site Doctor — 网站健康诊断

## 定位
站点全科医生。对 Next.js/FastAPI/Django 项目做端口占用、依赖版本、配置完整性、构建就绪和运行时健康五维体检，一键诊断"为什么启动不了"。

## 触发条件
- 用户说"site doctor" / "health check" / "diagnose project"
- "why won't it start" / "check port" / "网站体检"
- 项目启动失败需要排错

## 工作流
1. **端口扫描** — 检查项目配置端口的占用情况（netstat / lsof）
2. **依赖检查** — 对比 package.json/requirements.txt 与 node_modules/venv 一致性
3. **配置验证** — 检查 .env 完整性 + 证书/密钥有效性
4. **构建检查** — 验证 build 产物的存在性和完整性
5. **运行时探测** — HTTP 健康检查 + 进程存活确认

## 关键约束
- 支持 Next.js / FastAPI / Django 三种框架自动检测
- 非破坏性诊断（不修改任何文件或进程）
- 输出彩色分级报告（🟢 PASS / 🟡 WARN / 🔴 FAIL）
- Windows 兼容 netstat，Linux 兼容 ss/lsof
