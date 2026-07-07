$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\OpenClaw-Foreign.lnk")
$Shortcut.TargetPath = "cmd.exe"
$Shortcut.Arguments = "/c `"D:\bobo\openclaw-foreign\start-foreign.bat`""
$Shortcut.WorkingDirectory = "D:\bobo\openclaw-foreign"
$Shortcut.IconLocation = "C:\Program Files\QClaw\v0.2.29.592\openclaw.exe,0"
$Shortcut.Description = "OpenClaw Foreign Edition"
$Shortcut.Save()
Write-Host "Shortcut created successfully"
