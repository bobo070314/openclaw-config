"""IGP Git工具 — 统一git操作,解决中文/空格/shell编码问题"""
import subprocess
import sys
import os
from pathlib import Path

WORKSPACE = Path(r"D:\bobo\openclaw-foreign\workspace")

def git(args, cwd=None, timeout=30):
    """安全的git调用, 参数列表传避免shell解析问题"""
    cwd = cwd or WORKSPACE
    cmd = ["git"] + args
    r = subprocess.run(cmd, capture_output=True, text=True, 
                       encoding="utf-8", errors="replace",
                       cwd=cwd, timeout=timeout)
    return r

def git_commit_with_message(msg):
    """解决中文commit -m问题: 用-F从文件读"""
    tmp = WORKSPACE / ".igp_tmp_commit_msg.txt"
    tmp.write_text(msg, encoding="utf-8")
    r = git(["commit", "-F", str(tmp)])
    if tmp.exists():
        tmp.unlink()
    return r

def git_checkout_branch(branch_name):
    """安全创建或切换分支"""
    r = git(["checkout", "-b", branch_name])
    if r.returncode != 0 and "already exists" in (r.stderr or ""):
        r = git(["checkout", branch_name])
    return r

def git_add(paths=None):
    if isinstance(paths, str):
        paths = [paths]
    args = ["add"] + (paths if paths else ["-A"])
    return git(args)

def git_push(branch):
    return git(["push", "origin", branch, "--set-upstream"])

def gh_pr_create(title, body, draft=True):
    """gh pr create — 安全处理中文"""
    cmd = ["gh", "pr", "create"]
    if draft:
        cmd.append("--draft")
    cmd.extend(["--title", title, "--body", body])
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace",
                       cwd=WORKSPACE, timeout=30)
    return r

def demo_pr():
    """一键创建演示PR"""
    branch = f"igp-v3-auto-{__import__('datetime').date.today().isoformat()}"
    
    print(f"=== 分支: {branch} ===")
    
    # 1. checkout
    r = git_checkout_branch(branch)
    print(f"  checkout: {r.stdout[:100] + r.stderr[:100]}")
    
    # 2. 创建演示文件
    demo = WORKSPACE / "igp_v3_auto_report.md"
    demo.write_text(f"""# IGP v3 Auto Report
Generated: {__import__('datetime').datetime.now().isoformat()}
""", encoding="utf-8")
    
    # 3. add
    r = git_add()
    print(f"  add: {r.stderr[:100] or r.stdout[:100]}")
    
    # 4. commit (从文件读中文消息)
    r = git_commit_with_message("IGP v3 自动维护: 演示PR")
    print(f"  commit: {r.stdout[:100] + r.stderr[:100]}")
    
    # 5. push
    r = git_push(branch)
    print(f"  push: {r.stderr[:100] or r.stdout[:100]}")
    
    # 6. gh pr create
    r = gh_pr_create("IGP v3 自动维护演示", "自动创建的PR\n由IGP v3数字生命体生成", draft=True)
    print(f"  gh: {r.stdout[:200] + r.stderr[:200]}")
    
    return branch

if __name__ == "__main__":
    r = git(["status", "--short"])
    if r.returncode == 0:
        print(f"Git status:\n{r.stdout[:300]}")
        if r.stdout.strip():
            r2 = git(["log", "--oneline", "-3"])
            print(f"\nRecent commits:\n{r2.stdout}")
    
    # 如果有修改就创建演示PR
    if r.stdout.strip():
        branch = demo_pr()
        print(f"\n✅ PR管道完成: {branch}")
    else:
        print("没有未提交的修改")
