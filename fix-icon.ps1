# 修复桌面快捷方式图标
$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = "$desktop\国际版-OpenClaw.lnk"

if (Test-Path $shortcutPath) {
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    
    # 尝试从 QClaw 安装目录找图标
    $iconPaths = @(
        "C:\Program Files\QClaw\v0.2.29.592\resources\openclaw\openclaw.exe",
        "C:\Program Files\QClaw\v0.2.29.592\openclaw.exe",
        "D:\bobo\openclaw-foreign\openclaw\openclaw.exe"
    )
    
    $foundIcon = $null
    foreach ($path in $iconPaths) {
        if (Test-Path $path) {
            $foundIcon = $path
            break
        }
    }
    
    if ($foundIcon) {
        $Shortcut.IconLocation = "$foundIcon,0"
        $Shortcut.Save()
        Write-Host "图标已更新: $foundIcon" -ForegroundColor Green
    } else {
        # 如果没有 exe，尝试使用系统图标
        $Shortcut.IconLocation = "%SystemRoot%\System32\shell32.dll,14"
        $Shortcut.Save()
        Write-Host "使用系统默认图标" -ForegroundColor Yellow
    }
    
    # 刷新图标缓存
    Write-Host "刷新图标缓存..." -ForegroundColor Cyan
    ie4uinit.exe -show 2>$null
} else {
    Write-Host "找不到快捷方式: $shortcutPath" -ForegroundColor Red
}
