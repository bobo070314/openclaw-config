# 创建带图标的 OpenClaw Foreign 快捷方式
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\OpenClaw Foreign.lnk")
$Shortcut.TargetPath = "D:\bobo\openclaw-foreign\start-foreign.bat"
$Shortcut.WorkingDirectory = "D:\bobo\openclaw-foreign"
$Shortcut.IconLocation = "D:\bobo\openclaw-foreign\openclaw\openclaw.exe,0"
$Shortcut.Description = "OpenClaw Foreign Edition (Port 18900)"
$Shortcut.Save()
Write-Host "快捷方式已创建到桌面: OpenClaw Foreign.lnk" -ForegroundColor Green
