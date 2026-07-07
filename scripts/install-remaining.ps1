schtasks /create /tn "OpenClaw\Gateway AutoStart" /xml "D:\bobo\openclaw-foreign\scripts\task-gateway-autostart.xml" /f
schtasks /create /tn "OpenClaw\IGP API AutoStart" /xml "D:\bobo\openclaw-foreign\scripts\task-igp-api-autostart.xml" /f
Write-Host "Done. Press any key..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
