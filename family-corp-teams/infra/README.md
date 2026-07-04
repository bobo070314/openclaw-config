# fix_env.py 使用说明

## 功能
该脚本旨在解决在OpenClaw exec环境下运行Python脚本时出现的中文编码问题。

## 使用方法
1. 确保工作目录为 `D:\bobo\openclaw-foreign\workspace`
2. 运行脚本: `C:\Python314\python.exe fix_env.py`

## 验证
执行脚本后，应满足以下条件:
- 中文输出正常
- 不报任何PowerShell错误
- 能正常读取 `pending_tickets.json` 文件