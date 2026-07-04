"""IGP CI/CD — 安装 git hooks + 设置定时 CI"""
import subprocess, sys, os, shutil

V5 = r'D:\bobo\openclaw-foreign\workspace\family-corp-teams\v5'

def install_git_hook():
    """安装 pre-push git hook"""
    git_hooks = os.path.join(V5, '.git', 'hooks')
    hook_src = os.path.join(V5, 'v6', 'ci', 'ci_pre_push.py')
    
    if not os.path.exists(git_hooks):
        print(f"[SKIP] No .git/hooks directory at {git_hooks}")
        print("[INFO] 非 git 仓库，跳过 hook 安装")
        return False
    
    # pre-push hook: 调用 Python 脚本
    hook_path = os.path.join(git_hooks, 'pre-push')
    hook_content = f'''#!/usr/bin/env python3
"""IGP CI Pre-Push Hook — auto-generated"""
import subprocess, sys, os
V5 = r"{V5}"
hook = os.path.join(V5, "v6", "ci", "ci_pre_push.py")
r = subprocess.run([sys.executable, hook], capture_output=False)
sys.exit(r.returncode)
'''
    with open(hook_path, 'w', encoding='utf-8') as f:
        f.write(hook_content)
    print(f"[OK] pre-push hook 已安装: {hook_path}")
    return True

def setup_cron():
    """设置定时 cron job（用 OpenClaw cron）"""
    # 这里只是打印说明，实际 cron 需要在 OpenClaw 面板配置
    print()
    print("=" * 50)
    print(" 定时 CI 配置说明")
    print("=" * 50)
    print()
    print(" 在 OpenClaw WebChat 输入: ")
    print()
    print("  早上9点每天跑IGP CI pipeline")
    print()
    
    # 或者直接在 OpenClaw 内的 cron 配置
    print(" 或者手动添加 cron job:")
    print()
    print(f"  python {V5}\\v6\\ci\\ci_pre_push.py")
    print()
    print("=" * 50)

if __name__ == '__main__':
    print("=== IGP CI/CD Setup ===")
    print()
    install_git_hook()
    print()
    setup_cron()
    print()
    print("Done!")
