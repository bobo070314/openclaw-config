@echo off
echo Creating shortcut...

powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\国际版-OpenClaw.lnk'); $Shortcut.TargetPath = 'cmd.exe'; $Shortcut.Arguments = '/c ""D:\bobo\openclaw-foreign\start-foreign.bat""'; $Shortcut.WorkingDirectory = 'D:\bobo\openclaw-foreign'; $Shortcut.IconLocation = 'C:\Program Files\QClaw\v0.2.29.592\openclaw.exe,0'; $Shortcut.Description = 'OpenClaw Foreign Edition'; $Shortcut.Save()"

echo Shortcut created!
pause
