#!/usr/bin/env python3
"""
qclaw-env v0.2.0 — OpenClaw skill 全链路环境诊断与安装工具。安装任何 CLI、命令行工具、包管理器、运行时环境时必须使用此 skill。使用场景包括但不限于：(1) 安装或配置任何命令行工具或 CLI（如 gh、ffmpeg、whisper 等），(2) 安装 OpenClaw skill 所需的依赖环境（包括底层运行时 node/npm、python3/pip3、go、uv），(3) 遇到 'command not found'、'未找到命令'、'不是内部或外部命令' 等错误，(4) 用户说'帮我装 xxx'、'安装 xxx'、'配置 xxx 环境'、'setup xxx'、'install xxx'，(5) 检测系统已安装哪些工具、检查环境、环境诊断，(6) 安装包管理器（brew、scoop、winget、choco、npm、pip 等），(7) 配置 API Key、环境变量、PATH 等运行时配置，(8) 配置国内镜像源（Homebrew、npm、pip、Go proxy 等）。此 skill 为强制性入口，所有安装类操作必须遵循'先检测后安装'原则。

Usage:
  python run.py [--json] [--dry-run] [--version]
"""
import argparse
import json
import sys
import os

VERSION = "0.2.0"
SKILL_NAME = "qclaw-env"

# No custom functions — pure skeleton skill (declarative knowledge in SKILL.md)


def main():
    parser = argparse.ArgumentParser(description="OpenClaw skill 全链路环境诊断与安装工具。安装任何 CLI、命令行工具、包管理器、运行时环境时必须使用此 skill。使用场景包括但不限于：(1) 安装或配置任何命令行工具或 CLI（如 gh、ffmpeg、whisper 等），(2) 安装 OpenClaw skill 所需的依赖环境（包括底层运行时 node/npm、python3/pip3、go、uv），(3) 遇到 'command not found'、'未找到命令'、'不是内部或外部命令' 等错误，(4) 用户说'帮我装 xxx'、'安装 xxx'、'配置 xxx 环境'、'setup xxx'、'install xxx'，(5) 检测系统已安装哪些工具、检查环境、环境诊断，(6) 安装包管理器（brew、scoop、winget、choco、npm、pip 等），(7) 配置 API Key、环境变量、PATH 等运行时配置，(8) 配置国内镜像源（Homebrew、npm、pip、Go proxy 等）。此 skill 为强制性入口，所有安装类操作必须遵循'先检测后安装'原则。")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--dry-run", action="store_true", help="Preview mode")
    parser.add_argument("--version", action="store_true", help="Show version")
    args = parser.parse_args()

    if args.version:
        print(json.dumps({"skill": SKILL_NAME, "version": VERSION, "status": "live"}, indent=2))
        return 0

    info = {"skill": SKILL_NAME, "version": VERSION, "status": "live"}

    if args.dry_run:
        info["dry_run"] = True
        info["note"] = "Dry run — skeleton skill, no side effects."
        print(json.dumps(info, indent=2))
        return 0

    info["note"] = "Skeleton skill — functionality defined in SKILL.md"

    print(json.dumps(info, indent=2) if args.json else json.dumps(info, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
