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

### ❌ chcp 65001 >nul 在 OpenClaw exec 下必炸（2026-07-01）
**现象**: `chcp 65001 >nul` 报 `FileStream 打开不是文件的设备`
**根因**: OpenClaw exec 的 stdout 是 pipe 非文件句柄，PowerShell 的 `Out-File / >nul` 在 pipe 上调用 `new FileStream("nul", ...)` 失败
**修复**:
- ❌ `chcp 65001 >nul` — 已废弃
- ✅ `chcp 65001 2>&1 | Out-Null` — 安全版
- ✅ `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8` — 更干净
- `$env:PYTHONIOENCODING='utf-8'` 和 `$env:PYTHONUTF8='1'` 不受影响

### 来源
- Roo Code extension/core/tools.ts — 22 工具集设计
- Roo Code CLAUDE.md / AGENTS.md — 文件操作规则
- 本机实战验证：PowerShell 内联代码失败 10+ 次，走 .py 文件零失败

## Related

- [Agent workspace](/concepts/agent-workspace)
