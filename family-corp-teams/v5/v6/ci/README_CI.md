# IGP V5 CI/CD 配置手册

## 一键运行
双击 `v6\ci\run_ci.bat` 或命令行：
```
cd v5
v6\ci\run_ci.bat
```

## 安装 Git Pre-Push Hook
每次 `git push` 前自动跑全量检查：
```
python v6\ci\setup_hooks.py
```

## 配置 OpenClaw 定时 CI
在 WebChat 输入：
> 每天早上9点跑：python -W ignore D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\ci\ci_pre_push.py

或者手动配 cron job：
1. 打开 OpenClaw Web 面板
2. 进入 Cron Jobs
3. 添加定时任务，cron 表达式: `0 9 * * *`（北京时间9:00）
4. 命令: `python D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5\v6\ci\ci_pre_push.py`

## CI 文件结构
```
v6\ci\
├── run_ci.bat        # 一键 CI（Windows双击运行）
├── ci_pre_push.py    # pre-push hook（Python）
├── setup_hooks.py    # 安装 hook 到 .git/hooks/
├── pipeline.py       # 核心 pipeline（9/9）
├── deploy.py         # 部署验证
├── ci_status.log     # CI 状态日志
└── README_CI.md      # 本文件
```
