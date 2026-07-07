' OpenClaw Fix — 静默提权执行（VBS + Shell.Application ShellExecute runas）
Set oShell = CreateObject("Shell.Application")
sDir = "D:\bobo\openclaw-foreign\scripts"
sCmd = "powershell.exe"
sArgs = "-NoProfile -ExecutionPolicy Bypass -Command """ & sDir & "\fix-tasks-admin.bat"""
oShell.ShellExecute sCmd, sArgs, sDir, "runas", 1
