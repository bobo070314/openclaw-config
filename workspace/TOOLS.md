# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Windows 环境坑点（2026-06-23 token-saver 踩坑记录）

### PowerShell 吃引号
- ❌ `python -u -c "multi-line code with quotes"` → PowerShell 解析引号导致 SyntaxError
- ✅ 走 .py 文件执行，不要 inline 复杂的多行代码
- ✅ 简单单行无引号可用 -c，但只要涉及嵌套引号就走文件

### subprocess encoding
- Windows 下 `subprocess.run(..., text=True)` 默认用 GBK 解码
- git/现代 CLI 输出 UTF-8 → UnicodeDecodeError
- ✅ 加 `encoding="utf-8", errors="replace"`

### datetime.UTC
- Python 3.11+ 才有 `datetime.UTC`
- ✅ 兼容写法：`from datetime import datetime, timezone; UTC = timezone.utc`

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Roo Code 精选规则（2026-06-24 迁移）

### 文件操作铁律
- **写文件必须用 write 工具（fs 直写），严禁 exec 内联代码**
- PowerShell 会把 Python/JS 代码中的引号、反斜杠、括号全搞乱
- `python -c "f=open('x.py','w'); f.write('print(\"hello\")')"` ← PowerShell 必炸
- 替代方案：先用 write 工具落盘脚本，再 exec 执行脚本

### 工具优先级（2026-06-30 更新）
1. write / read / edit（文件操作，直通 fs）
2. grep：用 python subprocess 替代 findstr / Select-String
3. git：用 git CLI，避免 PowerShell 管道包装（见 git_safe_push.py）
4. exec：仅用于执行命令，绝不用于写文件

### 💥 血泪教训：永远不要 inline Python（2026-06-30）
**这是第 N 次踩坑**。哪怕只是读取一行 JSON 或打印一行信息，
只要涉及 `print(f"...{var['key']}...")` 这种嵌套引号，
PowerShell 必炸，报 SyntaxError: unterminated string literal。

**生死规则：**
- 哪怕3行代码 → 走 .py 文件
- 哪怕1行有 f-string + dict access → 走 .py 文件
- 只有纯 `print("hello")` 这种无嵌套引号的才 inline
- 检测标准：如果 cmd 里要先调 env 设编码，就说明该走文件了

### ✅ 标准执行模板（2026-07-07 09:15 升级 v2 — 解决 'run_py.bat' 被SIGKILL + openclaw CLI配置冲突）

**🔴 2026-07-07 09:15 新发现：`run_py.bat` 在 OpenClaw exec pipe 下可能卡死**
- 现象：`Set-Location D:\bobo\openclaw-foreign; D:\bobo\openclaw-foreign\run_py.bat _myscript.py` → Process 被 SIGKILL
- 根因：`@echo off` + pipe stdout 导致一些 Python 进程未正常结束

**新铁律（三选一，按优先级）：**
```
🥇 python D:\path\to\script.py（绝对路径，最稳）
🥇 D:\bobo\openclaw-foreign\run_py.bat D:\path\to\script.py（绝对路径+双保险）
❌ Set-Location + 相对路径 + run_py.bat（Pipe死锁高风险）
❌ 任何形式的 inline python -c
❌ 任何形式的 $env:PYTHONIOENCODING + python -c
```

**直接执行 Python（🥇黄金规则）：**
```
# ✅ 最佳实践：绝对路径 + 直接 python 调用
python D:\bobo\openclaw-foreign\workspace\example.py

# ✅ 用 run_py.bat 时也给绝对路径
D:\bobo\openclaw-foreign\run_py.bat D:\bobo\openclaw-foreign\workspace\example.py
```

**🔴 `openclaw` CLI 串行规则（2026-07-07 09:15 新增）**
- 多 CLI 命令不可并行执行（`openclaw models ...` 同时跑 → ConfigMutationConflictError）
- 必须等一个完成后再跑下一个
- 特别是 `openclaw models fallbacks add/set` 这种写 config 的操作

**检测标准：** 任何时候要执行 Python，直接走绝对路径文件。不用想、不用判断。
文件 vs 内联不是选择题。

### ❌ chcp 65001 >nul 在 OpenClaw exec 下必炸（2026-07-01）
**现象**: `chcp 65001 >nul` 报 `FileStream 打开不是文件的设备`
**根因**: OpenClaw exec 的 stdout 是 pipe 非文件句柄，PowerShell 的 `Out-File / >nul` 在 pipe 上调用 `new FileStream("nul", ...)` 失败
**修复**:
- ❌ `chcp 65001 >nul` — 已废弃
- ✅ `chcp 65001 2>&1 | Out-Null` — 安全版
- ✅ `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8` — 更干净
- `$env:PYTHONIOENCODING='utf-8'` 和 `$env:PYTHONUTF8='1'` 不受影响

### ❌ `cd /d` 是 CMD 语法，不是 PowerShell（2026-07-07 新增）
**现象**: `cd /d D:\bobo\openclaw-foreign && python script.py` 报 `标记“&&”不是此版本中的有效语句分隔符`

**根因**: 
- `cd /d` 是 `cmd.exe` 的语法，PowerShell 不认识 `/d` 参数
- `&&`（条件执行）是 PowerShell **7+** 才有的功能，Windows 默认 PowerShell **5.x** 不支持

**修复（三选一）**:
```powershell
# ✅ 方案A: 分号 + Set-Location（最稳，PS5/7 通用）
Set-Location D:\bobo\openclaw-foreign; D:\bobo\openclaw-foreign\run_py.bat _nightly_sweep.py

# ✅ 方案B: 先 cd 再独立 exec（OpenClaw exec 最佳实践）
exec(command="D:\bobo\openclaw-foreign\run_py.bat _nightly_sweep.py", workdir="D:\bobo\openclaw-foreign")

# ✅ 方案C: PowerShell 7 安全写法（仅在知道 PS7 可用时）
cd D:\bobo\openclaw-foreign && D:\bobo\openclaw-foreign\run_py.bat _nightly_sweep.py
```

**生死规则（预防）**:
- 永远用 `Set-Location` 替代 `cd /d` — 前者 PowerShell 原生
- 永远用 `;` 替代 `&&` — 除非确认是 PowerShell 7 环境
- 优先传 `workdir` 参数到 exec 工具，比自己 cd 干净

### 来源
- Roo Code extension/core/tools.ts — 22 工具集设计
- Roo Code CLAUDE.md / AGENTS.md — 文件操作规则
- 本机实战验证：PowerShell 内联代码失败 10+ 次，走 .py 文件零失败

## Related

- [Agent workspace](/concepts/agent-workspace)
