"""
IGP MCP Bridge — 读/写文件、执行shell、git操作的统一工具层

设计哲学：
- 不依赖外部 MCP Server 运行
- 直接调用 Python 的 subprocess/pathlib 实现标准 MCP 工具接口
- 将来可升级为连接真正的 MCP Server (filesystem/git/shell)
"""

import subprocess, pathlib, json, os, shutil, tempfile, sys
from typing import Optional

WORKSPACE = pathlib.Path(r"D:\bobo\openclaw-foreign\workspace")

class IGP_MCP:
    """IGP自带的MCP工具层 — 提供文件/Git/Shell操作"""

    def __init__(self, workdir=None):
        self.sandbox = None  # Docker沙箱实例 (可选)
        self.workdir = pathlib.Path(workdir) if workdir else WORKSPACE

    # ── 工具函数 ──

    def read_file(self, path: str) -> str:
        """读取文件内容"""
        p = self._resolve(path)
        if not p.exists():
            return f"ERROR: 文件不存在: {path}"
        return p.read_text(encoding="utf-8")

    def write_file(self, path: str, content: str) -> str:
        """写入文件（自动创建目录）"""
        p = self._resolve(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"OK: 写入 {path} ({len(content)} bytes)"

    def edit_file(self, path: str, old: str, new: str) -> str:
        """精确替换文件中的文本"""
        p = self._resolve(path)
        content = p.read_text(encoding="utf-8")
        if old not in content:
            return f"ERROR: 未找到匹配文本: {old[:50]}..."
        if content.count(old) != 1:
            return f"ERROR: 找到{content.count(old)}处匹配，需要唯一匹配"
        content = content.replace(old, new, 1)
        p.write_text(content, encoding="utf-8")
        return f"OK: 替换成功 {path}"

    def shell(self, command: str, timeout: int = 30, cwd: str = None) -> str:
        """在本地或沙箱中执行shell命令"""
        if self.sandbox:
            return self._sandbox_exec(command, timeout)
        else:
            return self._local_exec(command, cwd=cwd, timeout=timeout)

    def git_status(self, repo_path: str = ".") -> str:
        """Git status"""
        p = self._resolve(repo_path)
        return self._local_exec("git status --short", cwd=p, timeout=10)

    def git_diff(self, repo_path: str = ".") -> str:
        """Git diff (未提交的变更)"""
        p = self._resolve(repo_path)
        return self._local_exec("git diff", cwd=p, timeout=10)

    def git_commit(self, repo_path: str = ".", msg: str = "IGP auto commit") -> str:
        """创建Git commit"""
        p = self._resolve(repo_path)
        r1 = self._local_exec("git add -A", cwd=p)
        r2 = self._local_exec(f'git commit -m "{msg}"', cwd=p)
        return r1 + r2

    def ls(self, path: str = ".") -> str:
        """列出目录内容"""
        p = self._resolve(path)
        if not p.is_dir():
            return f"ERROR: 不是目录: {path}"
        items = []
        for f in p.iterdir():
            tag = "D" if f.is_dir() else "F"
            sz = f.stat().st_size if f.is_file() else 0
            items.append(f"{tag} {f.name:30s} {sz:>8,}b")
        return "\n".join(items)

    def glob(self, pattern: str) -> str:
        """通配符搜索"""
        results = list(self.workdir.rglob(pattern))
        if not results:
            return "无匹配"
        return "\n".join(str(r.relative_to(self.workdir)) for r in results[:50])

    # ── Docker沙箱 ──

    def sandbox_start(self, image: str = "python:3.12-slim") -> str:
        """启动Docker沙箱"""
        try:
            result = subprocess.run(
                ["docker", "run", "-d", "--rm", image, "sleep", "3600"],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                self.sandbox = result.stdout.strip()
                return f"OK: 沙箱启动 {self.sandbox[:12]}"
            return f"ERROR: {result.stderr}"
        except Exception as e:
            return f"ERROR: {e}"

    def sandbox_stop(self) -> str:
        """停止Docker沙箱"""
        if not self.sandbox:
            return "无运行中的沙箱"
        try:
            subprocess.run(["docker", "stop", self.sandbox], capture_output=True, timeout=10)
            self.sandbox = None
            return "OK: 沙箱停止"
        except Exception as e:
            return f"ERROR: {e}"

    # ── 内部 ──

    def _resolve(self, path: str) -> pathlib.Path:
        p = pathlib.Path(path)
        if p.is_absolute():
            return p
        return self.workdir / p

    def _local_exec(self, cmd: str, cwd=None, timeout=30) -> str:
        try:
            result = subprocess.run(
                cmd, shell=True, cwd=cwd or self.workdir,
                capture_output=True, text=True, timeout=timeout,
                encoding="utf-8", errors="replace"
            )
            out = result.stdout.strip()
            err = result.stderr.strip()
            if err:
                return f"OUT:\n{out}\n\nERR:\n{err}" if out else f"ERR:\n{err}"
            return out or "(空输出)"
        except subprocess.TimeoutExpired:
            return f"ERROR: 命令超时 ({timeout}s)"
        except Exception as e:
            return f"ERROR: {e}"

    def _sandbox_exec(self, cmd: str, timeout=30) -> str:
        if not self.sandbox:
            return "ERROR: 沙箱未启动"
        try:
            result = subprocess.run(
                ["docker", "exec", self.sandbox, "sh", "-c", cmd],
                capture_output=True, text=True, timeout=timeout,
                encoding="utf-8", errors="replace"
            )
            out = result.stdout.strip()
            err = result.stderr.strip()
            return out if out else (err if err else "(空输出)")
        except subprocess.TimeoutExpired:
            return f"ERROR: 沙箱命令超时 ({timeout}s)"
        except Exception as e:
            return f"ERROR: {e}"


if __name__ == "__main__":
    mcp = IGP_MCP()
    print("=== IGP MCP Bridge Test ===")
    print(f"工作目录: {mcp.workdir}")
    print()
    print("[ls] workspace:")
    print(mcp.ls("."))
