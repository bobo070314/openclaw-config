---
name: deployment-automation
description: >
  DevSecOps deployment automation — builds Docker images, pushes to registry,
  deploys with docker-compose, runs health checks, and auto-invokes
  security-audit before deployment. Supports build-only, deploy-only,
  and full pipeline modes. Use when user says "deploy", "ship it",
  "push to production", "build and deploy", "CI/CD pipeline".
version: 0.2.0
status: implemented
category: devsecops
---

# Deployment Automation — DevSecOps 部署引擎

## 定位
DevSecOps 一键部署流水线。Docker 构建 → 推送到镜像仓库 → docker-compose 部署 → 健康检查四步一体化。部署前自动调用 `security-audit` 做安全自检，阻断漏洞容器上线。

## 触发条件
- 用户说"部署" / "deploy" / "ship it" / "push to production"
- "build and deploy" / "CI/CD pipeline" / "上线"
- Docker 项目需要自动化部署流程

## 工作流
1. **安全自检** — 链式调用 `security-audit` 扫描部署文件，CRITICAL 发现 → 阻断
2. **Docker 构建** — `docker build -t <image>:<tag>` 带构建参数
3. **镜像推送** — `docker push` 到指定 registry
4. **服务部署** — `docker-compose up -d` 滚动更新
5. **健康检查** — 轮询 HTTP 200 + 超时告警

## 关键约束
- 部署前强制通过 security-audit（无 CRITICAL 发现）
- 支持分步模式：build-only / deploy-only / full-pipeline
- 镜像标签自动生成（基于 git commit SHA + 时间戳）
- 健康检查可配置等待时间和重试次数
