---
name: security-audit
description: >
  Infrastructure security audit — scans Dockerfile, docker-compose,
  CI/CD workflows (.github, .gitlab-ci, Jenkins), .env files, Terraform,
  shell scripts, private keys (.pem/.key), and JSON/YAML configs for
  hardcoded secrets, misconfigurations, and compliance violations.
  12 rules across 4 risk tiers: CRITICAL (tokens/keys), HIGH (latest tag,
  root user, privileged mode, CI injection), MEDIUM (exposed ports,
  missing .dockerignore), LOW. Generates Markdown report with fix examples.
  Critical findings exit 1. Use when user says "security audit",
  "scan for secrets", "check Dockerfile", "audit infrastructure",
  "review CI/CD security".
version: 0.2.0
status: implemented
category: devsecops
---

# Security Audit — 基础设施安全审计引擎

## 定位
对 Docker/K8s 部署文件做 12 条安全规则扫描，检出 `privileged: true`、root 用户、latest 标签、`.env` 真值泄露、CI/CD 注入等生产级漏洞。覆盖 Dockerfile、docker-compose、CI 工作流、Terraform、shell 脚本、密钥文件、环境配置 8 类文件。

**Dify 项目实测：96 条漏洞检出。**

## 触发条件
- 用户说"安全审计" / "scan for secrets" / "check infrastructure"
- "audit Dockerfile" / "review CI/CD security" / "find keys in repo"
- 部署前合规检查 / CI 管道安全门禁

## 工作流
1. **文件定位** — 扫描目标目录下的所有相关文件类型
2. **规则匹配** — 依次执行 12 条安全规则，按风险分级
3. **分级输出** — CRITICAL / HIGH / MEDIUM / LOW 四级 + 修复建议
4. **报告生成** — Markdown 表格报告，含文件名、行号、修复方案
5. **退出判定** — CRITICAL 发现 → exit 1（阻断 CI）

## 12 条安全规则

### 🔴 CRITICAL
| ID | Rule | 检测内容 |
|----|------|----------|
| CRIT-001 | 令牌暴露 | GitHub/AWS/API tokens in config/shell/workflow |
| CRIT-002 | AWS 密钥 | AKIA/ASIA Access Key hardcoded in Terraform/CI |
| CRIT-003 | 密钥文件 | .pem/.key committed to repository |
| CRIT-004 | .env 真值 | .env contains real tokens (non-placeholder values) |

### 🟠 HIGH
| ID | Rule | 检测内容 |
|----|------|----------|
| HIGH-001 | latest 标签 | FROM ...:latest — unreproducible builds |
| HIGH-002 | Root 运行 | Missing USER directive — runs as root |
| HIGH-003 | 特权容器 | docker-compose privileged:true or cap_add:SYS_ADMIN |
| HIGH-004 | CI 注入 | secret piped/redirected in shell command |

### 🟡 MEDIUM
| ID | Rule | 检测内容 |
|----|------|----------|
| MED-001 | 端口暴露 | Sensitive port (22/3306/5432/6379/9200) mapped to 0.0.0.0 |
| MED-002 | .dockerignore | Dockerfile missing .dockerignore |
| MED-003 | CI 权限 | CI/CD missing minimal GITHUB_TOKEN permissions |
| MED-004 | .gitignore | .env not in .gitignore — risk of accidental commit |

## 关键约束
- 不修改原始文件，仅输出审计报告
- 密钥检测支持脱敏输出（只显示前缀 + `***`）
- 与 `deployment-automation` 链式集成：部署前被自动调用做安全自检
